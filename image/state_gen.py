from PIL import Image, ImageDraw, ImageFont
import requests

def generate(icon, title, messages, members, created):

    if icon != None:

        p = requests.get(icon)
        out = open("image/icon.png", "wb")
        out.write(p.content)
        out.close()

        with Image.open("image/icon.png") as img_monastery:
            img_monastery.load()

    image = Image.open("image/frame1.png")
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("image/font.ttf", size=128)

    x1, y1, x2, y2 = font.getbbox(title)
    w = abs(x2 - x1)

    if icon != None:
        draw.text(((1920 - w + 102) / 2, (197)), title, font=font, align='center', fill='#FFFFFF')
        image.paste(img_monastery.resize((175, 175)), (w, 185))

    else:
        draw.text(((1920 - w) / 2, (197)), title, font=font, align='center', fill='#FFFFFF')

    x1, y1, x2, y2 = font.getbbox(f"Messages - {messages}")
    w = abs(x2 - x1)
    draw.text(((1920 - w) / 2, (427)), f"Messages - {messages}", font=font, align='center', fill='#FFFFFF')

    x1, y1, x2, y2 = font.getbbox(f"Members - {members}")
    w = abs(x2 - x1)
    draw.text(((1920 - w) / 2, (586)), f"Members - {members}", font=font, align='center', fill='#FFFFFF')

    x1, y1, x2, y2 = font.getbbox(f"Created on - {created}")
    w = abs(x2 - x1)
    draw.text(((1920 - w) / 2, (745)), f"Created on - {created}", font=font, align='center', fill='#FFFFFF')

    image.save("result.png")