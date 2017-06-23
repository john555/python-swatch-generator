"""
This is an example of how to use the Pyhton Image Library (PIL) module.

"""
import sys
from string import Template
from PIL import Image

IMAGE_FILE = "images/image1.jpg"
TEMPLATE_FILE = "templates/template.html"
OUTPUT_FILE = "index.html"
MAX_DEPTH = 3
RED_INDEX = 0
GREEN_INDEX = 1
BLUE_INDEX = 2

def main():
    """ This is the main function """
    image = Image.open(IMAGE_FILE, 'r')
    pixels = list(image.getdata())
    swatch = quantize(pixels, 0)
    render(swatch, IMAGE_FILE)

def quantize(pixels, depth=0):
    """ Returns a list of colors (color swatch)"""
    index = compute_highest_range_index(pixels)
    pixels = sorted(pixels, key=lambda x: x[index])
    length = len(pixels)
    
    if depth == MAX_DEPTH:

        red, green, blue = 0, 0, 0

        for pixel in pixels:
            red += pixel[RED_INDEX]
            green += pixel[GREEN_INDEX]
            blue += pixel[BLUE_INDEX]

        red = red // length
        green = green // length
        blue = blue // length

        return [(red, green, blue)]
    
    mid = length // 2
    result = []
    result.extend(quantize(pixels[0: mid], depth + 1))
    result.extend(quantize(pixels[mid+1:], depth + 1))
    return result

def compute_highest_range_index(pixels):
    """ Returns the index of the channel with the highest range """
    r_min, r_max = sys.maxsize, -sys.maxsize
    g_min, g_max = sys.maxsize, -sys.maxsize
    b_min, b_max = sys.maxsize, -sys.maxsize

    for pixel in pixels:
        r_min = min(r_min, pixel[RED_INDEX])
        r_max = max(r_max, pixel[RED_INDEX])
        g_min = min(g_min, pixel[GREEN_INDEX])
        g_max = max(g_max, pixel[GREEN_INDEX])
        b_min = min(b_min, pixel[BLUE_INDEX])
        b_max = max(b_max, pixel[BLUE_INDEX])

    r_range = r_max - r_min
    g_range = g_max - g_min
    b_range = b_max - b_min

    min_range = min(r_range, g_range, b_range)

    if min_range == r_range:
        return RED_INDEX
    if min_range == g_range:
        return GREEN_INDEX

    return BLUE_INDEX

def render(swatch, image_src):
    """ Generates the html file to display the results """
    html = load_template(TEMPLATE_FILE)
    swatches_html = ""
    for color in swatch:
        div = "<div class=\"flex-center\" style=\"background-color: rgb{};\"></div>"
        div = div.format(color)
        swatches_html += div
    html_template = Template(html)
    html = html_template.substitute(dict(image_src=image_src, swatches=swatches_html))
    write_file(OUTPUT_FILE, html)

def load_template(file):
    """ Returns a string containing the content of specified file. """
    file_handle = open(file, "r")
    result = ""
    for line in file_handle.readlines():
        result += line
    file_handle.close()
    return result

def write_file(file_name, data):
    """ Writes data to a file """
    file_handler = open(file_name, "w")
    file_handler.write(data)
    file_handler.close()

if __name__ == "__main__":
    main()
