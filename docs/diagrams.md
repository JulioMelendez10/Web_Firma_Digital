**Diagramas de la feature: Firma Digital**

Archivo con diagramas Mermaid que describen el flujo, las entidades (ER) y el diagrama de clases de la funcionalidad de firma digital.

1) Flujo de la firma (flowchart)

```mermaid
flowchart TD
  U[Usuario] -->|Sube .cer/.key| C[Certificados - /certificates/]
  U -->|Sube documento| D[Documentos - /documents/]
  U -->|Selecciona cert + pwd| V[Vista Detalle Documento]
  V -->|Calcula hash SHA-256| H[Hash SHA-256]
  V -->|Carga .key y firma hash| S[Firma con llave privada]
  S -->|Almacena firma| DB[(Base de Datos)]
  DB -->|Almacena: Documento.firma_sha256, fecha_firma, certificado| D
  U -->|Verificar| V
  V -->|Toma firma y .cer, verifica| R[Resultado de verificación]
  R --> U

  style DB fill:#f9f,stroke:#333,stroke-width:2px
```

2) Diagrama de Entidades (ER)

```mermaid
erDiagram
    DOCUMENTO {
        int id PK
        string titulo
        string descripcion
        string archivo_path
        string hash_sha256
        bool esta_firmado
        text firma_sha256
        datetime fecha_firma
        int certificado_id FK
    }

    CERTIFICADO {
        int id PK
        string archivo_cer_path
        string archivo_key_path
        string numero_serie
        string subject
        string issuer
        string rfc
        string curp
        datetime fecha_inicio
        datetime fecha_expiracion
        string algoritmo_firma
        string huella_sha256
    }

    DOCUMENTO }o--|| CERTIFICADO : "usa/puede referenciar"
```

3) Diagrama de Clases (simplificado)

```mermaid
classDiagram
    class Documento {
      +int id
      +string titulo
      +string descripcion
      +File archivo
      +string hash_sha256
      +bool esta_firmado
      +string firma_sha256
      +datetime fecha_firma
      +calcular_hash()
      +guardar_con_hash()
      +firmar_documento(certificado, key_password)
    }

    class Certificado {
      +int id
      +File archivo_cer
      +File archivo_key
      +string numero_serie
      +string subject
      +string issuer
      +string rfc
      +datetime fecha_inicio
      +datetime fecha_expiracion
      +string algoritmo_firma
      +string huella_sha256
      +extraer_metadatos()
    }

    Documento --> Certificado : "usa referencia a"
```

4) Notas y uso

- Los diagramas están escritos en Mermaid y se renderizan en muchos visores de Markdown (por ejemplo GitHub, VSCode con extensión Mermaid). Si tu plataforma no renderiza Mermaid, puedes abrir el archivo en VSCode con la extensión "Markdown Preview Enhanced" o usar el live editor de Mermaid (https://mermaid.live).
- Archivos añadidos al repo: `docs/diagrams.md`.

Si quieres, puedo además generar PNG/SVG exportados desde Mermaid y añadirlos a `docs/images/`.
