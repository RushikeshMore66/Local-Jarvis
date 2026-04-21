import pyautogui
import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def capture_screen():
    screenshot = pyautogui.screenshot()
    screenshot.save("screen.png")
    return screenshot

def read_text():
    screenshot = capture_screen()
    text = pytesseract.image_to_string(screenshot)
    return text