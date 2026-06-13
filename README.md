# Tienda IA — Autoservicio con visión por computador

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![OpenCV](https://img.shields.io/badge/OpenCV-4.9+-green)
![YOLO](https://img.shields.io/badge/YOLO-v11-orange)
![License](https://img.shields.io/badge/Licencia-MIT-lightgrey)

Sistema de *smart checkout* (caja de autoservicio) en tiempo real escrito en Python: la cámara detecta los productos que el cliente coloca en el área de compras, los agrega a la lista con su precio, reconoce los billetes colombianos con los que paga y calcula el cambio — todo dibujado en vivo sobre la imagen de la cámara, sin pantallas ni botones físicos.

La idea simula la experiencia de tiendas sin cajero (estilo Amazon Go) con hardware mínimo: **una cámara web y un computador**.

## ¿Qué hace?

1. **Detecta productos.** Un modelo YOLO11 identifica en vivo los objetos frente a la cámara (frutas, accesorios, tecnología, utensilios...) y los cruza con un catálogo de 32 productos con precios en pesos colombianos.
2. **Arma la lista de compras.** Cada producto detectado dentro del área de compras se agrega una sola vez a la lista, con su nombre en español y su precio, y se va acumulando el total.
3. **Recibe el pago en efectivo.** Un segundo modelo de detección, dedicado solo a billetes colombianos, reconoce billetes de $10.000, $20.000 y $50.000 cuando se muestran en el área de pago.
4. **Calcula el cambio.** Al procesar el pago, compara el saldo entregado contra el total de la compra y muestra el cambio, lo que falta por pagar, o el mensaje de compra exitosa si el pago es exacto.

## ¿Cómo funciona por dentro?

El flujo de cada frame de la cámara es:

```
Cámara (1280x720)
   │
   ├── copia limpia del frame ──► YOLO11 (productos)  ──► catálogo de precios ──► lista de compras
   │                         └──► modelo de billetes  ──► valor del billete    ──► saldo
   │
   └── frame de salida: zonas + detecciones + lista + totales ──► ventana "Tienda IA"
```

- **Doble inferencia por frame:** sobre una copia limpia del frame corren dos modelos independientes — el de objetos generales (YOLO11, clases COCO) y el de billetes (`billBank2`, entrenado específicamente para denominaciones colombianas). Separarlos permite reemplazar o reentrenar cada uno sin tocar el otro.
- **Zonas con coordenadas normalizadas:** las tres zonas de la interfaz (*Área de compras*, *Área de pago* y *Lista de compras*) se definen con proporciones de 0 a 1 en lugar de píxeles, así el layout se adapta a cualquier resolución de cámara.
- **Catálogo como única fuente de verdad:** los productos, sus precios y las traducciones al español viven en diccionarios de la clase (`PRODUCT_PRICES`, `TRANSLATIONS`, `BILL_VALUES`). Para agregar un producto nuevo basta una línea en el catálogo — no hay que tocar la lógica.
- **Estado por frame:** la lista de compras se reconstruye en cada frame a partir de lo que la cámara ve en ese momento; el saldo abonado y el resultado del pago sí persisten entre frames.

## La interfaz

Sobre el video en vivo se dibujan tres zonas:

| Zona | Qué pasa ahí |
|------|--------------|
| **Área de compras** (izquierda) | Los productos detectados aquí entran a la lista con su nombre y precio |
| **Área de pago** (derecha arriba) | Los billetes mostrados aquí se reconocen y quedan listos para abonar |
| **Lista de compras** (derecha abajo) | Lista de productos, total de la compra y saldo entregado |

Cada detección se dibuja con su recuadro, el nombre en español y el porcentaje de confianza del modelo.

## Controles

| Tecla | Acción |
|-------|--------|
| `S`   | Abonar el billete detectado al saldo |
| `P`   | Procesar el pago (muestra el cambio, lo que falta, o confirma la compra) |
| `ESC` | Salir |

**Ejemplo de uso:** coloca una manzana y una taza frente a la cámara → aparecen en la lista ($2.000 + $8.000 = $10.000) → muestra un billete de $10.000 en el área de pago → presiona `S` para abonarlo → presiona `P` → "¡Gracias por su compra!".

## Instalación

Requiere **Python 3.10+** y una cámara web.

```bash
git clone https://github.com/Naiker-96/TiendaIA.git
cd TiendaIA
python -m venv venv
venv\Scripts\activate        # En Linux/Mac: source venv/bin/activate
pip install -r requirements.txt
```

### Modelos

Los pesos no se incluyen en el repositorio por su tamaño. Crear la carpeta `Modelo/` y colocar en ella:

| Modelo | Función | Dónde conseguirlo |
|--------|---------|-------------------|
| `yolo11l.pt` | Detección de productos (clases COCO) | Descarga oficial de [Ultralytics](https://docs.ultralytics.com/models/yolo11/) |
| `billBank2.pt` | Detección de billetes colombianos ($10.000 / $20.000 / $50.000) | Disponible bajo solicitud |

## Uso

```bash
python Tienda.py
```

Consejos para mejores resultados: buena iluminación, fondo despejado y mostrar los billetes extendidos (sin doblar) frente a la cámara.

## Estructura del proyecto

| Archivo | Descripción |
|---------|-------------|
| `Tienda.py` | Punto de entrada: crea la instancia y arranca el ciclo principal |
| `ShoppingIA.py` | Clase `ShopIA`: captura de cámara, inferencia de los dos modelos, catálogo, lista de compras, proceso de pago y todo el dibujado de la interfaz |
| `export.py` | Utilidad para exportar los modelos a formato ONNX |
| `requirements.txt` | Dependencias (Ultralytics y OpenCV) |

## Limitaciones e ideas futuras

- El modelo de billetes cubre tres denominaciones; ampliarlo a $2.000, $5.000 y $100.000 requiere reentrenar con más datos.
- La lista depende de lo que la cámara ve en cada momento: si un producto se tapa, sale de la lista. Una mejora natural es darle memoria con un *tracker* (p. ej. ByteTrack) para mantener productos ya escaneados.
- Exportar el recibo de compra (CSV/PDF) y llevar histórico de ventas.
- Migrar la inferencia a ONNX Runtime (los modelos ya se pueden exportar con `export.py`) para correr más liviano en equipos modestos.

## Tecnologías

Python · OpenCV · Ultralytics YOLO (v8/v11) · ONNX

## Licencia

[MIT](LICENSE) — © 2024 Héctor Antolínez Rojas
