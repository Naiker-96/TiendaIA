# Tienda IA — Autoservicio con visión por computador

Sistema de *smart checkout* en tiempo real construido en Python: la cámara detecta los productos que el cliente coloca en el área de compras, los suma a la lista con su precio, reconoce los billetes colombianos con los que paga y calcula el cambio — todo en vivo sobre la imagen de la cámara.

## Cómo funciona

- **Detección de productos:** un modelo YOLO11 identifica más de 20 tipos de productos (frutas, accesorios, tecnología, etc.) y los cruza con un catálogo de precios en pesos colombianos.
- **Reconocimiento de billetes:** un segundo modelo de detección reconoce billetes colombianos de $10.000, $20.000 y $50.000 dentro del área de pago.
- **Interfaz en vivo:** sobre el video de la cámara (OpenCV) se dibujan tres zonas — *Área de compras*, *Área de pago* y *Lista de compras* — con el total acumulado, el saldo entregado y el cambio.

## Controles

| Tecla | Acción |
|-------|--------|
| `S`   | Abonar el billete detectado al saldo |
| `P`   | Procesar el pago (muestra el cambio o lo que falta) |
| `ESC` | Salir |

## Instalación

Requiere Python 3.10+ y una cámara web.

```bash
git clone <url-del-repo>
cd tienda-ia
python -m venv venv
venv\Scripts\activate        # En Linux/Mac: source venv/bin/activate
pip install -r requirements.txt
```

### Modelos

Los pesos no se incluyen en el repositorio por su tamaño. Crear la carpeta `Modelo/` y colocar en ella:

- `yolo11l.pt` — descarga oficial de [Ultralytics](https://docs.ultralytics.com/models/yolo11/).
- `billBank2.pt` — modelo de detección de billetes colombianos (disponible bajo solicitud).

## Uso

```bash
python Tienda.py
```

## Estructura

| Archivo | Descripción |
|---------|-------------|
| `Tienda.py` | Punto de entrada |
| `ShoppingIA.py` | Lógica de detección, lista de compras y proceso de pago |
| `export.py` | Exportación de modelos a formato ONNX |

## Tecnologías

Python · OpenCV · Ultralytics YOLO (v8/v11) · ONNX
