#!/usr/bin/env python3
from __future__ import annotations

import sys
sys.dont_write_bytecode = True

import contextlib
import hashlib
import json
import os
import re
import shutil
import subprocess
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any, Iterable, Iterator, Mapping, Sequence
from urllib.parse import urlsplit, urlunsplit


@dataclass(frozen=True)
class Anchors:
    root_skill: str = "SKILL.md"
    orchestrator: str = "orchestrator/SKILL.md"
    registry: str = "orchestrator/registry.json"
    routes: str = "shared/manifests/routes.json"
    tooling: str = "shared/manifests/tooling.json"


@dataclass(frozen=True)
class ToolingIssue:
    code: str
    file: str
    entity: str
    received: str
    rule: str

    def render(self) -> str:
        return (
            f"[{self.code}] file={self.file} entity={self.entity} "
            f"received={self.received!r} rule={self.rule}"
        )


class ToolingError(RuntimeError):
    def __init__(self, issue: ToolingIssue):
        self.issue = issue
        super().__init__(issue.render())


@dataclass(frozen=True)
class SourceSection:
    id: str
    source_path: Path
    start: int
    end: int
    data: bytes


@dataclass
class RepositoryModel:
    root: Path
    anchors: Anchors
    registry: dict[str, Any]
    routes_manifest: dict[str, Any]
    source_index: dict[str, Any]
    tooling: dict[str, Any]
    skills_by_id: dict[str, dict[str, Any]]
    skill_order: list[str]
    cross_cutting_ids: list[str]
    expected_files: set[Path]
    sections: dict[str, SourceSection]
    source_manifests: list[Path]
    canonical_sources: list[Path]

    @property
    def shared_root(self) -> Path:
        raw = self.registry.get("shared", {}).get("root", "shared")
        return safe_path(self.root, raw, entity="registry.shared.root")


_GIT_OPERATIONS = (
    "MERGE_HEAD",
    "CHERRY_PICK_HEAD",
    "REVERT_HEAD",
    "BISECT_LOG",
    "rebase-merge",
    "rebase-apply",
)

_TASK_PATTERNS = {
    "build": re.compile(r"^build_[A-Za-z0-9][A-Za-z0-9_]*\.py$"),
    "validate": re.compile(r"^(?:validate_|verify_)[A-Za-z0-9][A-Za-z0-9_]*\.py$"),
}

_PREFLIGHTED_ROOTS: set[Path] = set()


def issue(code: str, file: Path | str, entity: str, received: Any, rule: str) -> ToolingError:
    return ToolingError(
        ToolingIssue(
            code=code,
            file=str(file),
            entity=entity,
            received=str(received),
            rule=rule,
        )
    )


def resolve_root(start: Path | None = None, override: Path | None = None, anchors: Anchors = Anchors()) -> Path:
    candidate = (override or start or Path(__file__)).expanduser()
    candidate = candidate if candidate.is_dir() else candidate.parent
    candidate = candidate.resolve(strict=True)
    matches: list[Path] = []
    current = candidate
    while True:
        if all((current / rel).is_file() for rel in (anchors.root_skill, anchors.orchestrator, anchors.registry, anchors.routes)):
            matches.append(current)
        if current.parent == current:
            break
        current = current.parent
    if not matches:
        raise issue("ROOT_NOT_FOUND", candidate, "repository-root", candidate, "required structural anchors must exist")
    root = matches[0]
    if root == Path(root.anchor):
        raise issue("UNSAFE_ROOT", root, "repository-root", root, "repository root must not be filesystem root")
    return root


def safe_path(root: Path, value: str | Path, *, entity: str, base: Path | None = None, must_exist: bool = False) -> Path:
    raw = str(value)
    posix = PurePosixPath(raw.replace("\\", "/"))
    if not raw or posix.is_absolute() or ".." in posix.parts:
        raise issue("UNSAFE_PATH", entity, entity, raw, "path must be non-empty, relative, and contain no '..'")
    candidate = ((base or root) / Path(*posix.parts)).resolve(strict=False)
    root_resolved = root.resolve(strict=True)
    try:
        candidate.relative_to(root_resolved)
    except ValueError as exc:
        raise issue("PATH_ESCAPE", entity, entity, raw, "resolved path must remain inside repository root") from exc
    if must_exist and not candidate.exists():
        raise issue("MISSING_PATH", candidate.relative_to(root_resolved), entity, raw, "referenced path must exist")
    if candidate.exists():
        resolved = candidate.resolve(strict=True)
        try:
            resolved.relative_to(root_resolved)
        except ValueError as exc:
            raise issue("SYMLINK_ESCAPE", candidate.relative_to(root_resolved), entity, raw, "symlink target must remain inside repository root") from exc
    return candidate


def relative(root: Path, path: Path) -> str:
    return path.resolve(strict=False).relative_to(root.resolve(strict=True)).as_posix()


def load_json(path: Path, *, root: Path | None = None) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise issue("MISSING_FILE", relative(root, path) if root else path, "json", path, "file must exist") from exc
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise issue("INVALID_JSON", relative(root, path) if root else path, "json", exc, "valid UTF-8 JSON required") from exc
    if not isinstance(value, dict):
        raise issue("INVALID_JSON_ROOT", relative(root, path) if root else path, "json", type(value).__name__, "JSON root must be an object")
    return value


def require_positive_schema(document: Mapping[str, Any], *, file: Path, supported: Sequence[int] | None = None) -> int:
    version = document.get("schemaVersion")
    if not isinstance(version, int) or isinstance(version, bool) or version < 1:
        raise issue("INVALID_SCHEMA_VERSION", file, "schemaVersion", version, "positive integer required")
    if supported is not None and version not in supported:
        raise issue("UNSUPPORTED_SCHEMA_VERSION", file, "schemaVersion", version, f"supported versions: {list(supported)}")
    return version


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def atomic_write(path: Path, data: bytes) -> bool:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.is_file() and path.read_bytes() == data:
        return False
    fd, temporary = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    temp_path = Path(temporary)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_path, path)
    finally:
        temp_path.unlink(missing_ok=True)
    return True


def atomic_write_json(path: Path, document: Mapping[str, Any]) -> bool:
    data = (json.dumps(document, indent=2, ensure_ascii=False, sort_keys=False) + "\n").encode("utf-8")
    return atomic_write(path, data)


def _iter_declared_paths(value: Any, *, key: str = "") -> Iterator[tuple[str, str]]:
    if isinstance(value, dict):
        for child_key, child in value.items():
            yield from _iter_declared_paths(child, key=child_key)
    elif isinstance(value, list):
        for child in value:
            yield from _iter_declared_paths(child, key=key)
    elif isinstance(value, str) and (
        key.lower().endswith(("file", "path", "catalog", "manifest", "entrypoint"))
        or key in {"orchestrator", "sourceIndex", "modelProfileFile", "routesManifest"}
    ):
        yield key, value


def _detect_cycle(graph: Mapping[str, Sequence[str]], *, code: str, file: Path) -> None:
    state: dict[str, int] = {}
    stack: list[str] = []

    def visit(node: str) -> None:
        marker = state.get(node, 0)
        if marker == 2:
            return
        if marker == 1:
            start = stack.index(node)
            cycle = stack[start:] + [node]
            raise issue(code, file, node, " -> ".join(cycle), "graph must be acyclic")
        state[node] = 1
        stack.append(node)
        for child in graph.get(node, ()):
            visit(child)
        stack.pop()
        state[node] = 2

    for node in graph:
        visit(node)


def expand_route(routes: Mapping[str, Any], route_name: str) -> tuple[list[str], list[str]]:
    if route_name not in routes:
        raise issue("UNKNOWN_ROUTE", "shared/manifests/routes.json", "route", route_name, "route must be declared")
    sections: list[str] = []
    files: list[str] = []
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(name: str) -> None:
        if name in visited:
            return
        if name in visiting:
            raise issue("ROUTE_CYCLE", "shared/manifests/routes.json", "route", name, "route extension graph must be acyclic")
        route = routes.get(name)
        if not isinstance(route, dict):
            raise issue("INVALID_ROUTE", "shared/manifests/routes.json", name, route, "route must be an object")
        visiting.add(name)
        for parent in route.get("extends", []):
            if parent not in routes:
                raise issue("UNKNOWN_ROUTE", "shared/manifests/routes.json", name, parent, "extended route must exist")
            visit(parent)
        for section in route.get("sections", []):
            if section not in sections:
                sections.append(section)
        for file_name in route.get("files", []):
            if file_name not in files:
                files.append(file_name)
        visiting.remove(name)
        visited.add(name)

    visit(route_name)
    return sections, files


def _parse_frontmatter_name(text: str) -> str | None:
    match = re.match(r"\A---\s*\n(.*?)\n---\s*\n", text, flags=re.DOTALL)
    if not match:
        return None
    for line in match.group(1).splitlines():
        key, sep, value = line.partition(":")
        if sep and key.strip() == "name":
            return value.strip().strip('"\'')
    return None


