import logging
from collections import deque

from PIL import Image, ImageDraw, ImageFont

from src.states import DISPLAY_MODE, MENU_STATE, WORKING_LANGUAGE, WORKING_MODE

MAX_AMOUNT_OF_LINES = 10


class DisplayController:
    disp = None

    def __init__(self):
        logging.info("Hello DisplayController!")
        self.mode = DISPLAY_MODE.VISUAL

        logging.basicConfig(level=logging.INFO)

        self.states_map = {
            WORKING_LANGUAGE.ENGLISH: "english",
            WORKING_LANGUAGE.FRENCH: "french",
            WORKING_MODE.CONVERSATION_MODE: "./resources/conversation.jpg",
            WORKING_MODE.STORY_MODE: "./resources/story.jpg",
            MENU_STATE.LISTENING_PROMPT: "./resources/listening.jpg",
            MENU_STATE.LISTENING_PROMPT_FINISHED: "./resources/validate.jpg",
            MENU_STATE.GENERATING_PROMPT: "./resources/listenup.jpg",
        }

        self.log_queue: deque = deque(maxlen=MAX_AMOUNT_OF_LINES)
        self.font = ImageFont.truetype("./resources/Roboto-Regular.ttf", 20)

        try:
            from src.external.apa102 import APA102
            from src.external.LCD_2inch import LCD_2inch

            # disable the ReSpeaker LED because it collideds with the display
            led_strip = APA102(num_led=3)
            led_strip.clear_strip()
            led_strip.cleanup()

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

            # logging.info("show image")
            # image = Image.open("../pic/LCD_2inch.jpg")
            # image = image.rotate(180)
            # self.disp.ShowImage(image)
            # time.sleep(1)

            # Create blank image for drawing.
            # image1 = Image.new("RGB", (self.disp.height, self.disp.width), "WHITE")
            # self.draw = ImageDraw.Draw(image1)

            # logging.info("draw point")

            # self.draw.rectangle((5, 10, 6, 11), fill="BLACK")
            # self.draw.rectangle((5, 25, 7, 27), fill="BLACK")
            # self.draw.rectangle((5, 40, 8, 43), fill="BLACK")
            # self.draw.rectangle((5, 55, 9, 59), fill="BLACK")

            # logging.info("draw line")
            # self.draw.line([(20, 10), (70, 60)], fill="RED", width=1)
            # self.draw.line([(70, 10), (20, 60)], fill="RED", width=1)
            # self.draw.line([(170, 15), (170, 55)], fill="RED", width=1)
            # self.draw.line([(150, 35), (190, 35)], fill="RED", width=1)

            # logging.info("draw rectangle")
            # self.draw.rectangle([(20, 10), (70, 60)], fill="WHITE", outline="BLUE")
            # self.draw.rectangle([(85, 10), (130, 60)], fill="BLUE")

            # logging.info("draw circle")
            # self.draw.arc((150, 15, 190, 55), 0, 360, fill=(0, 255, 0))
            # self.draw.ellipse((150, 65, 190, 105), fill=(0, 255, 0))

            # logging.info("draw text")
            # Font1 = ImageFont.truetype("../Font/Font01.ttf", 25)
            # Font2 = ImageFont.truetype("../Font/Font01.ttf", 35)
            # Font3 = ImageFont.truetype("../Font/Font02.ttf", 32)

            # self.draw.rectangle([(0, 65), (140, 100)], fill="WHITE")
            # self.draw.text((5, 68), "Hello world", fill="BLACK", font=Font1)
            # self.draw.rectangle([(0, 115), (190, 160)], fill="RED")
            # self.draw.text((5, 118), "WaveShare", fill="WHITE", font=Font2)
            # self.draw.text((5, 160), "1234567890", fill="GREEN", font=Font3)
            # text = "微雪电子"
            # self.draw.text((5, 200), text, fill="BLUE", font=Font3)
            # image1 = image1.rotate(180)
            # self.disp.ShowImage(image1)

        except IOError as e:
            logging.info("DisplayController error: {}".format(e))
        except FileNotFoundError as e:
            logging.info("DisplayController error: {}".format(e))

    def stop(self):
        if self.disp is not None:
            self.disp.module_exit()
            self.disp = None

        logging.info("DisplayController destructor called.")

    def change_mode(self, target_mode: DISPLAY_MODE):
        self.mode = DISPLAY_MODE(not bool(int(target_mode.value)))
        logging.info("Changing display mode to: {}".format(self.mode))

    def update_dev(self):
        if self.disp is not None:
            self.disp.clear()

            # Create blank image for drawing.
            image1 = Image.new("RGB", (self.disp.height, self.disp.width), "WHITE")
            self.draw = ImageDraw.Draw(image1)

            for i in range(0, len(self.log_queue)):
                self.display_text(self.log_queue[i], i)

            self.disp.ShowImage(image1)

    def update(
        self, state: WORKING_LANGUAGE | WORKING_MODE | DISPLAY_MODE | MENU_STATE
    ):
        if self.mode == DISPLAY_MODE.VISUAL and state in self.states_map:
            self.display_image(self.states_map[state])

    def display_text(self, text, line):
        self.draw.text((5, 5 + line * 20), text=text, fill="BLACK", font=self.font)

        # self.draw.text((5, 68), "Hello world", fill="BLACK", font=Font1)
        # self.draw.text((5, 118), "WaveShare", fill="WHITE", font=Font2)
        # self.draw.text((5, 160), "1234567890", fill="GREEN", font=Font3)

    def display_image(self, image_path):
        logging.info("Display image {}".format(image_path))
        image = Image.open(image_path)
        # image = image.rotate(180)

        if self.disp is not None:
            self.disp.clear()
            self.disp.ShowImage(image)

    def push_log_to_display_queue(self, text: str):
        self.log_queue.append(text)
        # print("Received log: {}".format(text))
        if self.mode == DISPLAY_MODE.DEV:
            self.update_dev()
