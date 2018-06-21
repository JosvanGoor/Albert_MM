import core.module as module
import io
import json

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

class MemeModule(module.Module):

    def __init__(self):
        self.load_db()

    async def handle_message(self, message):
        #if not message.channel.name == "de-dankste-memes":
        #    return

        args = message.content.split(" ")
        
        if await super().handle_message(message):
            return

        if len(args) == 2:
            if args[1] == "list":
                msg = "Memes:\r\n"
                for key in self.data.keys():
                    msg += "    - {}\r\n".format(key)
                await module.dc_client.send_message(message.channel, msg)
                return



        if len(args) <= 3:
            await module.dc_client.send_message(message.channel, "I no understand :(")
            return

        # return with image

        flavor = args[1]

        buffer = message.content.split('"')
        del buffer[0]

        lines = []
        for line in buffer:
            if line.strip() == "":
                continue
            
            lines.append(line)

        if not flavor in self.data:
            await module.dc_client.send_message(message.channel, "No original jokes please!")
            return

        meme = self.data[flavor]
        image = Image.open("data/memes/{}".format(self.data[flavor]["file"]))
        
        if len(lines) == 0:
            await module.dc_client.send_message(message.channel, "There a joke in there?")
            return

        if not draw_text(image, "top", lines[0]):
           await module.dc_client.send_message(message.channel, "Less eleborate my dude!")
           return
        if len(lines) > 1:
           if not draw_text(image, "bottom", lines[1]):
               await module.dc_client.send_message(message.channel, "Less eleborate friendo!")
               return

        with open("data/memes/temporary_image.png", "wb+") as file:
            image.save(file)

        await module.dc_client.send_file(message.channel, "data/memes/temporary_image.png")


    def get_filter(self):
        pass

    def help_message(self):
        msg = "MemeModule help\r\n"
        msg += "Dont let your meme's be dreams!\r\n\r\n"
        msg += "Usage:\r\n"
        msg += "    !meme list - Prints out the names of the available templates.\r\n"
        msg += "    !meme <template name> \"text1\" \"text2\" - To generate a meme"
        return msg


    def short_status(self):
        return "MemeModule: Kek!"

    def status(self):
        return short_status()

    def load_db(self):
        with open("data/memes/data.json", "r") as file:
            self.data = json.load(file)


#
#   MEME STUFF
#

class PlacementError(Exception):
    pass

class Request:
    def __init__(self, format, lines):
        self.format = format
        self.lines = lines

fonts = \
[
    ImageFont.truetype("impact.ttf", 52),
    ImageFont.truetype("impact.ttf", 45),
    ImageFont.truetype("impact.ttf", 38),
    ImageFont.truetype("impact.ttf", 31),
    ImageFont.truetype("impact.ttf", 24),
    ImageFont.truetype("impact.ttf", 20),
    ImageFont.truetype("impact.ttf", 15)
]

def draw_outlined(image, draw, font, text, x, y):
    draw.text((x - 2, y - 2), text, (0, 0, 0), font=font)
    draw.text((x + 2, y - 2), text, (0, 0, 0), font=font)
    draw.text((x - 2, y + 2), text, (0, 0, 0), font=font)
    draw.text((x + 2, y + 2), text, (0, 0, 0), font=font)
    draw.text((x, y), text, (255, 255, 255), font=font)


def center_text(image, draw, font, text):
    w, h = draw.textsize(text, font)
    return (image.width / 2) - (w / 2)


def linelen(draw, font, text):
    w, h = draw.textsize(text, font)
    return w

def _draw_text(image, font, place, text):
    draw = ImageDraw.Draw(image)

    ascent, descent = font.getmetrics()
    height = ascent + descent

    w, h = draw.textsize(text, font)
    if w < (image.width - 20):
        if place == "top":
            draw_outlined(image, draw, font, text, center_text(image, draw, font, text), 0)
        else:
            draw_outlined(image, draw, font, text, center_text(image, draw, font, text), image.height - height)
        return
    
    line1 = text.split(" ")
    line2 = []

    while linelen(draw, font, " ".join(line1)) >= (image.width - 20):
        if len(line1) == 0: 
            break
        line2.insert(0, line1.pop(len(line1)-1))

    if len(line1) == 0 or linelen(draw, font, " ".join(line2)) >= (image.width - 20):
        raise PlacementError()
        return

    if place == "top":
        x = center_text(image, draw, font, " ".join(line1))
        draw_outlined(image, draw, font, " ".join(line1), x, 0)
        x = center_text(image, draw, font, " ".join(line2))
        draw_outlined(image, draw, font, " ".join(line2), x, height)
    else:
        x = center_text(image, draw, font, " ".join(line1))
        draw_outlined(image, draw, font, " ".join(line1), x, image.height - (2*height))
        x = center_text(image, draw, font, " ".join(line2))
        draw_outlined(image, draw, font, " ".join(line2), x, image.height - height)

def draw_text(image, place, text):
    for font in fonts:
        try:
            _draw_text(image, font, place, text)
            return True
        except PlacementError:
            pass
    return False
    