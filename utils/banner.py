import pyfiglet
import random
from utils.colors import Color

def colored_print(text, color_code):
    print(f"{color_code}{text}"+Color.END)

def generate_banner():
    selected_fonts = ['standard', 'big', 'slant', 'small', 'shadow']
    selected_font = random.choice(selected_fonts)
    font = pyfiglet.Figlet(font=selected_font)
    ascii_banner = font.renderText("WX DevTools")
    color_codes = [Color.RED, Color.GREEN, Color.BLUE, Color.YELLOW, Color.CYAN, Color.PURPLE]
    selected_color = random.choice(color_codes)
    ascii_banner_with_author = ascii_banner.rstrip('\r\n')
    colored_print(ascii_banner_with_author, selected_color)