from flask import Flask, request, send_from_directory,send_file
from urllib.parse import unquote
import PIL, os
from PIL import Image, ImageDraw, ImageFont
import random
import requests
from io import BytesIO
from random import choice,randint
TEMPLATE_WIDTH = 574
TEMPLATE_HEIGHT = 522
TEMPLATE_COORDS = (75, 45, 499, 373)
PADDING = 10
app = Flask(__name__)
def drawXAxisCenteredText(image, text, font, size, pos_y):
    draw = ImageDraw.Draw(image)
    textFont = ImageFont.truetype(font, size)
    textWidth = textFont.getsize(text)[0]

    while textWidth >= TEMPLATE_WIDTH - PADDING * 2:
        textFont = ImageFont.truetype(font, size)
        textWidth = textFont.getsize(text)[0]
        size -= 1

    draw.text(((TEMPLATE_WIDTH - textWidth) / 2, pos_y), text, font = textFont)

def getSizeFromArea(area):
    return (area[2] - area[0], area[3] - area[1])
@app.route('/s/<path:path>')
def send_js(path):
    return send_from_directory('static', path)

@app.route("/gen-demotivator/<str1>/<str2>")
@app.route("/gen-demotivator/<str1>")
@app.route("/gen-demotivator")
@app.route("/gen-demotivator/<str1>/<str2>/")
@app.route("/gen-demotivator/<str1>/")
@app.route("/gen-demotivator/")
def demote(str1="",str2=""):
    TEMPLATE_FILENAME = 'template.jpg'
    EXTENSIONS = ['.jpg', '.png']
    str1=str(str1)
    str2=str(str2)
    UPPER_FONT = 'font.ttf'
    UPPER_SIZE = 45
    UPPER_FONT_Y = 390
    LOWER_FONT = 'font.ttf'
    LOWER_SIZE = 14
    LOWER_FONT_Y = 450



    imgio=BytesIO()
    frame = PIL.Image.open(TEMPLATE_FILENAME)
    hh=randint(200,1500)
    demot = PIL.Image.open(requests.get(f"https://picsum.photos/{hh}/{hh}", stream=True).raw)
    demot = demot.resize(getSizeFromArea(TEMPLATE_COORDS), PIL.Image.ANTIALIAS)
    frame.paste(demot, TEMPLATE_COORDS)

    drawXAxisCenteredText(frame, str1,
                          UPPER_FONT, UPPER_SIZE,
                          UPPER_FONT_Y)
    drawXAxisCenteredText(frame, str2,
                          LOWER_FONT, LOWER_SIZE,
                          LOWER_FONT_Y)
    frame = frame.convert("RGB")
    frame.save(imgio, 'JPEG', quality=70)
    imgio.seek(0)
    return send_file(imgio, mimetype='image/jpeg')

if __name__ == "__main__":
    app.run()
