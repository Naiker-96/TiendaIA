import cv2
from ultralytics import YOLO
import math

class ShopIA:
    def __init__(self):
        try:
            self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

            if not self.cap.isOpened():
                raise Exception("No se pudo abrir la cámara")

            # Configurar la calidad de la cámara
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
            self.cap.set(cv2.CAP_PROP_FPS, 30)

            # Verificar que la cámara funciona
            ret, test_frame = self.cap.read()
            if not ret:
                raise Exception("No se pueden leer frames de la cámara")

            # MODELS:
            ObjectModel = YOLO('Modelo/yolo11l.pt')
            self.ObjectModel = ObjectModel

            billModel = YOLO('Modelo/billBank2.pt')
            self.billModel = billModel

            # CLASES:
            # Objects
            clsObject = ObjectModel.names
            self.clsObject = clsObject

            # Bills Bank
            clsBillBank = ['Billete10', 'Billete20', 'Billete50']
            self.clsBillBank = clsBillBank

            # Total balance
            self.total_balance = 0
            self.pay = ''


        except Exception as e:
            print(f"Error al inicializar la cámara: {str(e)}")
            if hasattr(self, 'cap'):
                self.cap.release()
            cv2.destroyAllWindows()
            raise

    def add_to_shopping_list(self, object, list_products, frame, list_area_xi, list_area_yi, size_obj, thickness_obj):
        if object not in [item[0] for item in self.shopping_list]:
            price = list_products[object]
            self.shopping_list.append([object, price])
            # Show
            text = f'{object} --> ${price}'
            frame = self.draw_text(frame, (0, 255, 0), text, list_area_xi + 10,
                                   list_area_yi + (40 + (self.posicion_products * 20)),
                                   size_obj, thickness_obj, back=False)
            self.posicion_products += 1
            # Price
            self.accumulative_price += price

    # DRAW FUNCTIONS
    # Area
    def draw_area(self, img, color, xi, yi, xf, yf):
        img = cv2.rectangle(img, (xi, yi), (xf, yf), color, 1, 1)
        return img

    # Text
    def draw_text(self, img, color, text, xi, yi, size, thickness, back=False):
        sizetext = cv2.getTextSize(text, cv2.FONT_HERSHEY_DUPLEX, size, thickness)
        dim = sizetext[0]
        baseline = sizetext[1]
        if back is True:
            img = cv2.rectangle(img, (xi, yi - dim[1] - baseline), (xi + dim[0], yi + baseline - 7), (0, 0, 0), cv2.FILLED)
        img = cv2.putText(img, text, (xi, yi - 5), cv2.FONT_HERSHEY_DUPLEX, size, color, thickness)
        return img

    # Line
    def draw_line(self, img, color, xi, yi, xf, yf):
        img = cv2.line(img, (xi, yi), (xf, yf), color, 1, 1)
        return img

    def area(self, frame, xi, yi, xf, yf):
        # Info
        al, an, c = frame.shape
        # Coordenates
        xi, yi = int(xi * an), int(yi * al)
        xf, yf = int(xf * an), int(yf * al)

        return xi, yi, xf, yf

    def marketplace_list(self, frame, object):
        # Diccionario de productos y precios
        list_products = {
            'backpack': 80000,  # Mochila
            'umbrella': 25000,  # Paraguas
            'handbag': 60000,  # Bolso
            'tie': 35000,  # Corbata
            'suitcase': 150000,  # Maleta
            'sports ball': 30000,  # Pelota
            'bottle': 5000,  # Botella
            'wine glass': 15000,  # Copa
            'cup': 8000,  # Taza
            'fork': 3000,  # Tenedor
            'knife': 3500,  # Cuchillo
            'spoon': 3000,  # Cuchara
            'bowl': 12000,  # Tazón
            'banana': 1000,  # Banano
            'apple': 2000,  # Manzana
            'sandwich': 8000,  # Sandwich
            'orange': 1500,  # Naranja
            'broccoli': 3000,  # Brócoli
            'carrot': 2000,  # Zanahoria
            'hot dog': 7000,  # Perro Caliente
            'pizza': 25000,  # Pizza
            'donut': 3500,  # Dona
            'cake': 35000,  # Pastel
            'mouse': 35000,  # Mouse
            'keyboard': 85000,  # Teclado
            'cell phone': 1200000,  # Celular
            'book': 45000,  # Libro
            'clock': 55000,  # Reloj
            'vase': 40000,  # Florero
            'scissors': 12000,  # Tijeras
            'teddy bear': 40000,  # Peluche
            'toothbrush': 5000  # Cepillo de dientes
        }

        # Text Config
        list_area_xi, list_area_yi, list_area_xf, list_area_yf = self.area(frame, 0.7739, 0.6250, 0.9649, 0.9444)
        size_obj, thickness_obj = 0.60, 1

        # Mochila
        if object == 'backpack' and object not in [item[0] for item in self.shopping_list]:
            price = list_products['backpack']
            self.shopping_list.append([object, price])
            text = f'Mochila --> ${price:,}'
            frame = self.draw_text(frame, (0, 255, 0), text, list_area_xi + 10,
                                   list_area_yi + (40 + (self.posicion_products * 20)),
                                   size_obj, thickness_obj, back=False)
            self.posicion_products += 1
            self.accumulative_price += price

        # Bolso
        if object == 'handbag' and object not in [item[0] for item in self.shopping_list]:
            price = list_products['handbag']
            self.shopping_list.append([object, price])
            text = f'Bolso --> ${price:,}'
            frame = self.draw_text(frame, (0, 255, 0), text, list_area_xi + 10,
                                   list_area_yi + (40 + (self.posicion_products * 20)),
                                   size_obj, thickness_obj, back=False)
            self.posicion_products += 1
            self.accumulative_price += price

        # Pelota
        if object == 'sports ball' and object not in [item[0] for item in self.shopping_list]:
            price = list_products['sports ball']
            self.shopping_list.append([object, price])
            text = f'Pelota --> ${price:,}'
            frame = self.draw_text(frame, (0, 255, 0), text, list_area_xi + 10,
                                   list_area_yi + (40 + (self.posicion_products * 20)),
                                   size_obj, thickness_obj, back=False)
            self.posicion_products += 1
            self.accumulative_price += price

        # Botella
        if object == 'bottle' and object not in [item[0] for item in self.shopping_list]:
            price = list_products['bottle']
            self.shopping_list.append([object, price])
            text = f'Botella --> ${price:,}'
            frame = self.draw_text(frame, (0, 255, 0), text, list_area_xi + 10,
                                   list_area_yi + (40 + (self.posicion_products * 20)),
                                   size_obj, thickness_obj, back=False)
            self.posicion_products += 1
            self.accumulative_price += price

        # Taza
        if object == 'cup' and object not in [item[0] for item in self.shopping_list]:
            price = list_products['cup']
            self.shopping_list.append([object, price])
            text = f'Taza --> ${price:,}'
            frame = self.draw_text(frame, (0, 255, 0), text, list_area_xi + 10,
                                   list_area_yi + (40 + (self.posicion_products * 20)),
                                   size_obj, thickness_obj, back=False)
            self.posicion_products += 1
            self.accumulative_price += price

        # Tenedor
        if object == 'fork' and object not in [item[0] for item in self.shopping_list]:
            price = list_products['fork']
            self.shopping_list.append([object, price])
            text = f'Tenedor --> ${price:,}'
            frame = self.draw_text(frame, (0, 255, 0), text, list_area_xi + 10,
                                   list_area_yi + (40 + (self.posicion_products * 20)),
                                   size_obj, thickness_obj, back=False)
            self.posicion_products += 1
            self.accumulative_price += price

        # Cuchillo
        if object == 'knife' and object not in [item[0] for item in self.shopping_list]:
            price = list_products['knife']
            self.shopping_list.append([object, price])
            text = f'Cuchillo --> ${price:,}'
            frame = self.draw_text(frame, (0, 255, 0), text, list_area_xi + 10,
                                   list_area_yi + (40 + (self.posicion_products * 20)),
                                   size_obj, thickness_obj, back=False)
            self.posicion_products += 1
            self.accumulative_price += price

        # Cuchara
        if object == 'spoon' and object not in [item[0] for item in self.shopping_list]:
            price = list_products['spoon']
            self.shopping_list.append([object, price])
            text = f'Cuchara --> ${price:,}'
            frame = self.draw_text(frame, (0, 255, 0), text, list_area_xi + 10,
                                   list_area_yi + (40 + (self.posicion_products * 20)),
                                   size_obj, thickness_obj, back=False)
            self.posicion_products += 1
            self.accumulative_price += price

        # Banano
        if object == 'banana' and object not in [item[0] for item in self.shopping_list]:
            price = list_products['banana']
            self.shopping_list.append([object, price])
            text = f'Banano --> ${price:,}'
            frame = self.draw_text(frame, (0, 255, 0), text, list_area_xi + 10,
                                   list_area_yi + (40 + (self.posicion_products * 20)),
                                   size_obj, thickness_obj, back=False)
            self.posicion_products += 1
            self.accumulative_price += price

        # Manzana
        if object == 'apple' and object not in [item[0] for item in self.shopping_list]:
            price = list_products['apple']
            self.shopping_list.append([object, price])
            text = f'Manzana --> ${price:,}'
            frame = self.draw_text(frame, (0, 255, 0), text, list_area_xi + 10,
                                   list_area_yi + (40 + (self.posicion_products * 20)),
                                   size_obj, thickness_obj, back=False)
            self.posicion_products += 1
            self.accumulative_price += price

        # Naranja
        if object == 'orange' and object not in [item[0] for item in self.shopping_list]:
            price = list_products['orange']
            self.shopping_list.append([object, price])
            text = f'Naranja --> ${price:,}'
            frame = self.draw_text(frame, (0, 255, 0), text, list_area_xi + 10,
                                   list_area_yi + (40 + (self.posicion_products * 20)),
                                   size_obj, thickness_obj, back=False)
            self.posicion_products += 1
            self.accumulative_price += price

        # Zanahoria
        if object == 'carrot' and object not in [item[0] for item in self.shopping_list]:
            price = list_products['carrot']
            self.shopping_list.append([object, price])
            text = f'Zanahoria --> ${price:,}'
            frame = self.draw_text(frame, (0, 255, 0), text, list_area_xi + 10,
                                   list_area_yi + (40 + (self.posicion_products * 20)),
                                   size_obj, thickness_obj, back=False)
            self.posicion_products += 1
            self.accumulative_price += price

        # Mouse
        if object == 'mouse' and object not in [item[0] for item in self.shopping_list]:
            price = list_products['mouse']
            self.shopping_list.append([object, price])
            text = f'Mouse --> ${price:,}'
            frame = self.draw_text(frame, (0, 255, 0), text, list_area_xi + 10,
                                   list_area_yi + (40 + (self.posicion_products * 20)),
                                   size_obj, thickness_obj, back=False)
            self.posicion_products += 1
            self.accumulative_price += price

        # Teclado
        if object == 'keyboard' and object not in [item[0] for item in self.shopping_list]:
            price = list_products['keyboard']
            self.shopping_list.append([object, price])
            text = f'Teclado --> ${price:,}'
            frame = self.draw_text(frame, (0, 255, 0), text, list_area_xi + 10,
                                   list_area_yi + (40 + (self.posicion_products * 20)),
                                   size_obj, thickness_obj, back=False)
            self.posicion_products += 1
            self.accumulative_price += price

        # Celular
        if object == 'cell phone' and object not in [item[0] for item in self.shopping_list]:
            price = list_products['cell phone']
            self.shopping_list.append([object, price])
            text = f'Celular --> ${price:,}'
            frame = self.draw_text(frame, (0, 255, 0), text, list_area_xi + 10,
                                   list_area_yi + (40 + (self.posicion_products * 20)),
                                   size_obj, thickness_obj, back=False)
            self.posicion_products += 1
            self.accumulative_price += price

        # Libro
        if object == 'book' and object not in [item[0] for item in self.shopping_list]:
            price = list_products['book']
            self.shopping_list.append([object, price])
            text = f'Libro --> ${price:,}'
            frame = self.draw_text(frame, (0, 255, 0), text, list_area_xi + 10,
                                   list_area_yi + (40 + (self.posicion_products * 20)),
                                   size_obj, thickness_obj, back=False)
            self.posicion_products += 1
            self.accumulative_price += price

        # Reloj
        if object == 'clock' and object not in [item[0] for item in self.shopping_list]:
            price = list_products['clock']
            self.shopping_list.append([object, price])
            text = f'Reloj --> ${price:,}'
            frame = self.draw_text(frame, (0, 255, 0), text, list_area_xi + 10,
                                   list_area_yi + (40 + (self.posicion_products * 20)),
                                   size_obj, thickness_obj, back=False)
            self.posicion_products += 1
            self.accumulative_price += price

        # Tijeras
        if object == 'scissors' and object not in [item[0] for item in self.shopping_list]:
            price = list_products['scissors']
            self.shopping_list.append([object, price])
            text = f'Tijeras --> ${price:,}'
            frame = self.draw_text(frame, (0, 255, 0), text, list_area_xi + 10,
                                   list_area_yi + (40 + (self.posicion_products * 20)),
                                   size_obj, thickness_obj, back=False)
            self.posicion_products += 1
            self.accumulative_price += price

        # Peluche
        if object == 'teddy bear' and object not in [item[0] for item in self.shopping_list]:
            price = list_products['teddy bear']
            self.shopping_list.append([object, price])
            text = f'Peluche --> ${price:,}'
            frame = self.draw_text(frame, (0, 255, 0), text, list_area_xi + 10,
                                   list_area_yi + (40 + (self.posicion_products * 20)),
                                   size_obj, thickness_obj, back=False)
            self.posicion_products += 1
            self.accumulative_price += price

        # Cepillo de dientes
        if object == 'toothbrush' and object not in [item[0] for item in self.shopping_list]:
            price = list_products['toothbrush']
            self.shopping_list.append([object, price])
            text = f'Cepillo de dientes --> ${price:,}'
            frame = self.draw_text(frame, (0, 255, 0), text, list_area_xi + 10,
                                   list_area_yi + (40 + (self.posicion_products * 20)),
                                   size_obj, thickness_obj, back=False)
            self.posicion_products += 1
            self.accumulative_price += price

        return frame

    # Balance process
    def balance_process(self, bill_type):
        if bill_type == 'Billete10':
            self.balance = 10000
        elif bill_type == 'Billete20':
            self.balance = 20000
        elif bill_type == 'Billete50':
            self.balance = 50000

    # Payment process
    def payment_process(self, accumulative_price, accumulative_balance):
        payment = accumulative_balance - accumulative_price
        print(payment)
        if payment < 0:
            text = f'Falta cancelar ${abs(payment):,}'

        elif payment > 0:
            text = f'Su cambio es de: ${abs(payment):,}'
            self.accumulative_price = 0
            self.total_balance = 0

        elif payment == 0:
            text = '¡Gracias por su compra!'
            self.accumulative_price = 0
            self.total_balance = 0

        return text

    # INFERENCE
    def prediction_model(self, clean_frame, frame, model, clase):

        # Diccionario de traducción de nombres
        translations = {
            'person': 'Persona',
            'bicycle': 'Bicicleta',
            'car': 'Carro',
            'motorcycle': 'Motocicleta',
            'airplane': 'Avión',
            'bus': 'Bus',
            'train': 'Tren',
            'truck': 'Camión',
            'boat': 'Bote',
            'traffic light': 'Semáforo',
            'fire hydrant': 'Hidrante',
            'stop sign': 'Señal de Stop',
            'parking meter': 'Parquímetro',
            'bench': 'Banca',
            'bird': 'Pájaro',
            'cat': 'Gato',
            'dog': 'Perro',
            'horse': 'Caballo',
            'sheep': 'Oveja',
            'cow': 'Vaca',
            'elephant': 'Elefante',
            'bear': 'Oso',
            'zebra': 'Cebra',
            'giraffe': 'Jirafa',
            'backpack': 'Mochila',
            'umbrella': 'Paraguas',
            'handbag': 'Bolso',
            'tie': 'Corbata',
            'suitcase': 'Maleta',
            'frisbee': 'Frisbee',
            'skis': 'Esquís',
            'snowboard': 'Snowboard',
            'sports ball': 'Pelota',
            'kite': 'Cometa',
            'baseball bat': 'Bate',
            'baseball glove': 'Guante',
            'skateboard': 'Patineta',
            'surfboard': 'Tabla de surf',
            'tennis racket': 'Raqueta',
            'bottle': 'Botella',
            'wine glass': 'Copa',
            'cup': 'Taza',
            'fork': 'Tenedor',
            'knife': 'Cuchillo',
            'spoon': 'Cuchara',
            'bowl': 'Tazón',
            'banana': 'Banano',
            'apple': 'Manzana',
            'sandwich': 'Sandwich',
            'orange': 'Naranja',
            'broccoli': 'Brócoli',
            'carrot': 'Zanahoria',
            'hot dog': 'Perro Caliente',
            'pizza': 'Pizza',
            'donut': 'Dona',
            'cake': 'Pastel',
            'chair': 'Silla',
            'couch': 'Sofá',
            'potted plant': 'Planta',
            'bed': 'Cama',
            'dining table': 'Mesa',
            'toilet': 'Inodoro',
            'tv': 'Televisor',
            'laptop': 'Portátil',
            'mouse': 'Mouse',
            'remote': 'Control',
            'keyboard': 'Teclado',
            'cell phone': 'Celular',
            'microwave': 'Microondas',
            'oven': 'Horno',
            'toaster': 'Tostadora',
            'sink': 'Lavaplatos',
            'refrigerator': 'Nevera',
            'book': 'Libro',
            'clock': 'Reloj',
            'vase': 'Florero',
            'scissors': 'Tijeras',
            'teddy bear': 'Peluche',
            'hair drier': 'Secador',
            'toothbrush': 'Cepillo de dientes'
        }


        cls = 0
        conf = 0
        # Yolo | AntiSpoof
        results = model(clean_frame, stream=True, verbose=False)
        for res in results:
            # Box
            boxes = res.boxes
            for box in boxes:
                # Bounding box
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

                # Error < 0
                if x1 < 0:
                    x1 = 0
                if y1 < 0:
                    y1 = 0
                if x2 < 0:
                    x2 = 0
                if y2 < 0:
                    y2 = 0

                # bbox = [x1, y1, x2, y2]

                # Class
                cls = int(box.cls[0])

                # Confidence
                conf = math.ceil(box.conf[0])

                if clase == 0:
                    # Draw
                    objeto = self.clsObject[cls]
                    # Traducir el nombre para la detección
                    nombre_esp = translations.get(objeto, objeto)
                    text_obj = f'{nombre_esp} {int(conf * 100)}%'
                    # Marketplace list
                    frame = self.marketplace_list(frame, objeto)

                    # Draw
                    size_obj, thickness_obj = 0.75, 1
                    frame = self.draw_text(frame, (0, 255, 0), text_obj, x1, y1, size_obj, thickness_obj, back=True)
                    frame = self.draw_area(frame, (0, 255, 0), x1, y1, x2, y2)

                if clase == 1:
                    # Draw
                    bill_type = self.clsBillBank[cls]
                    text_obj = f'{self.clsBillBank[cls]} {int(conf * 100)}%'
                    self.balance_process(bill_type)

                    # Draw
                    size_obj, thickness_obj = 0.75, 1
                    frame = self.draw_text(frame, (0, 255, 0), text_obj, x1, y1, size_obj, thickness_obj, back=True)
                    frame = self.draw_area(frame, (0, 255, 0), x1, y1, x2, y2)

                    # break
        return frame

    # Main
    def tiendaIA(self, cap):
        while True:
            # Frames
            ret, frame = cap.read()
            # Read keyboard
            t = cv2.waitKey(5)

            # Frame Object Detect
            clean_frame = frame.copy()

            # Info Marketplace list
            shopping_list = []
            self.shopping_list = shopping_list
            posicion_products = 1
            self.posicion_products = posicion_products
            accumulative_price = 0
            self.accumulative_price = accumulative_price
            # Info Payment process
            balance = 0
            self.balance = balance

            # Areas
            # Shopping area
            shop_area_xi, shop_area_yi, shop_area_xf, shop_area_yf = self.area(frame, 0.0351, 0.0486, 0.7539, 0.9444)
            # Draw
            color = (0, 255, 0)
            text_shop = 'Area de Compras'
            size_shop, thickness_shop = 0.75, 1
            frame = self.draw_area(frame, color, shop_area_xi, shop_area_yi, shop_area_xf, shop_area_yf)
            frame = self.draw_text(frame, color, text_shop, shop_area_xi, shop_area_yf + 30, size_shop, thickness_shop)

            # Payment area
            pay_area_xi, pay_area_yi, pay_area_xf, pay_area_yf = self.area(frame, 0.7739, 0.0486, 0.9649, 0.6050)
            # Draw
            text_pay = 'Area de Pago'
            size_pay, thickness_pay = 0.50, 1
            frame = self.draw_line(frame, color, pay_area_xi, pay_area_yi, pay_area_xi, int((pay_area_yi+pay_area_yf)/2))
            frame = self.draw_line(frame, color, pay_area_xi, pay_area_yi, int((pay_area_xi+pay_area_xf)/2), pay_area_yi)
            frame = self.draw_line(frame, color, pay_area_xf, int((pay_area_yi+pay_area_yf)/2), pay_area_xf, pay_area_yf)
            frame = self.draw_line(frame, color, int((pay_area_xi+pay_area_xf)/2), pay_area_yf, pay_area_xf, pay_area_yf)
            frame = self.draw_text(frame, color, text_pay, pay_area_xf-100, shop_area_yi+10, size_pay, thickness_pay)

            # List area
            list_area_xi, list_area_yi, list_area_xf, list_area_yf = self.area(frame, 0.7739, 0.6250, 0.9649, 0.9444)
            # Draw
            text_list = 'Lista de Compras'
            size_list, thickness_list = 0.65, 1
            frame = self.draw_line(frame, color, list_area_xi, list_area_yi, list_area_xi, list_area_yf)
            frame = self.draw_line(frame, color, list_area_xi, list_area_yi, list_area_xf, list_area_yi)
            frame = self.draw_line(frame, color, list_area_xi+30, list_area_yi+30, list_area_xf-30, list_area_yi+30)
            frame = self.draw_text(frame, color, text_list, list_area_xi+55, list_area_yi+30, size_list, thickness_list)

            # Predict Object
            frame = self.prediction_model(clean_frame, frame, self.ObjectModel, clase=0)
            # Predict Bills Bank
            frame = self.prediction_model(clean_frame, frame, self.billModel, clase=1)

            # Accumulative Price Show
            text_price = f'Compra total: ${self.accumulative_price:,} $'
            frame = self.draw_text(frame, (0, 255, 0), text_price, list_area_xi + 10, list_area_yf, 0.60, 1, back=False)
            # Total Balance Show
            text_balance = f'Saldo total: ${self.total_balance:,} $'
            frame = self.draw_text(frame, (0, 255, 0), text_balance, list_area_xi + 10, list_area_yf + 30, 0.60, 1, back=False)
            # Payment
            frame = self.draw_text(frame, (0, 255, 0), self.pay, list_area_xi + - 300, list_area_yf + 30, 0.60, 1, back=False)

            # Show
            cv2.imshow("Tienda IA", frame)

            # Balance
            if t == 83 or t == 115:
                self.total_balance = self.total_balance + self.balance
                self.balance = 0
            # Payment
            if t == 80 or t == 112:
                self.pay = self.payment_process(self.accumulative_price, self.total_balance)
            # Exit
            if t == 27:
                break

        # Release
        self.cap.release()
        cv2.destroyAllWindows()