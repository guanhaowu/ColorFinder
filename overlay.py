from tkinter import *
from PIL import ImageDraw, ImageTk, Image
import win32gui
import win32con
import pyautogui


def createOverlay():
    # TODO: Create a top layered overlay.
    screen_width, screen_height = pyautogui.size()

    root = Tk()
    root.geometry('%dx%d' % (screen_width, screen_height)) ## screen size
    root.title("FindColor")
    root.attributes("-transparentcolor", "white", "-topmost", 1)
    root.config(bg='white')
    root.attributes("-alpha", 0.25)
    root.wm_attributes("-topmost", 1)
    bg = Canvas(root, width=screen_width, height=screen_height, bg='white')
    setClickThrough(bg.winfo_id())

    frame = ImageTk.PhotoImage


def drawOverlay(overlay, positions):
    # TODO: Fix the draw rectangle at position.
    for position in positions:
        xpos, ypos = position
        overlay.rectangle((xpos - 2, ypos - 2, xpos + 4, ypos + 4), outline='#23e06f', width=2)


def setClickThrough(hwnd):
    try:
        styles = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
        styles = win32con.WS_EX_LAYERED | win32con.WS_EX_TRANSPARENT
        win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, styles)
        win32gui.SetLayeredWindowAttributes(hwnd, 0, 255, win32con.LWA_ALPHA)
    except Exception as e:
        print(e)

