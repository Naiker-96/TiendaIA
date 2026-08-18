<div align="center">

# 🤖 Tienda IA

### Smart Checkout con visión por computador

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-4.9+-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)
![YOLO11](https://img.shields.io/badge/YOLO11-Ultralytics-111F68?style=for-the-badge)
![License](https://img.shields.io/badge/Licencia-MIT-0F172A?style=for-the-badge)

**Sistema de caja de autoservicio en tiempo real que detecta productos, reconoce billetes colombianos y calcula el pago utilizando una cámara web.**

[Perfil de GitHub](https://github.com/Naiker-96) · [Código fuente](https://github.com/Naiker-96/TiendaIA)

</div>

---

## ✨ Qué problema resuelve

Tienda IA explora una experiencia de compra sin cajero utilizando hardware mínimo: **una cámara web y un computador**.

La aplicación analiza el video en tiempo real, identifica los productos ubicados en el área de compra, construye automáticamente la lista del cliente, reconoce billetes colombianos y calcula el saldo y el cambio directamente sobre la imagen de la cámara.

### Funcionalidades principales

| Función | Descripción |
|---|---|
| 🛒 **Detección de productos** | YOLO11 identifica objetos en vivo y los cruza con un catálogo de 32 productos con precios en COP |
| 🧾 **Lista automática** | Los productos visibles en el área de compras se agregan con nombre y precio |
| 💵 **Reconocimiento de billetes** | Un modelo independiente detecta billetes colombianos de $10.000, $20.000 y $50.000 |
| 💰 **Procesamiento de pago** | Calcula total, saldo abonado, valor faltante y cambio |
| 🎥 **Interfaz sobre video** | Detecciones, áreas, productos y totales se dibujan directamente sobre la cámara |

---

## 🧠 Arquitectura

```text
Cámara (1280x720)
   │
   ├── Frame limpio ──► YOLO11 productos ──► catálogo de precios ──► lista de compras
   │              └──► modelo de billetes ──► valor detectado     ──► saldo
   │
   └── Render final ──► zonas + detecciones + lista + totales ──► ventana "Tienda IA"
```

### Decisiones técnicas

- **Dos modelos independientes:** uno para objetos generales y otro para billetes colombianos.
- **Coordenadas normalizadas:** las zonas de compra, pago y lista se definen con proporciones para adaptarse a distintas resoluciones.
- **Catálogo centralizado:** nombres, precios, traducciones y valores de billetes viven en diccionarios de la clase principal.
- **Procesamiento por frame:** los objetos visibles actualizan la lista en tiempo real; el saldo y el estado de pago persisten.

---

## 🖥️ Interfaz

El video se divide en tres zonas funcionales:

| Zona | Comportamiento |
|---|---|
| **Área de compras** | Los productos detectados entran a la lista con nombre y precio |
| **Área de pago** | Los billetes detectados quedan listos para ser abonados |
| **Lista de compras** | Muestra productos, total y saldo entregado |

Cada detección incluye su bounding box, nombre en español y confianza del modelo.

### Controles

| Tecla | Acción |
|---|---|
| `S` | Abonar el billete detectado al saldo |
| `P` | Procesar el pago |
| `ESC` | Salir |

**Ejemplo:** una manzana y una taza suman $10.000 → se muestra un billete de $10.000 → `S` para abonarlo → `P` para procesar → compra confirmada.

---

## 🚀 Instalación

### Requisitos

- Python **3.10+**
- Cámara web
- Pesos de los modelos

```bash
git clone https://github.com/Naiker-96/TiendaIA.git
cd TiendaIA
python -m venv venv
```

**Windows**

```bash
venv\Scripts\activate
```

**Linux / macOS**

```bash
source venv/bin/activate
```

Luego:

```bash
pip install -r requirements.txt
python Tienda.py
```

---

## 🧩 Modelos

Los pesos no están incluidos en el repositorio debido a su tamaño.

Crea una carpeta `Modelo/` y agrega:

| Modelo | Uso | Fuente |
|---|---|---|
| `yolo11l.pt` | Detección de productos con clases COCO | [Ultralytics YOLO11](https://docs.ultralytics.com/models/yolo11/) |
| `billBank2.pt` | Billetes colombianos $10.000 / $20.000 / $50.000 | Disponible bajo solicitud |

---

## 📁 Estructura

```text
TiendaIA/
├── Tienda.py          # Punto de entrada
├── ShoppingIA.py      # Captura, inferencia, catálogo, pagos e interfaz
├── export.py          # Exportación de modelos a ONNX
├── requirements.txt   # Dependencias
└── Modelo/            # Pesos locales (no incluidos en Git)
```

---

## 🛠️ Tecnologías

`Python` · `OpenCV` · `Ultralytics YOLO11` · `ONNX`

---

## 🗺️ Próximas mejoras

- Ampliar el reconocimiento a billetes de $2.000, $5.000 y $100.000.
- Incorporar tracking, por ejemplo ByteTrack, para mantener productos aunque queden temporalmente ocultos.
- Generar recibos de compra en CSV o PDF.
- Crear histórico de ventas.
- Migrar inferencia a ONNX Runtime para reducir requerimientos de hardware.

---

## 👤 Autor

**Héctor Antolínez Rojas**  
Ingeniería de Sistemas y Computación · Data · Computer Vision · Cybersecurity

[GitHub](https://github.com/Naiker-96) · [LinkedIn](https://www.linkedin.com/in/hector-antolinez-rojas-067a0115a/)

---

## 📄 Licencia

[MIT](LICENSE) — © 2024 Héctor Antolínez Rojas
