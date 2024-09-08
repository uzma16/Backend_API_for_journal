from colorthief import ColorThief
import colorsys


def color(image):
    rgb = ColorThief(image)
    color = rgb.get_color()
    hue, s, v = colorsys.rgb_to_hsv(color[0], color[1], color[2])
    hue_value = hue * 360
    return int(hue_value)
