import logging
import time

from PIL import Image, ImageDraw, ImageFont

from src.external.LCD_2inch import LCD_2inch


class DisplayController:
    def __init__(self):
        print("Hello DisplayController!")

        logging.basicConfig(level=logging.DEBUG)
        try:
            # display with hardware SPI:
            """
            Warning!!!Don't  creation of multiple displayer objects!!!
            """
            self.disp = LCD_2inch()
            # Initialize library.
            self.disp.Init()
            # Clear display.
            self.disp.clear()
            # Set the backlight to 100
            self.disp.bl_DutyCycle(50)

            logging.info("show image")
            image = Image.open("../pic/LCD_2inch.jpg")
            image = image.rotate(180)
            self.disp.ShowImage(image)
            time.sleep(1)

            # Create blank image for drawing.
            image1 = Image.new("RGB", (self.disp.height, self.disp.width), "WHITE")
            self.draw = ImageDraw.Draw(image1)

            logging.info("draw point")

            self.draw.rectangle((5, 10, 6, 11), fill="BLACK")
            self.draw.rectangle((5, 25, 7, 27), fill="BLACK")
            self.draw.rectangle((5, 40, 8, 43), fill="BLACK")
            self.draw.rectangle((5, 55, 9, 59), fill="BLACK")

            logging.info("draw line")
            self.draw.line([(20, 10), (70, 60)], fill="RED", width=1)
            self.draw.line([(70, 10), (20, 60)], fill="RED", width=1)
            self.draw.line([(170, 15), (170, 55)], fill="RED", width=1)
            self.draw.line([(150, 35), (190, 35)], fill="RED", width=1)

            logging.info("draw rectangle")
            self.draw.rectangle([(20, 10), (70, 60)], fill="WHITE", outline="BLUE")
            self.draw.rectangle([(85, 10), (130, 60)], fill="BLUE")

            logging.info("draw circle")
            self.draw.arc((150, 15, 190, 55), 0, 360, fill=(0, 255, 0))
            self.draw.ellipse((150, 65, 190, 105), fill=(0, 255, 0))

            logging.info("draw text")
            Font1 = ImageFont.truetype("../Font/Font01.ttf", 25)
            Font2 = ImageFont.truetype("../Font/Font01.ttf", 35)
            Font3 = ImageFont.truetype("../Font/Font02.ttf", 32)

            self.draw.rectangle([(0, 65), (140, 100)], fill="WHITE")
            self.draw.text((5, 68), "Hello world", fill="BLACK", font=Font1)
            self.draw.rectangle([(0, 115), (190, 160)], fill="RED")
            self.draw.text((5, 118), "WaveShare", fill="WHITE", font=Font2)
            self.draw.text((5, 160), "1234567890", fill="GREEN", font=Font3)
            text = "微雪电子"
            self.draw.text((5, 200), text, fill="BLUE", font=Font3)
            image1 = image1.rotate(180)
            self.disp.ShowImage(image1)

        except IOError as e:
            logging.info("DisplayController error: {}".format(e))

    def __del__(self):
        self.disp.module_exit()
        print("DisplayController destructor called.")
