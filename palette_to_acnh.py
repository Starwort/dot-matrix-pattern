from time import sleep

import pyautogui
import pyperclip

from hex_to_acnh import convert

if __name__ == "__main__":
    from acnh_constants import hue_width, sat_width, val_width

    hue_slider_scale = 1
    sat_slider_scale = 1
    val_slider_scale = 1

    for i in range(3, 0, -1):
        print(f"Starting in {i} seconds... ", end="\r")
        sleep(1)

    old_sel = pyperclip.paste()
    for colour in range(15):
        pyautogui.hotkey("shift", "tab")
        pyautogui.typewrite(str(colour))
        pyautogui.press("tab")
        pyautogui.hotkey("ctrl", "c")
        hex = pyperclip.paste()
        nh, ns, nv = convert(int(hex, 16))
        hue_slider = ["░" for i in range(hue_width)]
        hue_slider[nh] = "█"
        sat_slider = ["[]" for i in range(sat_width)]
        sat_slider[ns] = "██"
        val_slider = ["[]" for i in range(val_width)]
        val_slider[nv] = "██"

        print(f"Colour {colour} (#{hex.upper()}) is:  ")
        print("".join(i * hue_slider_scale for i in hue_slider))
        print("".join(i * sat_slider_scale for i in sat_slider))
        print("".join(i * val_slider_scale for i in val_slider))
    pyperclip.copy(old_sel)
