from ultralytics import YOLO

#Carga de Modelo
model =YOLO('Modelo/yolov8l.pt')

#Exportar
model.export(format = 'onnx')
