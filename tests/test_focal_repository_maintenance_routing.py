from __future__ import annotations

import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
ENTRYPOINT = ROOT / "prompts/focal-autonomous-development.md"
CONTROL_PLANE = ROOT / "prompts/focal/13-autonomy-control-plane-v4.md"
FLOWCHART = ROOT / "prompts/focal/11-process-flowchart.md"
TERMINAL = ROOT / "prompts/focal/08-terminal-report.md"


class RepositoryMaintenanceRoutingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.entry = ENTRYPOINT.read_text(encoding="utf-8")
        cls.control = CONTROL_PLANE.read_text(encoding="utf-8")
        cls.flowchart = FLOWCHART.read_text(encoding="utf-8")
        cls.terminal = TERMINAL.read_text(encoding="utf-8")

    def test_router_selects_administrative_mode_before_focal_cycle(self) -> None:
        router = self.entry.index("## Router de intención obligatorio")
        focal_gate = self.entry.index("## Gate cero obligatorio de `FOCAL_CYCLE`")
        self.assertLess(router, focal_gate)
        self.assertIn("REPOSITORY_MAINTENANCE", self.entry)
        self.assertIn("borrá las ramas detrás de main", self.entry)
        self.assertIn("scope `branches`", self.entry)

    def test_execution_is_distinct_from_implementation(self) -> None:
        self.assertIn("Una solicitud de **ejecución** administrativa", self.entry)
        self.assertIn("crear, implementar, mejorar, ampliar, reparar", self.control)
        self.assertIn("MAINTENANCE_INTENT_MISROUTED", self.control)
        self.assertIn("MAINTENANCE_EXECUTION_PATH_UNAVAILABLE", self.control)

    def test_dedicated_issue_is_the_permanent_ingress(self) -> None:
        self.assertIn("issue `#101`", self.control)
        self.assertIn("focal-repository-maintenance:v1", self.control)
        self.assertIn('"operation": "repository_maintenance"', self.control)
        self.assertIn("processedMaintenanceCommandIds", self.control)
        self.assertNotIn("Escribir el comando administrativo en `focal-command:v3`", self.control)

    def test_branch_cleanup_forbids_transport_artifacts(self) -> None:
        required = (
            "crear o actualizar una rama de transporte",
            "crear, abrir, modificar o mergear una PR",
            "crear o modificar un workflow",
            "createdBranches == []",
            "branchCountAfter <= branchCountBefore",
            "defaultBranchHeadAfter == defaultBranchHeadBefore",
        )
        for marker in required:
            self.assertIn(marker, self.control)

    def test_flowchart_has_independent_administrative_route(self) -> None:
        self.assertIn("MODE -- Ejecutar cleanup existente --> REPOSITORY_MAINTENANCE", self.flowchart)
        self.assertIn("MAINTENANCE_CREATED_REF", self.flowchart)
        self.assertIn("MAINTENANCE_CREATED_PR", self.flowchart)
        self.assertIn("MAINTENANCE_CREATED_WORKFLOW", self.flowchart)
        self.assertIn("MAINTENANCE_BRANCH_SCOPE_MODIFIED_DEFAULT_HEAD", self.flowchart)

    def test_terminal_report_does_not_invent_delivery_pr(self) -> None:
        self.assertIn("`REPOSITORY_MAINTENANCE`", self.terminal)
        self.assertIn("no tiene “rama final” ni “PR de entrega”", self.terminal)
        self.assertIn("Ramas creadas", self.terminal)
        self.assertIn("Head de main antes / después", self.terminal)


if __name__ == "__main__":
    unittest.main()
