from kivy.utils import get_color_from_hex


APP_BG = get_color_from_hex("#FBF5EC")
CARD_BG = get_color_from_hex("#FFFAF2")
INPUT_BG = get_color_from_hex("#F3E9DB")
BORDER = get_color_from_hex("#E6D8C6")
PRIMARY = get_color_from_hex("#B96F50")
PRIMARY_PRESSED = get_color_from_hex("#A25C40")
SECONDARY = get_color_from_hex("#8FAE8B")
SECONDARY_DARK = get_color_from_hex("#6F8F6C")
HONEY = get_color_from_hex("#E8B96A")
TEXT_PRIMARY = get_color_from_hex("#4A3B32")
TEXT_SECONDARY = get_color_from_hex("#8C7B6E")
SUCCESS = get_color_from_hex("#7FA77F")
ERROR = get_color_from_hex("#C96B5E")
WHITE = get_color_from_hex("#FFF8EE")


def rounded_rect(radius=18):
    return {"radius": [radius, radius, radius, radius]}