def load_repository_model(root: Path | None = None, *, verify_sources: bool = True) -> RepositoryModel:
    anchors = Anchors()
    root = resolve_root(root, anchors=anchors)
    registry_path = safe_path(root, anchors.registry, entity="registry", must_exist=True)
    registry = load_json(registry_path, root=root)
    require_positive_schema(registry, file=Path(anchors.registry))

    shared_config = registry.get("shared")
    if not isinstance(shared_config, dict):
        raise issue("INVALID_REGISTRY", anchors.registry, "shared", shared_config, "shared configuration object required")
    shared_root = safe_path(root, shared_config.get("root", "shared"), entity="registry.shared.root", must_exist=True)
    routes_rel = shared_config.get("routesManifest", anchors.routes)
    routes_path = safe_path(root, routes_rel, entity="registry.shared.routesManifest", must_exist=True)
    routes_manifest = load_json(routes_path, root=root)
    require_positive_schema(routes_manifest, file=Path(relative(root, routes_path)))
    routes = routes_manifest.get("routes")
    if not isinstance(routes, dict):
        raise issue("INVALID_ROUTES", relative(root, routes_path), "routes", routes, "routes object required")
    route_graph: dict[str, list[str]] = {}
    for route_id, route in routes.items():
        if not isinstance(route_id, str) or not route_id:
            raise issue("INVALID_ROUTE_ID", relative(root, routes_path), "route", route_id, "non-empty string required")
        if not isinstance(route, dict):
            raise issue("INVALID_ROUTE", relative(root, routes_path), route_id, route, "route object required")
        for field in ("extends", "sections", "files"):
            values = route.get(field, [])
            if not isinstance(values, list) or any(not isinstance(value, str) or not value for value in values):
                raise issue("INVALID_ROUTE", relative(root, routes_path), f"{route_id}.{field}", values, "string array required")
        route_graph[route_id] = list(route.get("extends", []))
        for parent in route_graph[route_id]:
            if parent not in routes:
                raise issue("UNKNOWN_ROUTE", relative(root, routes_path), route_id, parent, "extended route must exist")
    _detect_cycle(route_graph, code="ROUTE_CYCLE", file=Path(relative(root, routes_path)))

    skills = registry.get("skills")
    if not isinstance(skills, list):
        raise issue("INVALID_REGISTRY", anchors.registry, "skills", skills, "skills array required")
    skills_by_id: dict[str, dict[str, Any]] = {}
    skill_order: list[str] = []
    expected: set[Path] = {
        safe_path(root, anchors.root_skill, entity="rootSkill", must_exist=True),
        safe_path(root, anchors.orchestrator, entity="orchestrator", must_exist=True),
        registry_path,
        routes_path,
    }
    dependency_graph: dict[str, list[str]] = {}
    for index, item in enumerate(skills):
        if not isinstance(item, dict):
            raise issue("INVALID_SKILL", anchors.registry, f"skills[{index}]", item, "skill object required")
        skill_id = item.get("id")
        if not isinstance(skill_id, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", skill_id):
            raise issue("INVALID_SKILL_ID", anchors.registry, f"skills[{index}].id", skill_id, "lowercase kebab-case required")
        if skill_id in skills_by_id:
            raise issue("DUPLICATE_SKILL_ID", anchors.registry, "skill.id", skill_id, "skill IDs must be unique")
        skill_file = item.get("skillFile")
        path = safe_path(root, skill_file, entity=f"skill:{skill_id}.skillFile", must_exist=True)
        expected.add(path)
        text = path.read_text(encoding="utf-8")
        if _parse_frontmatter_name(text) != skill_id:
            raise issue("SKILL_ID_MISMATCH", relative(root, path), "frontmatter.name", _parse_frontmatter_name(text), f"must equal {skill_id}")
        if path.parent.name != skill_id:
            raise issue("SKILL_DIRECTORY_MISMATCH", relative(root, path), "directory", path.parent.name, f"must equal {skill_id}")
        required_routes = item.get("requiredRoutes", [])
        optional_routes = item.get("optionalRoutes", [])
        for field, values in (("requiredRoutes", required_routes), ("optionalRoutes", optional_routes)):
            if not isinstance(values, list) or any(not isinstance(value, str) or not value for value in values):
                raise issue("INVALID_SKILL_ROUTES", anchors.registry, f"{skill_id}.{field}", values, "string array required")
        for route_id in required_routes + optional_routes:
            if route_id not in routes:
                raise issue("UNKNOWN_ROUTE", anchors.registry, skill_id, route_id, "skill routes must be declared")
        capabilities = item.get("capabilities")
        capability_keys = {"remoteReads", "remoteWrites", "localWrites"}
        if not isinstance(capabilities, dict) or set(capabilities) != capability_keys or any(not isinstance(value, bool) for value in capabilities.values()):
            raise issue("INVALID_CAPABILITIES", anchors.registry, skill_id, capabilities, f"boolean capability object with keys {sorted(capability_keys)} required")
        load_policy = item.get("loadPolicy")
        if not isinstance(load_policy, dict) or load_policy.get("onDemand") is not True:
            raise issue("INVALID_LOAD_POLICY", anchors.registry, skill_id, load_policy, "loadPolicy.onDemand must be true")
        dependencies = item.get("dependencies", [])
        if not isinstance(dependencies, list) or any(not isinstance(value, str) for value in dependencies):
            raise issue("INVALID_DEPENDENCIES", anchors.registry, skill_id, dependencies, "dependencies must be a string array")
        for resource in item.get("resources", []) + item.get("referenceFiles", []):
            resource_path = resource.get("path") if isinstance(resource, dict) else resource
            expected.add(safe_path(root, resource_path, entity=f"skill:{skill_id}.resource", must_exist=True))
        skills_by_id[skill_id] = item
        skill_order.append(skill_id)
        dependency_graph[skill_id] = dependencies
    for skill_id, dependencies in dependency_graph.items():
        for dependency in dependencies:
            if dependency not in skills_by_id:
                raise issue("UNKNOWN_DEPENDENCY", anchors.registry, skill_id, dependency, "dependency must be a registered skill")
    _detect_cycle(dependency_graph, code="DEPENDENCY_CYCLE", file=Path(anchors.registry))

    cross_cutting = registry.get("selectionPolicy", {}).get("crossCuttingSkillIds", [])
    if not isinstance(cross_cutting, list) or len(cross_cutting) != len(set(cross_cutting)):
        raise issue("INVALID_CROSS_CUTTING", anchors.registry, "selectionPolicy.crossCuttingSkillIds", cross_cutting, "unique skill ID array required")
    for skill_id in cross_cutting:
        if skill_id not in skills_by_id:
            raise issue("UNKNOWN_CROSS_CUTTING", anchors.registry, "crossCuttingSkillIds", skill_id, "ID must be registered")
        if skills_by_id[skill_id].get("role") != "cross-cutting":
            raise issue("CROSS_CUTTING_ROLE", anchors.registry, skill_id, skills_by_id[skill_id].get("role"), "role must be cross-cutting")
    auto_attach = registry.get("selectionPolicy", {}).get("autoAttach", {})
    if not isinstance(auto_attach, dict):
        raise issue("INVALID_AUTO_ATTACH", anchors.registry, "selectionPolicy.autoAttach", auto_attach, "object required")
    for skill_id in auto_attach:
        if skill_id not in cross_cutting:
            raise issue("UNKNOWN_AUTO_ATTACH", anchors.registry, "selectionPolicy.autoAttach", skill_id, "auto-attach entries must name registered cross-cutting skills")

    for _, path_value in _iter_declared_paths(registry):
        try:
            candidate = safe_path(root, path_value, entity="registry.path")
        except ToolingError:
            raise
        if candidate.is_file():
            expected.add(candidate)
    for path_key, path_value in _iter_declared_paths(routes_manifest):
        base = root if path_key == "entrypoint" else shared_root
        candidate = safe_path(root, path_value, entity=f"routes.{path_key}", base=base)
        if candidate.is_file():
            expected.add(candidate)

    source_index_rel = routes_manifest.get("sourceIndex")
    if not isinstance(source_index_rel, str):
        raise issue("MISSING_SOURCE_INDEX", relative(root, routes_path), "sourceIndex", source_index_rel, "source index path required")
    source_index_path = safe_path(root, source_index_rel, entity="routes.sourceIndex", base=shared_root, must_exist=True)
    expected.add(source_index_path)
    source_index = load_json(source_index_path, root=root)
    require_positive_schema(source_index, file=Path(relative(root, source_index_path)))

    sections: dict[str, SourceSection] = {}
    source_manifests: list[Path] = []
    canonical_sources: list[Path] = []
    seen_manifest_paths: set[str] = set()
    seen_source_paths: set[str] = set()
    source_entries = source_index.get("sources")
    if not isinstance(source_entries, list):
        raise issue("INVALID_SOURCE_INDEX", relative(root, source_index_path), "sources", source_entries, "sources array required")
    for source_position, entry in enumerate(source_entries):
        if not isinstance(entry, dict):
            raise issue("INVALID_SOURCE_ENTRY", relative(root, source_index_path), f"sources[{source_position}]", entry, "object required")
        manifest_rel = entry.get("path")
        canonical_rel = entry.get("canonicalPath")
        if manifest_rel in seen_manifest_paths:
            raise issue("DUPLICATE_SOURCE_MANIFEST", relative(root, source_index_path), "source.path", manifest_rel, "manifest paths must be unique")
        if canonical_rel in seen_source_paths:
            raise issue("DUPLICATE_CANONICAL_SOURCE", relative(root, source_index_path), "source.canonicalPath", canonical_rel, "canonical paths must be unique")
        seen_manifest_paths.add(manifest_rel)
        seen_source_paths.add(canonical_rel)
        manifest_path = safe_path(root, manifest_rel, entity="source-index.path", base=shared_root, must_exist=True)
        canonical_path = safe_path(root, canonical_rel, entity="source-index.canonicalPath", base=shared_root, must_exist=True)
        expected.update((manifest_path, canonical_path))
        source_manifests.append(manifest_path)
        canonical_sources.append(canonical_path)
        raw_manifest = manifest_path.read_bytes()
        declared_manifest_hash = entry.get("sha256")
        if not isinstance(declared_manifest_hash, str) or not re.fullmatch(r"[0-9a-f]{64}", declared_manifest_hash):
            raise issue("SOURCE_MANIFEST_HASH_MISSING", relative(root, source_index_path), manifest_rel, declared_manifest_hash, "lowercase SHA-256 required")
        if sha256_bytes(raw_manifest) != declared_manifest_hash:
            raise issue("SOURCE_MANIFEST_HASH", relative(root, manifest_path), "sha256", sha256_bytes(raw_manifest), declared_manifest_hash)
        manifest = load_json(manifest_path, root=root)
        require_positive_schema(manifest, file=Path(relative(root, manifest_path)))
        declared_source = safe_path(root, manifest.get("path"), entity="source-manifest.path", base=shared_root, must_exist=True)
        if declared_source != canonical_path:
            raise issue("SOURCE_PATH_MISMATCH", relative(root, manifest_path), "path", manifest.get("path"), canonical_rel)
        data = canonical_path.read_bytes()
        if verify_sources:
            if manifest.get("bytes") != len(data):
                raise issue("SOURCE_SIZE", relative(root, canonical_path), "bytes", len(data), manifest.get("bytes"))
            if manifest.get("sha256") != sha256_bytes(data):
                raise issue("SOURCE_HASH", relative(root, canonical_path), "sha256", sha256_bytes(data), manifest.get("sha256"))
        cursor = 0
        rebuilt: list[bytes] = []
        for section_position, section in enumerate(manifest.get("sections", [])):
            if not isinstance(section, dict):
                raise issue("INVALID_SECTION", relative(root, manifest_path), f"sections[{section_position}]", section, "object required")
            section_id = section.get("id")
            if not isinstance(section_id, str) or not section_id:
                raise issue("INVALID_SECTION_ID", relative(root, manifest_path), f"sections[{section_position}].id", section_id, "non-empty string required")
            if section_id in sections:
                raise issue("DUPLICATE_SECTION_ID", relative(root, manifest_path), "section.id", section_id, "section IDs must be globally unique")
            start = section.get("startByte")
            end = section.get("endByte")
            if not isinstance(start, int) or not isinstance(end, int) or start < 0 or end < start or end > len(data):
                raise issue("SECTION_RANGE", relative(root, manifest_path), section_id, f"{start}:{end}", f"0 <= start <= end <= {len(data)}")
            if start != cursor:
                code = "SECTION_GAP" if start > cursor else "SECTION_OVERLAP"
                raise issue(code, relative(root, manifest_path), section_id, start, f"startByte must equal previous endByte {cursor}")
            chunk = data[start:end]
            if verify_sources:
                if section.get("bytes") != len(chunk):
                    raise issue("SECTION_SIZE", relative(root, manifest_path), section_id, len(chunk), section.get("bytes"))
                if section.get("sha256") != sha256_bytes(chunk):
                    raise issue("SECTION_HASH", relative(root, manifest_path), section_id, sha256_bytes(chunk), section.get("sha256"))
            sections[section_id] = SourceSection(section_id, canonical_path, start, end, chunk)
            rebuilt.append(chunk)
            cursor = end
        if cursor != len(data):
            raise issue("SECTION_GAP", relative(root, manifest_path), "end", cursor, f"must cover source through byte {len(data)}")
        if verify_sources and b"".join(rebuilt) != data:
            raise issue("SOURCE_REBUILD", relative(root, canonical_path), "sections", "mismatch", "sections must reconstruct source byte-for-byte")

    for route_id, route in routes.items():
        for section_id in route.get("sections", []):
            if section_id not in sections:
                raise issue("UNKNOWN_SECTION", relative(root, routes_path), route_id, section_id, "route section must exist in source manifests")

    tooling_path = safe_path(root, anchors.tooling, entity="tooling", must_exist=True)
    expected.add(tooling_path)
    tooling = load_json(tooling_path, root=root)
    require_positive_schema(tooling, file=Path(anchors.tooling))

    required_headings = tooling.get("skillRequiredHeadings", [])
    if not isinstance(required_headings, list) or any(not isinstance(value, str) or not value for value in required_headings):
        raise issue("INVALID_SKILL_HEADINGS", anchors.tooling, "skillRequiredHeadings", required_headings, "string array required")
    for skill_id, item in skills_by_id.items():
        skill_path = safe_path(root, item["skillFile"], entity=f"skill:{skill_id}", must_exist=True)
        text = skill_path.read_text(encoding="utf-8")
        missing = [heading for heading in required_headings if heading not in text]
        if missing:
            raise issue("SKILL_HEADING_MISSING", relative(root, skill_path), skill_id, ", ".join(missing), "configured skill headings are required")

    text_contracts = tooling.get("textContracts", {})
    if not isinstance(text_contracts, dict):
        raise issue("INVALID_TEXT_CONTRACTS", anchors.tooling, "textContracts", text_contracts, "object required")
    for rel, markers in text_contracts.items():
        contract_path = safe_path(root, rel, entity="tooling.textContracts", must_exist=True)
        if not isinstance(markers, list) or any(not isinstance(marker, str) or not marker for marker in markers):
            raise issue("INVALID_TEXT_CONTRACTS", anchors.tooling, rel, markers, "marker string array required")
        text = contract_path.read_text(encoding="utf-8")
        missing = [marker for marker in markers if marker not in text]
        if missing:
            raise issue("TEXT_CONTRACT_MISSING", relative(root, contract_path), rel, ", ".join(missing), "configured semantic markers are required")

    active_text = "\n".join(
        [
            safe_path(root, anchors.root_skill, entity="rootSkill", must_exist=True).read_text(encoding="utf-8"),
            safe_path(root, anchors.orchestrator, entity="orchestrator", must_exist=True).read_text(encoding="utf-8"),
        ]
        + [safe_path(root, item["skillFile"], entity=f"skill:{skill_id}", must_exist=True).read_text(encoding="utf-8") for skill_id, item in skills_by_id.items()]
    )
    if re.search(r"(?m)^\s*(?:git\s+(?:clone|pull)|gh\s+(?:api|repo|pr|issue|run|workflow|release|search))\b", active_text):
        raise issue(
            "REMOTE_COMMAND_PROHIBITED",
            root,
            "active-hierarchy",
            "unmanaged remote git/gh command",
            "autonomous remote GitHub operations use the connector; local Git network access is limited to explicit publish tooling",
        )
    if re.search(r"(?mi)^\s*git\s+push\b[^\n]*(?:--force(?:-with-lease)?|--mirror|--all|--tags)\b", active_text):
        raise issue(
            "UNSAFE_PUSH_DOCUMENTED",
            root,
            "active-hierarchy",
            "unsafe push option",
            "explicit local publication must remain single-branch and non-forced",
        )
    workflow_files = tooling.get("workflowFiles", [])
    if not isinstance(workflow_files, list) or any(not isinstance(value, str) or not value for value in workflow_files):
        raise issue("INVALID_WORKFLOW_FILES", anchors.tooling, "workflowFiles", workflow_files, "workflowFiles must be a string array")
    if len(workflow_files) != len(set(workflow_files)):
        raise issue("DUPLICATE_WORKFLOW_FILE", anchors.tooling, "workflowFiles", workflow_files, "workflow paths must be unique")

    declared_workflows: set[Path] = set()
    for workflow_rel in workflow_files:
        workflow_posix = PurePosixPath(workflow_rel.replace("\\", "/"))
        if workflow_posix.parent != PurePosixPath(".github/workflows") or workflow_posix.suffix not in {".yml", ".yaml"}:
            raise issue("INVALID_WORKFLOW_PATH", anchors.tooling, "workflowFiles", workflow_rel, "workflow must be a .yml or .yaml file directly under .github/workflows")
        workflow_path = safe_path(root, workflow_rel, entity="tooling.workflowFiles", must_exist=True)
        if not workflow_path.is_file():
            raise issue("INVALID_WORKFLOW_FILE", relative(root, workflow_path), "workflow", workflow_path, "declared workflow must be a regular file")
        workflow_text = workflow_path.read_text(encoding="utf-8")
        if not re.search(r"(?m)^on:\s*(?:#.*)?$", workflow_text):
            raise issue("WORKFLOW_TRIGGER_MISSING", relative(root, workflow_path), "on", "missing", "workflow must declare triggers")
        if not re.search(r"(?m)^permissions:\s*(?:#.*)?$", workflow_text):
            raise issue("WORKFLOW_PERMISSIONS_MISSING", relative(root, workflow_path), "permissions", "missing", "workflow must declare explicit top-level permissions")
        if not re.search(r"(?m)^\s+timeout-minutes:\s*[1-9][0-9]*\s*(?:#.*)?$", workflow_text):
            raise issue("WORKFLOW_TIMEOUT_MISSING", relative(root, workflow_path), "timeout-minutes", "missing", "every workflow must declare a positive job timeout")
        if re.search(r"(?m)^\s*pull_request_target\s*:", workflow_text):
            raise issue("WORKFLOW_TRIGGER_PROHIBITED", relative(root, workflow_path), "trigger", "pull_request_target", "privileged pull_request_target workflows are prohibited")
        for action_spec in re.findall(r"(?m)^\s*(?:-\s*)?uses:\s*([^\s#]+)", workflow_text):
            if action_spec.startswith("./"):
                continue
            action, separator, action_ref = action_spec.rpartition("@")
            if not separator or not action or not re.fullmatch(r"[0-9a-f]{40}", action_ref):
                raise issue("UNPINNED_WORKFLOW_ACTION", relative(root, workflow_path), "uses", action_spec, "external actions must be pinned to a full lowercase commit SHA")
        expected.add(workflow_path)
        declared_workflows.add(workflow_path.resolve())

    workflow_root = root / ".github" / "workflows"
    actual_workflows: set[Path] = set()
    if workflow_root.exists():
        if not workflow_root.is_dir():
            raise issue("INVALID_WORKFLOW_ROOT", relative(root, workflow_root), "workflows", workflow_root, ".github/workflows must be a directory")
        actual_workflows = {
            path.resolve()
            for path in workflow_root.iterdir()
            if path.is_file() and path.suffix in {".yml", ".yaml"}
        }
    undeclared_workflows = sorted(relative(root, path) for path in actual_workflows - declared_workflows)
    if undeclared_workflows:
        raise issue("UNDECLARED_GITHUB_WORKFLOW", relative(root, workflow_root), "workflows", ", ".join(undeclared_workflows), "every GitHub workflow must be declared in tooling.workflowFiles")

    model_path_rel = routes_manifest.get("modelProfileFile")
    if isinstance(model_path_rel, str):
        model_path = safe_path(root, model_path_rel, entity="routes.modelProfileFile", base=shared_root, must_exist=True)
        expected.add(model_path)
        descriptor = load_json(model_path, root=root)
        require_positive_schema(descriptor, file=Path(relative(root, model_path)))
        for _, resource_rel in _iter_declared_paths(descriptor):
            resource_path = safe_path(root, resource_rel, entity="model.resource", base=shared_root, must_exist=True)
            expected.add(resource_path)

    for profile_rel in routes_manifest.get("profiles", {}).values():
        expected.add(safe_path(root, profile_rel, entity="routes.profile", base=shared_root, must_exist=True))
    for rel in routes_manifest.get("alwaysFiles", []):
        expected.add(safe_path(root, rel, entity="routes.alwaysFiles", base=shared_root, must_exist=True))
    for route_id in routes:
        _, files = expand_route(routes, route_id)
        for rel in files:
            expected.add(safe_path(root, rel, entity=f"route:{route_id}.file", base=shared_root, must_exist=True))

    repository_readmes = [path for path in root.rglob("README.md") if path.is_file() and ".git" not in path.parts]
    if repository_readmes != [root / "README.md"]:
        raise issue("README_COUNT", root, "README.md", [relative(root, path) for path in repository_readmes], "exactly one root README.md required")
    expected.add(root / "README.md")

    scripts_root = safe_path(root, tooling.get("scriptsRoot", "scripts"), entity="tooling.scriptsRoot", must_exist=True)
    for script in scripts_root.rglob("*.py"):
        if "__pycache__" not in script.parts:
            expected.add(script.resolve())
    tests_rel = tooling.get("testsRoot", "tests")
    tests_root = safe_path(root, tests_rel, entity="tooling.testsRoot")
    if tests_root.exists():
        for test in tests_root.rglob("*.py"):
            if "__pycache__" not in test.parts:
                expected.add(test.resolve())

    for rel in tooling.get("declaredFiles", []):
        expected.add(safe_path(root, rel, entity="tooling.declaredFiles", must_exist=True))

    inventory_collections = tooling.get("inventoryCollections", [])
    if not isinstance(inventory_collections, list) or any(not isinstance(name, str) or not name for name in inventory_collections):
        raise issue("INVALID_INVENTORY_COLLECTIONS", anchors.tooling, "inventoryCollections", inventory_collections, "string array required")
    for collection in inventory_collections:
        collection_root = safe_path(root, collection, entity="tooling.inventoryCollections", base=shared_root)
        if not collection_root.exists():
            continue
        if not collection_root.is_dir():
            raise issue("INVALID_INVENTORY_COLLECTION", relative(root, collection_root), collection, collection_root, "collection must be a directory")
        for resource in collection_root.rglob("*"):
            if resource.is_file() and "__pycache__" not in resource.parts:
                expected.add(resource.resolve())

    return RepositoryModel(
        root=root,
        anchors=anchors,
        registry=registry,
        routes_manifest=routes_manifest,
        source_index=source_index,
        tooling=tooling,
        skills_by_id=skills_by_id,
        skill_order=skill_order,
        cross_cutting_ids=list(cross_cutting),
        expected_files=expected,
        sections=sections,
        source_manifests=source_manifests,
        canonical_sources=canonical_sources,
    )


def actual_repository_files(model: RepositoryModel) -> set[Path]:
    excluded_dirs = {".git", "__pycache__", ".pytest_cache"}
    configured = set(model.tooling.get("ignoredDirectories", ["dist"]))
    result: set[Path] = set()
    integrity_path = safe_path(model.root, model.tooling.get("integrityFile", "shared/manifests/integrity.json"), entity="tooling.integrityFile")
    for path in model.root.rglob("*"):
        if not path.is_file() or any(part in excluded_dirs | configured for part in path.parts):
            continue
        resolved = path.resolve()
        if resolved == integrity_path.resolve(strict=False):
            continue
        result.add(resolved)
    return result


def validate_inventory(model: RepositoryModel) -> None:
    actual = actual_repository_files(model)
    missing = sorted(relative(model.root, path) for path in model.expected_files - actual)
    extra = sorted(relative(model.root, path) for path in actual - model.expected_files)
    if missing:
        raise issue("INVENTORY_MISSING", model.root, "inventory", ", ".join(missing), "all registered or referenced files must exist")
    if extra:
        raise issue("INVENTORY_EXTRA", model.root, "inventory", ", ".join(extra), "files must be registered, referenced, or conventionally discovered")


def dependency_closure(model: RepositoryModel, roots: Sequence[str]) -> list[str]:
    unknown = [skill_id for skill_id in roots if skill_id not in model.skills_by_id]
    if unknown:
        raise issue("UNKNOWN_SKILL", model.anchors.registry, "skills", ", ".join(unknown), "all selected skills must be registered")
    selected: set[str] = set()

    def add(skill_id: str) -> None:
        if skill_id in selected:
            return
        for dependency in model.skills_by_id[skill_id].get("dependencies", []):
            add(dependency)
        selected.add(skill_id)

    for skill_id in roots:
        add(skill_id)
    return [skill_id for skill_id in model.skill_order if skill_id in selected]


def select_skills(
    model: RepositoryModel,
    *,
    skills: Sequence[str] | None = None,
    include: Sequence[str] = (),
    exclude: Sequence[str] = (),
) -> list[str]:
    roots = list(skills) if skills is not None else list(model.skill_order)
    roots.extend(include)
    roots = list(dict.fromkeys(roots))
    selected = dependency_closure(model, roots)
    unknown_excludes = [skill_id for skill_id in exclude if skill_id not in model.skills_by_id]
    if unknown_excludes:
        raise issue("UNKNOWN_SKILL", model.anchors.registry, "exclude", ", ".join(unknown_excludes), "excluded skills must be registered")
    excluded = set(exclude)
    remaining = [skill_id for skill_id in selected if skill_id not in excluded]
    remaining_set = set(remaining)
    for skill_id in remaining:
        blocked = set(model.skills_by_id[skill_id].get("dependencies", [])) - remaining_set
        if blocked:
            raise issue("EXCLUDED_DEPENDENCY", model.anchors.registry, skill_id, ", ".join(sorted(blocked)), "cannot exclude a dependency of a selected skill")
    return remaining


def compiled_bytes(model: RepositoryModel, selected: Sequence[str]) -> bytes:
    chunks: list[bytes] = []
    emitted_files: set[Path] = set()
    emitted_sections: set[str] = set()

    def emit_file(path: Path) -> None:
        resolved = path.resolve()
        if resolved not in emitted_files:
            chunks.append(resolved.read_bytes().rstrip(b"\n") + b"\n\n")
            emitted_files.add(resolved)

    emit_file(safe_path(model.root, model.anchors.root_skill, entity="rootSkill", must_exist=True))
    emit_file(safe_path(model.root, model.anchors.orchestrator, entity="orchestrator", must_exist=True))
    for rel in model.routes_manifest.get("alwaysFiles", []):
        emit_file(safe_path(model.root, rel, entity="routes.alwaysFiles", base=model.shared_root, must_exist=True))
    for skill_id in selected:
        item = model.skills_by_id[skill_id]
        emit_file(safe_path(model.root, item["skillFile"], entity=f"skill:{skill_id}", must_exist=True))
        for resource in item.get("resources", []) + item.get("referenceFiles", []):
            rel = resource.get("path") if isinstance(resource, dict) else resource
            emit_file(safe_path(model.root, rel, entity=f"skill:{skill_id}.resource", must_exist=True))
        for route_id in item.get("requiredRoutes", []):
            section_ids, files = expand_route(model.routes_manifest["routes"], route_id)
            for rel in files:
                emit_file(safe_path(model.root, rel, entity=f"route:{route_id}.file", base=model.shared_root, must_exist=True))
            for section_id in section_ids:
                if section_id in emitted_sections:
                    continue
                section = model.sections.get(section_id)
                if section is None:
                    raise issue("UNKNOWN_SECTION", "shared/manifests/routes.json", route_id, section_id, "route section must exist in source manifests")
                chunks.append(section.data.rstrip(b"\n") + b"\n\n")
                emitted_sections.add(section_id)
    return b"".join(chunks).rstrip() + b"\n"


def _validate_output_file(model: RepositoryModel, output: Path) -> Path:
    output = output.expanduser().resolve(strict=False)
    root = model.root.resolve(strict=True)
    if output == root or output.is_dir():
        raise issue("UNSAFE_OUTPUT", output, "output", output, "compiled output must be a file and must not equal repository root")
    if any(output == path.resolve(strict=False) for path in model.expected_files):
        raise issue("UNSAFE_OUTPUT", output, "output", output, "compiled output must not overwrite a source input")
    if root in output.parents:
        relative_output = output.relative_to(root)
        ignored = set(model.tooling.get("ignoredDirectories", ["dist"]))
        if not relative_output.parts or relative_output.parts[0] not in ignored:
            raise issue("UNSAFE_OUTPUT", relative_output, "output", output, f"in-repository outputs must be inside one of {sorted(ignored)}")
    return output


def build_compiled(
    model: RepositoryModel,
    output: Path,
    *,
    skills: Sequence[str] | None = None,
    include: Sequence[str] = (),
    exclude: Sequence[str] = (),
) -> list[str]:
    selected = select_skills(model, skills=skills, include=include, exclude=exclude)
    output = _validate_output_file(model, output)
    atomic_write(output, compiled_bytes(model, selected))
    return selected


def _safe_output_directory(model: RepositoryModel, output: Path) -> Path:
    output = output.expanduser().resolve(strict=False)
    root = model.root.resolve(strict=True)
    if output == root:
        raise issue("UNSAFE_OUTPUT", output, "output", output, "output must not equal repository root")
    for source in model.expected_files:
        resolved = source.resolve(strict=False)
        if output == resolved or output in resolved.parents:
            raise issue("UNSAFE_OUTPUT", output, "output", output, "output must not contain source inputs")
    if root in output.parents:
        relative_output = output.relative_to(root)
        ignored = set(model.tooling.get("ignoredDirectories", ["dist"]))
        if not relative_output.parts or relative_output.parts[0] not in ignored:
            raise issue("UNSAFE_OUTPUT", relative_output, "output", output, f"in-repository outputs must be inside one of {sorted(ignored)}")
    if output.is_symlink() or (output.exists() and not output.is_dir()):
        raise issue("UNSAFE_OUTPUT", output, "output", output, "flat output must be a real directory")
    return output


def _bundle(paths: Sequence[Path]) -> bytes:
    return b"".join(path.read_bytes().rstrip(b"\n") + b"\n\n" for path in paths).rstrip() + b"\n"


def flat_outputs(model: RepositoryModel) -> dict[str, bytes]:
    outputs: dict[str, bytes] = {}
    labels: set[str] = set()
    position = 0

    def add(label: str, data: bytes, suffix: str = ".md") -> None:
        nonlocal position
        normalized = f"{label}{suffix}"
        if normalized in labels:
            raise issue("OUTPUT_COLLISION", "flat-build", "output", normalized, "generated output labels must be unique before numbering")
        labels.add(normalized)
        name = f"{position:02d}-{label}{suffix}"
        outputs[name] = data
        position += 1

    add("MAIN", safe_path(model.root, model.anchors.root_skill, entity="rootSkill", must_exist=True).read_bytes())
    add("ORCHESTRATOR", safe_path(model.root, model.anchors.orchestrator, entity="orchestrator", must_exist=True).read_bytes())
    domain = [skill_id for skill_id in model.skill_order if skill_id not in model.cross_cutting_ids]
    for skill_id in domain:
        add(f"SKILL-{skill_id.upper()}", safe_path(model.root, model.skills_by_id[skill_id]["skillFile"], entity=skill_id, must_exist=True).read_bytes())
    cross_paths = [safe_path(model.root, model.skills_by_id[skill_id]["skillFile"], entity=skill_id, must_exist=True) for skill_id in model.cross_cutting_ids]
    add("SKILLS-CROSS-CUTTING", _bundle(cross_paths))

    groups = model.tooling.get("flatBuild", {}).get("groups", [])
    assigned: set[Path] = set()
    for group in groups:
        if not isinstance(group, dict):
            raise issue("INVALID_FLAT_GROUP", model.anchors.tooling, "flatBuild.groups", group, "group object required")
        label = group.get("name")
        collections = group.get("collections", [])
        mode = group.get("mode", "bundle")
        paths_set: set[Path] = set()
        for rel in group.get("rootFiles", []):
            paths_set.add(safe_path(model.root, rel, entity=f"flat-group:{label}.rootFiles", must_exist=True))
        for path in model.expected_files:
            if not path.is_file() or path in assigned:
                continue
            try:
                shared_relative = path.relative_to(model.shared_root)
            except ValueError:
                continue
            if len(shared_relative.parts) > 1 and shared_relative.parts[0] in collections:
                paths_set.add(path)
        paths = sorted(paths_set, key=lambda path: relative(model.root, path))
        if not paths:
            continue
        assigned.update(paths)
        if mode == "individual":
            for path in paths:
                add(f"{label}-{path.stem.upper()}", path.read_bytes())
        else:
            add(label, _bundle(paths))

    instruction = model.tooling.get("flatBuild", {}).get("instructionText", "")
    if instruction:
        add("PROJECT-INSTRUCTIONS", instruction.rstrip().encode("utf-8") + b"\n", suffix=".txt")
    max_files = model.tooling.get("flatBuild", {}).get("maxFiles")
    if not isinstance(max_files, int) or max_files < 1:
        raise issue("INVALID_POLICY", model.anchors.tooling, "flatBuild.maxFiles", max_files, "positive integer policy required")
    if len(outputs) > max_files:
        raise issue("FLAT_FILE_LIMIT", "flat-build", "files", len(outputs), f"must not exceed configured limit {max_files}")
    return outputs


def build_flat(model: RepositoryModel, output: Path) -> dict[str, str]:
    output = _safe_output_directory(model, output)
    rendered = flat_outputs(model)
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = Path(tempfile.mkdtemp(prefix=f".{output.name}.new.", dir=output.parent))
    backup = output.parent / f".{output.name}.old.{os.getpid()}"
    replaced_existing = False
    try:
        for name, data in rendered.items():
            atomic_write(temporary / name, data)
        if backup.exists():
            shutil.rmtree(backup)
        if output.exists():
            os.replace(output, backup)
            replaced_existing = True
        os.replace(temporary, output)
        if replaced_existing:
            shutil.rmtree(backup)
    except Exception:
        if output.exists() and replaced_existing:
            shutil.rmtree(output)
        if replaced_existing and backup.exists():
            os.replace(backup, output)
        raise
    finally:
        if temporary.exists():
            shutil.rmtree(temporary)
        if backup.exists() and output.exists():
            shutil.rmtree(backup)
    return {name: sha256_bytes(data) for name, data in rendered.items()}


def catalog_entry_count(path: Path, begin: bytes = b"<!-- VERBATIM_CATALOG_BEGIN -->\n", end: bytes = b"<!-- VERBATIM_CATALOG_END -->\n") -> tuple[int, str]:
    data = path.read_bytes()
    try:
        payload = data[data.index(begin) + len(begin): data.index(end)].rstrip(b"\n")
    except ValueError as exc:
        raise issue("CATALOG_MARKERS", path, "catalog", path.name, "verbatim begin/end markers required") from exc
    try:
        text = payload.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise issue("CATALOG_ENCODING", path, "catalog", path.name, "UTF-8 catalog payload required") from exc
    entries = [part for part in text.split("\n\n") if part.strip()]
    return len(entries), sha256_bytes(payload)


def derive_integrity(model: RepositoryModel) -> dict[str, Any]:
    validate_inventory(model)
    inventory = sorted(relative(model.root, path) for path in model.expected_files)
    eval_counts: dict[str, int] = {}
    catalog_counts: dict[str, dict[str, Any]] = {}
    for path in sorted(model.expected_files, key=lambda item: relative(model.root, item)):
        rel = relative(model.root, path)
        if "/evals/" in f"/{rel}" and path.suffix == ".json":
            document = load_json(path, root=model.root)
            cases = document.get("cases", [])
            if isinstance(cases, list):
                eval_counts[rel] = len(cases)
        if "/catalogs/" in f"/{rel}" and path.suffix == ".md":
            count, payload_hash = catalog_entry_count(path)
            catalog_counts[rel] = {"entries": count, "payloadSha256": payload_hash}
    files = []
    integrity_rel = model.tooling.get("integrityFile", "shared/manifests/integrity.json")
    for path in sorted(model.expected_files, key=lambda item: relative(model.root, item)):
        data = path.read_bytes()
        files.append({"path": relative(model.root, path), "sha256": sha256_bytes(data), "bytes": len(data)})
    return {
        "schemaVersion": model.tooling.get("integritySchemaVersion", 1),
        "generatedBy": "scripts/tooling.py refresh-integrity",
        "selfExcluded": integrity_rel,
        "counts": {
            "registeredSkills": len(model.skill_order),
            "crossCuttingSkills": len(model.cross_cutting_ids),
            "canonicalSources": len(model.canonical_sources),
            "sourceManifests": len(model.source_manifests),
            "evalCases": eval_counts,
            "catalogs": catalog_counts,
            "flatOutputs": len(flat_outputs(model)),
        },
        "inventory": {
            "count": len(inventory),
            "sha256": sha256_bytes(("\n".join(inventory) + "\n").encode("utf-8")),
            "files": files,
        },
        "policy": {
            "flatMaxFiles": model.tooling.get("flatBuild", {}).get("maxFiles"),
        },
    }


def verify_integrity(model: RepositoryModel, override: bytes | None = None) -> None:
    path = safe_path(model.root, model.tooling.get("integrityFile", "shared/manifests/integrity.json"), entity="tooling.integrityFile", must_exist=override is None)
    expected = derive_integrity(model)
    expected_bytes = (json.dumps(expected, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
    actual = override if override is not None else path.read_bytes()
    if actual != expected_bytes:
        raise issue("INTEGRITY_STALE", relative(model.root, path), "integrity", sha256_bytes(actual), f"expected {sha256_bytes(expected_bytes)}; run refresh-integrity")


def refresh_integrity(model: RepositoryModel, *, write: bool = True) -> tuple[bool, bytes]:
    document = derive_integrity(model)
    data = (json.dumps(document, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
    path = safe_path(model.root, model.tooling.get("integrityFile", "shared/manifests/integrity.json"), entity="tooling.integrityFile")
    changed = not path.is_file() or path.read_bytes() != data
    if write and changed:
        atomic_write(path, data)
    return changed, data


def validate_model_descriptor(model: RepositoryModel) -> dict[str, Any]:
    descriptor_rel = model.routes_manifest.get("modelProfileFile")
    descriptor_path = safe_path(model.root, descriptor_rel, entity="routes.modelProfileFile", base=model.shared_root, must_exist=True)
    descriptor = load_json(descriptor_path, root=model.root)
    require_positive_schema(descriptor, file=Path(relative(model.root, descriptor_path)))
    model_id = descriptor.get("id")
    if not isinstance(model_id, str) or not model_id:
        raise issue("INVALID_MODEL_ID", relative(model.root, descriptor_path), "id", model_id, "non-empty model ID required")
    resources: list[tuple[str, Path]] = []
    for key, rel in _iter_declared_paths(descriptor):
        if key.lower().endswith("file"):
            resources.append((key, safe_path(model.root, rel, entity=f"model.{key}", base=model.shared_root, must_exist=True)))
    if not resources:
        raise issue("MODEL_RESOURCES", relative(model.root, descriptor_path), "resources", resources, "descriptor must declare linked resource files")
    integrity = descriptor.get("integrity", {})
    if not isinstance(integrity, dict):
        raise issue("MODEL_INTEGRITY", relative(model.root, descriptor_path), "integrity", integrity, "integrity object required")
    expected_hash_keys: set[str] = set()
    for key, path in resources:
        hash_key = key[:-4] + "Sha256" if key.endswith("File") else key + "Sha256"
        expected_hash_keys.add(hash_key)
        if hash_key not in integrity:
            raise issue("MODEL_RESOURCE_HASH_MISSING", relative(model.root, descriptor_path), hash_key, None, "every linked model resource must have a declared SHA-256")
        actual_hash = sha256_file(path)
        if integrity[hash_key] != actual_hash:
            raise issue("MODEL_RESOURCE_HASH", relative(model.root, descriptor_path), hash_key, integrity[hash_key], actual_hash)
    orphan_hashes = sorted(key for key in integrity if key.endswith("Sha256") and key not in expected_hash_keys)
    if orphan_hashes:
        raise issue("MODEL_ORPHAN_HASH", relative(model.root, descriptor_path), "integrity", ", ".join(orphan_hashes), "integrity hashes must correspond to linked resources")
    prompt = descriptor.get("prompt", {})
    structure = prompt.get("structure") if isinstance(prompt, dict) else None
    if not isinstance(structure, list) or not structure or len(structure) != len(set(structure)) or any(not isinstance(item, str) or not item for item in structure):
        raise issue("MODEL_PROMPT_STRUCTURE", relative(model.root, descriptor_path), "prompt.structure", structure, "non-empty unique string array required")
    eval_path = next((path for key, path in resources if "eval" in key.lower()), None)
    if eval_path:
        evals = load_json(eval_path, root=model.root)
        cases = evals.get("cases", [])
        ids = [case.get("id") for case in cases if isinstance(case, dict)] if isinstance(cases, list) else []
        minimum = descriptor.get("validation", {}).get("minimumEvalCases", 1)
        if not isinstance(minimum, int) or minimum < 1:
            raise issue("MODEL_EVAL_POLICY", relative(model.root, descriptor_path), "validation.minimumEvalCases", minimum, "positive integer required")
        if len(ids) < minimum or len(ids) != len(set(ids)) or any(not isinstance(value, str) or not value for value in ids):
            raise issue("MODEL_EVALS", relative(model.root, eval_path), "cases", len(ids), f"at least {minimum} unique non-empty IDs required")
        validation = descriptor.get("validation", {})
        required_fields = validation.get("evalRequiredFields", ["id"])
        non_empty_arrays = validation.get("evalNonEmptyArrayFields", [])
        if not isinstance(required_fields, list) or any(not isinstance(field, str) or not field for field in required_fields):
            raise issue("MODEL_EVAL_POLICY", relative(model.root, descriptor_path), "validation.evalRequiredFields", required_fields, "string array required")
        if not isinstance(non_empty_arrays, list) or any(not isinstance(field, str) or not field for field in non_empty_arrays):
            raise issue("MODEL_EVAL_POLICY", relative(model.root, descriptor_path), "validation.evalNonEmptyArrayFields", non_empty_arrays, "string array required")
        for position, case in enumerate(cases):
            if not isinstance(case, dict):
                raise issue("MODEL_EVAL_CASE", relative(model.root, eval_path), f"cases[{position}]", case, "evaluation case must be an object")
            missing = [field for field in required_fields if field not in case or case[field] in (None, "", [])]
            if missing:
                raise issue("MODEL_EVAL_CASE", relative(model.root, eval_path), case.get("id", position), ", ".join(missing), "required evaluation fields must be non-empty")
            for field in non_empty_arrays:
                value = case.get(field)
                if not isinstance(value, list) or not value:
                    raise issue("MODEL_EVAL_CASE", relative(model.root, eval_path), case.get("id", position), field, "configured array field must be non-empty")
        for identity_key in ("model", "modelId", "modelProfile"):
            if identity_key in evals and evals[identity_key] != model_id:
                raise issue("MODEL_EVAL_ID_MISMATCH", relative(model.root, eval_path), identity_key, evals[identity_key], model_id)
    return {"model": model_id, "resources": len(resources)}


def discover_tasks(model: RepositoryModel, kind: str) -> list[Path]:
    pattern = _TASK_PATTERNS.get(kind)
    if pattern is None:
        raise issue("UNKNOWN_TASK_KIND", model.anchors.tooling, "task-kind", kind, f"expected one of {sorted(_TASK_PATTERNS)}")
    scripts_root = safe_path(model.root, model.tooling.get("scriptsRoot", "scripts"), entity="tooling.scriptsRoot", must_exist=True)
    excluded = {"tooling.py"}
    tasks = [path for path in scripts_root.iterdir() if path.is_file() and path.name not in excluded and not path.name.startswith("_") and pattern.fullmatch(path.name)]
    return sorted(tasks, key=lambda path: path.name)


def run_process(arguments: Sequence[str], *, cwd: Path, env: Mapping[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        list(arguments),
        cwd=cwd,
        env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1", **(dict(env) if env else {})),
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=False,
    )


def run_tasks(model: RepositoryModel, kind: str, *, selected: Sequence[str] | None = None, output_base: Path | None = None) -> list[dict[str, Any]]:
    tasks = discover_tasks(model, kind)
    by_stem = {path.stem: path for path in tasks}
    if selected:
        unknown = [name for name in selected if name not in by_stem]
        if unknown:
            raise issue("UNKNOWN_TASK", model.tooling.get("scriptsRoot", "scripts"), kind, ", ".join(unknown), f"known tasks: {', '.join(sorted(by_stem))}")
        tasks = [by_stem[name] for name in selected]
    results: list[dict[str, Any]] = []
    for task in tasks:
        command = [os.fspath(Path(os.sys.executable)), os.fspath(task)]
        output: Path | None = None
        if kind == "build" and output_base is not None:
            output = output_base / task.stem
            command += ["--output", os.fspath(output)]
        result = run_process(command, cwd=model.root)
        record = {
            "task": task.stem,
            "command": command,
            "exitCode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
        }
        if output is not None and output.exists():
            record["output"] = os.fspath(output)
            record["sha256"] = tree_hash(output)
        results.append(record)
        if result.returncode:
            raise issue("TASK_FAILED", relative(model.root, task), task.stem, result.returncode, (result.stdout + result.stderr).strip())
    return results


def tree_hash(path: Path) -> str:
    if path.is_file():
        return sha256_file(path)
    digest = hashlib.sha256()
    for child in sorted((item for item in path.rglob("*") if item.is_file()), key=lambda item: item.relative_to(path).as_posix()):
        digest.update(child.relative_to(path).as_posix().encode("utf-8") + b"\0")
        digest.update(child.read_bytes())
    return digest.hexdigest()


def git(model: RepositoryModel, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    command = ["git", "-C", os.fspath(model.root), *args]
    result = run_process(command, cwd=model.root)
    if check and result.returncode:
        raise issue("GIT_FAILED", model.root, "git", " ".join(command), (result.stdout + result.stderr).strip())
    return result


@dataclass(frozen=True)
class GitHubRemote:
    name: str
    fetch_url: str
    push_url: str
    owner: str
    repository: str

    @property
    def full_name(self) -> str:
        return f"{self.owner}/{self.repository}"


def sanitize_remote_url(value: str) -> str:
    text = value.strip()
    text = re.sub(
        r"(?i)\b(?:ghp|github_pat|gho|ghu|ghs|ghr)_[A-Za-z0-9_]+",
        "***",
        text,
    )
    scp = re.fullmatch(r"([^@/:\s]+)@([^:/\s]+):(.+)", text)
    if scp:
        return f"{scp.group(1)}@{scp.group(2)}:{scp.group(3)}"
    try:
        parsed = urlsplit(text)
    except ValueError:
        return text
    if not parsed.scheme or not parsed.netloc:
        return text
    host = parsed.hostname or ""
    if parsed.port:
        host = f"{host}:{parsed.port}"
    userinfo = "***@" if parsed.username is not None or parsed.password is not None else ""
    return urlunsplit((parsed.scheme, userinfo + host, parsed.path, parsed.query, parsed.fragment))


def parse_github_remote_url(value: str) -> tuple[str, str]:
    raw = value.strip()
    scp = re.fullmatch(r"([^@/:\s]+)@([^:/\s]+):(.+)", raw)
    if scp:
        host = scp.group(2).lower()
        repository_path = scp.group(3)
    else:
        try:
            parsed = urlsplit(raw)
        except ValueError as exc:
            raise issue("INVALID_REMOTE_URL", "git-config", "remote-url", sanitize_remote_url(raw), "valid GitHub HTTPS or SSH URL required") from exc
        if parsed.scheme.lower() not in {"http", "https", "ssh"}:
            raise issue("UNSUPPORTED_REMOTE_URL", "git-config", "remote-url", sanitize_remote_url(raw), "GitHub HTTPS or SSH URL required")
        host = (parsed.hostname or "").lower()
        repository_path = parsed.path.lstrip("/")
    if host != "github.com":
        raise issue("REMOTE_NOT_GITHUB", "git-config", "remote-host", host or sanitize_remote_url(raw), "remote host must be github.com")
    repository_path = repository_path.rstrip("/")
    if repository_path.endswith(".git"):
        repository_path = repository_path[:-4]
    parts = repository_path.split("/")
    if len(parts) != 2 or not all(parts):
        raise issue("INVALID_GITHUB_REMOTE", "git-config", "remote-path", sanitize_remote_url(raw), "GitHub remote path must be owner/repository")
    if not all(re.fullmatch(r"[A-Za-z0-9_.-]+", part) for part in parts):
        raise issue("INVALID_GITHUB_REMOTE", "git-config", "remote-path", sanitize_remote_url(raw), "owner and repository contain unsupported characters")
    return parts[0], parts[1]


def resolve_github_remote(model: RepositoryModel, name: str) -> GitHubRemote:
    if not name or not re.fullmatch(r"[A-Za-z0-9_.-]+", name):
        raise issue("INVALID_REMOTE_NAME", model.root, "remote", name, "configured remote name required")
    configured = set(git(model, "remote").stdout.splitlines())
    if name not in configured:
        raise issue("REMOTE_NOT_CONFIGURED", model.root, "remote", name, "configure the selected remote before publication")
    fetch_result = git(model, "config", "--get-all", f"remote.{name}.url", check=False)
    push_result = git(model, "config", "--get-all", f"remote.{name}.pushurl", check=False)
    if fetch_result.returncode or not fetch_result.stdout.strip():
        raise issue("REMOTE_URL_MISSING", model.root, "remote", name, "remote fetch URL must be configured")
    fetch_url = fetch_result.stdout.strip().splitlines()[0]
    push_url = push_result.stdout.strip().splitlines()[0] if not push_result.returncode and push_result.stdout.strip() else fetch_url
    fetch_identity = parse_github_remote_url(fetch_url)
    push_identity = parse_github_remote_url(push_url)
    if tuple(part.lower() for part in fetch_identity) != tuple(part.lower() for part in push_identity):
        raise issue(
            "REMOTE_IDENTITY_MISMATCH",
            model.root,
            "remote",
            f"fetch={sanitize_remote_url(fetch_url)} push={sanitize_remote_url(push_url)}",
            "fetch and push URLs must identify the same GitHub repository",
        )
    return GitHubRemote(name=name, fetch_url=fetch_url, push_url=push_url, owner=fetch_identity[0], repository=fetch_identity[1])


def _classify_remote_failure(output: str, *, default: str) -> str:
    lowered = output.lower()
    if any(marker in lowered for marker in ("could not resolve host", "network is unreachable", "failed to connect", "connection timed out", "operation timed out")):
        return "NETWORK_UNAVAILABLE"
    if any(marker in lowered for marker in ("authentication failed", "could not read username", "terminal prompts disabled", "permission denied", "repository not found")):
        return "LOCAL_GIT_AUTH_UNAVAILABLE"
    return default


def remote_git(model: RepositoryModel, *args: str, error_code: str = "REMOTE_GIT_FAILED") -> subprocess.CompletedProcess[str]:
    command = ["git", "-C", os.fspath(model.root), *args]
    result = run_process(command, cwd=model.root, env={"GIT_TERMINAL_PROMPT": "0"})
    if result.returncode:
        output = sanitize_remote_url((result.stdout + result.stderr).strip())
        code = _classify_remote_failure(output, default=error_code)
        safe_command = " ".join(sanitize_remote_url(part) for part in command)
        raise issue(code, model.root, "git-network", safe_command, output or "remote Git command failed")
    return result


def _parse_ls_remote_heads(output: str, expected_ref: str) -> str | None:
    matches: list[str] = []
    for line in output.splitlines():
        fields = line.split("\t")
        if len(fields) == 2 and fields[1] == expected_ref and re.fullmatch(r"[0-9a-f]{40}", fields[0]):
            matches.append(fields[0])
    if not matches:
        return None
    if len(set(matches)) != 1:
        raise issue("REMOTE_REF_AMBIGUOUS", "remote", expected_ref, matches, "remote ref must resolve to one SHA")
    return matches[0]


def remote_ref_sha(model: RepositoryModel, remote: str, ref: str) -> str | None:
    result = remote_git(model, "ls-remote", "--heads", remote, ref, error_code="REMOTE_READ_FAILED")
    return _parse_ls_remote_heads(result.stdout, ref)


def resolve_remote_default_branch(model: RepositoryModel, remote: str, *, explicit: str | None = None) -> tuple[str, str]:
    local_ref = git(model, "symbolic-ref", "--quiet", "--short", f"refs/remotes/{remote}/HEAD", check=False)
    if not local_ref.returncode and local_ref.stdout.strip().startswith(f"{remote}/"):
        branch = local_ref.stdout.strip()[len(remote) + 1 :]
        if branch:
            return branch, "remote-tracking-head"
    symref = remote_git(model, "ls-remote", "--symref", remote, "HEAD", error_code="REMOTE_READ_FAILED")
    for line in symref.stdout.splitlines():
        match = re.fullmatch(r"ref:\s+refs/heads/(.+)\tHEAD", line)
        if match and match.group(1):
            return match.group(1), "ls-remote-symref"
    if explicit:
        check = git(model, "check-ref-format", "--branch", explicit, check=False)
        if check.returncode:
            raise issue("INVALID_DEFAULT_BRANCH", model.root, "default-branch", explicit, "valid branch name required")
        return explicit, "explicit"
    raise issue("DEFAULT_BRANCH_UNRESOLVED", model.root, "remote-head", remote, "remote default branch must resolve without ambiguity")


def _publication_cleanliness(model: RepositoryModel) -> None:
    entries = porcelain_status(model, include_untracked=True)
    index_dirty = [entry["path"] for entry in entries if entry["status"] != "??" and entry["status"][0] != " "]
    worktree_dirty = [entry["path"] for entry in entries if entry["status"] == "??" or entry["status"][1] != " "]
    if index_dirty:
        raise issue("INDEX_DIRTY", model.root, "index", ", ".join(index_dirty), "publication requires a clean index")
    if worktree_dirty:
        raise issue("WORKTREE_DIRTY", model.root, "working-tree", ", ".join(worktree_dirty), "publication requires a clean working tree including untracked files")


def _set_upstream_config(model: RepositoryModel, *, branch: str, remote: str, remote_branch: str) -> None:
    git(model, "config", f"branch.{branch}.remote", remote)
    git(model, "config", f"branch.{branch}.merge", f"refs/heads/{remote_branch}")


def publish_branch(
    model: RepositoryModel,
    *,
    remote: str = "origin",
    branch: str | None = None,
    dry_run: bool = False,
    set_upstream: bool = True,
    fetch: bool = True,
    expected_base: str | None = None,
    default_branch: str | None = None,
    prospective_commit: bool = False,
) -> dict[str, Any]:
    preflight = git_preflight(model)
    if not prospective_commit:
        _publication_cleanliness(model)
    remote_info = resolve_github_remote(model, remote)
    current_branch = preflight["branch"]
    target_branch = branch or current_branch
    branch_check = git(model, "check-ref-format", "--branch", target_branch, check=False)
    if branch_check.returncode:
        raise issue("INVALID_PUBLISH_BRANCH", model.root, "branch", target_branch, "valid branch name required")
    resolved_default, default_source = resolve_remote_default_branch(model, remote, explicit=default_branch)
    if current_branch == resolved_default or target_branch == resolved_default:
        raise issue("DEFAULT_BRANCH_PROTECTED", model.root, "branch", target_branch, "publication to or from the remote default branch is prohibited")

    fetch_performed = False
    if fetch and not dry_run:
        remote_git(model, "fetch", "--prune", remote, error_code="REMOTE_FETCH_FAILED")
        fetch_performed = True

    default_ref = f"refs/heads/{resolved_default}"
    remote_base = remote_ref_sha(model, remote, default_ref)
    if remote_base is None:
        raise issue("REMOTE_DEFAULT_BRANCH_MISSING", model.root, "default-branch", resolved_default, "remote default branch must exist")
    if expected_base and remote_base != expected_base:
        raise issue("REMOTE_BASE_CHANGED", model.root, "remote-base", remote_base, f"expected {expected_base}")
    base_object = git(model, "cat-file", "-e", f"{remote_base}^{{commit}}", check=False)
    if base_object.returncode:
        raise issue("REMOTE_BASE_NOT_LOCAL", model.root, "remote-base", remote_base, "fetch the verified remote base before publication")

    local_sha = preflight["head"]
    ancestry = git(model, "merge-base", "--is-ancestor", remote_base, local_sha, check=False)
    if ancestry.returncode:
        raise issue("LOCAL_HISTORY_NOT_BASED_ON_REMOTE", model.root, "history", f"base={remote_base} head={local_sha}", "local branch must descend from the remote default branch")
    ahead = int(git(model, "rev-list", "--count", f"{remote_base}..{local_sha}").stdout.strip())
    behind = int(git(model, "rev-list", "--count", f"{local_sha}..{remote_base}").stdout.strip())
    required_ahead = 0 if prospective_commit else 1
    if ahead != required_ahead or behind != 0:
        rule = "pre-commit branch must equal remote base" if prospective_commit else "publishable branch must be exactly one commit ahead and zero behind"
        raise issue("LOCAL_HISTORY_UNEXPECTED", model.root, "history", f"ahead={ahead} behind={behind}", rule)

    target_ref = f"refs/heads/{target_branch}"
    remote_before = remote_ref_sha(model, remote, target_ref)
    if prospective_commit:
        if remote_before is not None:
            raise issue("REMOTE_BRANCH_COLLISION", model.root, "remote-branch", f"local=pending remote={remote_before}", "commit dry-run cannot prove idempotence against an existing remote branch")
        collision = "ABSENT"
    elif remote_before is None:
        collision = "ABSENT"
    elif remote_before == local_sha:
        collision = "EXACT"
    else:
        raise issue("REMOTE_BRANCH_DIVERGED", model.root, "remote-branch", f"local={local_sha} remote={remote_before}", "refuse non-fast-forward or colliding publication")

    result: dict[str, Any] = {
        "status": "PASS",
        "command": "publish",
        "dryRun": dry_run,
        "remote": remote,
        "repository": remote_info.full_name,
        "remoteUrl": sanitize_remote_url(remote_info.push_url),
        "defaultBranch": resolved_default,
        "defaultBranchSource": default_source,
        "baseSha": remote_base,
        "branch": target_branch,
        "localSha": None if prospective_commit else local_sha,
        "preCommitHead": local_sha if prospective_commit else None,
        "aheadBy": 1 if prospective_commit else ahead,
        "behindBy": behind,
        "collision": collision,
        "remoteBefore": remote_before,
        "fetchPerformed": fetch_performed,
        "setUpstream": set_upstream,
        "force": False,
        "pushed": False,
        "idempotent": collision == "EXACT",
    }
    if dry_run or prospective_commit:
        result["wouldPush"] = collision == "ABSENT"
        return result
    if collision == "EXACT":
        if set_upstream:
            _set_upstream_config(model, branch=current_branch, remote=remote, remote_branch=target_branch)
        upstream = git(model, "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{upstream}", check=False)
        result["remoteAfter"] = remote_before
        result["upstream"] = upstream.stdout.strip() if not upstream.returncode else None
        return result

    push_args = ["push", "--porcelain"]
    if set_upstream:
        push_args.append("--set-upstream")
    push_args.extend([remote, f"HEAD:{target_ref}"])
    if any(argument in {"--force", "--force-with-lease", "--mirror", "--all", "--tags"} for argument in push_args):
        raise issue("UNSAFE_PUSH_ARGUMENT", model.root, "push", push_args, "force, mirror, all-branch, and tag publication are prohibited")
    push_result = remote_git(model, *push_args, error_code="REMOTE_PUSH_FAILED")
    remote_after = remote_ref_sha(model, remote, target_ref)
    if remote_after != local_sha:
        raise issue("REMOTE_PUSH_VERIFICATION_FAILED", model.root, "remote-branch", remote_after, f"expected {local_sha}")
    upstream = git(model, "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{upstream}", check=False)
    result.update(
        {
            "pushed": True,
            "remoteAfter": remote_after,
            "upstream": upstream.stdout.strip() if not upstream.returncode else None,
            "pushPorcelain": sanitize_remote_url(push_result.stdout.strip()),
        }
    )
    return result


@contextlib.contextmanager
def _exclusive_preflight_lock(root: Path) -> Iterator[None]:
    lock_root = Path(tempfile.gettempdir()) / "skills-tooling-locks"
    lock_root.mkdir(parents=True, exist_ok=True)
    key = sha256_bytes(os.fspath(root.resolve()).encode("utf-8"))[:24]
    lock_path = lock_root / f"{key}.lock"
    deadline = time.monotonic() + 30.0
    descriptor: int | None = None
    while descriptor is None:
        try:
            descriptor = os.open(lock_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
        except FileExistsError:
            if time.monotonic() >= deadline:
                raise issue("PREFLIGHT_LOCK_TIMEOUT", root, "ownership-lock", lock_path, "exclusive preflight lock must become available")
            time.sleep(0.05)
    try:
        os.write(descriptor, f"pid={os.getpid()}\nroot={root}\n".encode("utf-8"))
        yield
    finally:
        os.close(descriptor)
        lock_path.unlink(missing_ok=True)


def _normalize_repository_ownership(root: Path) -> dict[str, str]:
    resolved = root.resolve(strict=True)
    if resolved == Path(resolved.anchor) or not (resolved / ".git").exists():
        raise issue("GIT_REPOSITORY_REQUIRED", resolved, ".git", resolved / ".git", "safe canonical repository with .git required")
    if not hasattr(os, "geteuid"):
        if not os.access(resolved, os.R_OK | os.W_OK):
            raise issue("WORKSPACE_NOT_WRITABLE", resolved, "ownership", resolved, "repository must be readable and writable")
        return {"runtime": "non-posix", "owner": "current-user", "normalized": "not-applicable"}
    uid = os.geteuid()
    gid = os.getegid()
    if uid != 0:
        raise issue("ROOT_RUNTIME_REQUIRED", resolved, "runtime-uid", uid, "POSIX ownership normalization requires UID 0")
    with _exclusive_preflight_lock(resolved):
        for current, directories, files in os.walk(resolved, topdown=True, followlinks=False):
            current_path = Path(current)
            os.chown(current_path, uid, gid, follow_symlinks=False)
            for name in directories + files:
                path = current_path / name
                try:
                    os.chown(path, uid, gid, follow_symlinks=False)
                except FileNotFoundError:
                    continue
        root_stat = resolved.stat()
        git_stat = (resolved / ".git").stat()
        if (root_stat.st_uid, root_stat.st_gid) != (uid, gid) or (git_stat.st_uid, git_stat.st_gid) != (uid, gid):
            raise issue("LOCAL_GIT_OWNERSHIP_REPAIR_FAILED", resolved, "ownership", f"root={root_stat.st_uid}:{root_stat.st_gid};git={git_stat.st_uid}:{git_stat.st_gid}", f"expected {uid}:{gid}")
    return {"runtime": f"{uid}:{gid}", "owner": f"{uid}:{gid}", "normalized": "yes"}


def git_preflight(model: RepositoryModel) -> dict[str, str]:
    git_dir = model.root / ".git"
    if not git_dir.exists():
        raise issue("GIT_REPOSITORY_REQUIRED", model.root, ".git", git_dir, "local Git repository required")
    canonical_root = model.root.resolve(strict=True)
    if canonical_root not in _PREFLIGHTED_ROOTS:
        _normalize_repository_ownership(canonical_root)
        _PREFLIGHTED_ROOTS.add(canonical_root)
    if git(model, "rev-parse", "--is-inside-work-tree").stdout.strip() != "true":
        raise issue("GIT_WORKTREE_REQUIRED", model.root, "git", model.root, "must be a Git worktree")
    branch = git(model, "symbolic-ref", "--quiet", "--short", "HEAD", check=False)
    if branch.returncode or not branch.stdout.strip():
        raise issue("DETACHED_HEAD", model.root, "HEAD", "detached", "automatic commit requires an attached branch")
    git_dir_path = Path(git(model, "rev-parse", "--git-dir").stdout.strip())
    if not git_dir_path.is_absolute():
        git_dir_path = model.root / git_dir_path
    for marker in _GIT_OPERATIONS:
        if (git_dir_path / marker).exists():
            raise issue("GIT_OPERATION_IN_PROGRESS", relative(model.root, git_dir_path / marker), "git-operation", marker, "finish or abort the operation before automation")
    unmerged = git(model, "ls-files", "-u").stdout.splitlines()
    if unmerged:
        conflicts = sorted({line.split("\t", 1)[1] for line in unmerged if "\t" in line})
        raise issue("GIT_CONFLICTS", model.root, "conflicts", ", ".join(conflicts), "resolve conflicts before automation")
    return {"branch": branch.stdout.strip(), "head": git(model, "rev-parse", "HEAD").stdout.strip(), "ownershipPreflight": "verified"}


def porcelain_status(model: RepositoryModel, *, include_untracked: bool = True) -> list[dict[str, str]]:
    args = ["status", "--porcelain=v1", "-z"]
    if not include_untracked:
        args.append("--untracked-files=no")
    raw = git(model, *args).stdout
    entries: list[dict[str, str]] = []
    parts = raw.split("\0")
    index = 0
    while index < len(parts):
        record = parts[index]
        index += 1
        if not record:
            continue
        status = record[:2]
        path = record[3:]
        old = ""
        if "R" in status or "C" in status:
            if index < len(parts):
                old = path
                path = parts[index]
                index += 1
        entries.append({"status": status, "path": path, "oldPath": old})
    return entries


def _change_area(path: str) -> str:
    return path.split("/", 1)[0] if "/" in path else path


def _diff_stats(model: RepositoryModel, *, staged: bool, include_untracked: bool) -> dict[str, int]:
    arguments = ["diff", "--numstat"]
    if staged:
        arguments.append("--cached")
    else:
        arguments.append("HEAD")
    result = git(model, *arguments, check=False)
    additions = 0
    deletions = 0
    if result.returncode == 0:
        for line in result.stdout.splitlines():
            added, deleted, _, = (line.split("\t", 2) + ["", ""])[:3]
            if added.isdigit():
                additions += int(added)
            if deleted.isdigit():
                deletions += int(deleted)
    if include_untracked and not staged:
        for entry in porcelain_status(model, include_untracked=True):
            if entry["status"] != "??":
                continue
            path = safe_path(model.root, entry["path"], entity="git.untracked")
            if path.is_file():
                try:
                    additions += len(path.read_text(encoding="utf-8").splitlines())
                except UnicodeDecodeError:
                    additions += 0
    return {"additions": additions, "deletions": deletions}


def suggest_commit(model: RepositoryModel, *, staged: bool = False, include_untracked: bool = True) -> dict[str, Any]:
    entries = porcelain_status(model, include_untracked=include_untracked)
    if staged:
        entries = [entry for entry in entries if entry["status"][0] not in {" ", "?"}]
    if not entries:
        raise issue("NO_CHANGES", model.root, "git-status", "clean", "commit suggestion requires changes")
    paths = [entry["path"] for entry in entries]
    areas = sorted({_change_area(path) for path in paths})
    code = [path for path in paths if path.startswith("scripts/") or path.startswith("tests/")]
    manifests = [path for path in paths if "/manifests/" in f"/{path}" or path.endswith("registry.json")]
    docs = [path for path in paths if path.endswith(".md") and not path.startswith("scripts/")]
    ranked = sorted(
        [(len(code), "tooling"), (len(manifests), "manifests"), (len(docs), "documentation")],
        key=lambda item: (-item[0], item[1]),
    )
    dominant_count, dominant = ranked[0]
    tied = sum(count == dominant_count for count, _ in ranked) > 1
    if dominant == "tooling" and manifests and not tied:
        subject = "Make repository tooling manifest-driven"
    elif dominant == "tooling" and not tied:
        subject = "Strengthen repository tooling automation"
    elif dominant == "manifests" and not tied:
        subject = "Derive repository metadata from manifests"
    elif dominant == "documentation" and not tied:
        subject = "Update repository tooling documentation"
    elif code and manifests:
        subject = "Update repository tooling and metadata"
    else:
        subject = "Update repository configuration"
    subject = subject[:72].rstrip(" .")
    stats = _diff_stats(model, staged=staged, include_untracked=include_untracked)
    status_counts = {
        "added": sum(entry["status"] == "??" or "A" in entry["status"] for entry in entries),
        "modified": sum("M" in entry["status"] for entry in entries),
        "deleted": sum("D" in entry["status"] for entry in entries),
        "renamed": sum("R" in entry["status"] for entry in entries),
    }
    body_lines = [
        "Areas: " + ", ".join(areas),
        (
            f"Files: {len(entries)}; added {status_counts['added']}; modified {status_counts['modified']}; "
            f"deleted {status_counts['deleted']}; renamed {status_counts['renamed']}"
        ),
        f"Diff: +{stats['additions']} -{stats['deletions']}",
    ]
    return {
        "subject": subject,
        "body": "\n".join(body_lines),
        "files": entries,
        "areas": areas,
        "statistics": {**status_counts, **stats},
    }


def ensure_staged_paths_allowed(model: RepositoryModel) -> None:
    staged = git(model, "diff", "--cached", "--name-only", "--diff-filter=ACDMRTUXB").stdout.splitlines()
    prohibited = [path for path in staged if path.startswith(".github/workflows/")]
    if prohibited:
        raise issue("PROHIBITED_STAGING", model.root, "staged", ", ".join(prohibited), "GitHub workflows are prohibited")


def check_repository(model: RepositoryModel, *, integrity_override: bytes | None = None) -> dict[str, Any]:
    validate_inventory(model)
    verify_integrity(model, integrity_override)
    validate_model_descriptor(model)
    validation_results = run_tasks(model, "validate")
    with tempfile.TemporaryDirectory(prefix="skills-check-") as temporary:
        base = Path(temporary)
        first = base / "first"
        second = base / "second"
        first_results = run_tasks(model, "build", output_base=first)
        second_results = run_tasks(model, "build", output_base=second)
        first_hashes = {item["task"]: item.get("sha256") for item in first_results}
        second_hashes = {item["task"]: item.get("sha256") for item in second_results}
        if first_hashes != second_hashes:
            raise issue("NONDETERMINISTIC_BUILD", model.root, "builds", first_hashes, second_hashes)
    final_validation_results = run_tasks(model, "validate")
    return {
        "validators": [item["task"] for item in validation_results],
        "finalValidators": [item["task"] for item in final_validation_results],
        "builds": sorted(first_hashes),
        "hashes": first_hashes,
    }
