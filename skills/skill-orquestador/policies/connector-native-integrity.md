# Extensión — integridad de publicación connector-native

> Runtime repository variables
>
> - `{{repository_full_name}}`: exact `owner/name`, resolved from the user request, project context, URL, or connector metadata.
> - `{{repository_url}}`: canonical repository URL when an action specifically requires a URL.
> - `{{default_branch}}`: remote default branch resolved through repository metadata.
> - `{{base_sha}}`: exact verified base commit SHA.
> - `{{branch}}`: explicitly authorized working branch.
>
> No repository, owner, branch, framework, product, or organization is a built-in default.

Esta política complementa las reglas GitHub de `../playbooks/github/` y queda subordinada a `network-and-transport.md`.

## 1. Uso permitido

La secuencia `create_blob → create_tree → create_commit → create_branch/update_ref` es el mecanismo remoto autorizado cuando existe un source completo y validado.

No es un clon, no crea un working tree y no sustituye la validación local.

## 2. Manifest de publicación obligatorio

Antes de crear blobs, producir un manifest determinista por path:

```text
path
operation: add | modify | delete | rename
sourcePath, cuando sea rename
mode: 100644 | 100755 | 120000 | 160000
byteLength
localSha256
gitBlobSha1Expected
encoding: binary | utf-8
```

El manifest debe estar ligado al `base_sha`, `base_tree_sha`, branch objetivo y mensaje de commit.

## 3. Git blob SHA-1 esperado

Calcular sobre bytes exactos:

```text
SHA1("blob " + decimal_byte_length + NUL + bytes)
```

No calcular sobre texto reserializado, contenido normalizado ni una representación Base64 salvo que primero se decodifique al byte stream original.

## 4. Publicación

```text
LOCAL_BYTES_VALIDATED
→ crear blobs
→ comprobar SHA devuelto contra gitBlobSha1Expected
→ crear tree sobre base_tree_sha
→ crear commit con parent_sha exacto
→ crear branch o mover ref fast-forward
```

Prohibido:

```text
update_ref(force=true)
parent desconocido
base tree inferido sin verificación
publicar archivos no incluidos en el manifest
```

## 5. Verificación byte por byte obligatoria

Después de publicar:

1. Recuperar commit y tree remotos.
2. Verificar parent, tree, mensaje y ref.
3. Para cada add/modify/rename:
   - verificar path y mode;
   - recuperar blob remoto;
   - verificar blob SHA;
   - comparar tamaño;
   - calcular SHA-256 remoto;
   - exigir igualdad con `localSha256`.
4. Para cada delete, demostrar ausencia en el tree final.
5. Para rename, demostrar ausencia del path anterior y presencia exacta del nuevo.
6. Para modo `120000`, comparar los bytes del target del symlink, no el archivo apuntado.
7. Para modo `160000`, comparar el commit gitlink exacto; no tratarlo como blob.
8. Comparar el conjunto completo de paths cambiados contra el manifest.

Solo entonces declarar:

```text
REMOTE_BYTES_VERIFIED
```

## 6. Binarios y finales de línea

Los binarios deben transportarse como bytes exactos. Los archivos de texto no deben sufrir conversión implícita de LF/CRLF durante la creación del blob.

La validación remota debe usar SHA-256 sobre bytes recuperados, no una comparación semántica de texto.

## 7. Fallo

Cualquier diferencia de SHA, mode, path, parent, tree o ref activa `STOP-THE-LINE`. No ejecutar CI como prueba de integridad ni mover nuevamente la ref para ocultar el fallo.
