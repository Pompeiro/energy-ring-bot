# -*- coding: utf-8 -*-
"""
Created on Mon Feb  8 08:18:41 2021

@author: janusz
"""
import logging
import time

import keyboard
import pyautogui
import pywintypes
from win32gui import GetForegroundWindow, GetWindowText

logging.basicConfig(level=logging.DEBUG)


pyautogui.PAUSE = 0.01
pyautogui.MINIMUM_DURATION = 0.01
pyautogui.FAILSAFE = False

RING_SLOT = (1762, 313)
ARROW_SLOT = (1838, 313)
PADDING_X = 35
PADDING_Y = 25
ARROW_REGION = (
    ARROW_SLOT[0] - PADDING_X,
    ARROW_SLOT[1] - PADDING_Y,
    ARROW_SLOT[0] + PADDING_X,
    ARROW_SLOT[1] + PADDING_Y,
)
RING_REGION = (
    RING_SLOT[0] - PADDING_X,
    RING_SLOT[1] - PADDING_Y,
    RING_SLOT[0] + PADDING_X,
    RING_SLOT[1] + PADDING_Y,
)
BACKPACK_FIRST_SLOT = (1767, 460)
BACKPACK_REGION = (1740, 426, 1912, 630)
BACKPACK_AND_SLOTS_REGION = (1738, 285, 1912, 630)
STATUS_BAR_REGION = (1742, 354, 1814, 372)


ERING_IMG = "images/ering.jpg"
BUFF_IMG = "images/buff.jpg"
ARROW_IMG = "images/arrow.jpg"
RING_IMG = "images/ring.jpg"


def activate_window(mode, delay=0.05):
    """


    Parameters
    ----------
    mode : "tibia"
    delay : Delay between actions. The default is 0.5.

    Returns
    -------
    None.

    """

    logging.debug("Function activate_window() called with passed: %s.", mode)
    logging.info("Current active window: %s", GetWindowText(GetForegroundWindow()))
    if mode == "tibia":
        window = pyautogui.getWindowsWithTitle("Kasteria - Tibijka")[0]
        window_text = "Kasteria - Tibijka"
    if GetWindowText(GetForegroundWindow()) != window_text:
        logging.info("active window != desired window, window activation goes on")
        window.minimize()
        time.sleep(delay)
        window.restore()
        window.activate()
        time.sleep(delay)
    logging.info("Current active window: %s", GetWindowText(GetForegroundWindow()))

    logging.debug("Function activate_window end.")


def back_to_mouse_position(func, **kwargs):
    """
    Save mouse position before function call, and then move mouse back to starting position.

    Parameters
    ----------
    func : function that need to be done.
    **kwargs :

    Returns
    -------
    None.

    """
    logging.debug("Function back_to_mouse_position() called.")
    start = pyautogui.position()
    logging.info("Start mouse position: %s", start)
    func(**kwargs)
    pyautogui.moveTo(start)
    logging.info("Start mouse position: %s", start)

    logging.debug("Function back_to_mouse_position() end.")


def slide(start, meta):
    """
    Slides object in game from start to meta point.

    Parameters
    ----------
    start : slide start point.
    meta : slide meta point.

    Returns
    -------
    None.

    """
    logging.debug("Function slide() called.")
    logging.info("start = %s meta = %s", start, meta)
    if start == RING_SLOT:
        logging.info("start position: ring slot")
    elif start == ARROW_SLOT:
        logging.info("start position: arrow slot")
    elif start == BACKPACK_FIRST_SLOT:
        logging.info("start position: bp first slot")
    else:
        logging.info("start position not in predefined positions")
    if meta == RING_SLOT:
        logging.info("meta position: ring slot")
    elif meta == ARROW_SLOT:
        logging.info("meta position: arrow slot")
    elif meta == BACKPACK_FIRST_SLOT:
        logging.info("meta position: bp first slot")
    pyautogui.moveTo(start)
    time.sleep(0.03)
    pyautogui.mouseDown()
    pyautogui.moveTo(meta)
    pyautogui.mouseUp()
    time.sleep(0.03)
    logging.debug("Function slide() end.")


def check_buff():
    buff_center = pyautogui.locateCenterOnScreen(
        BUFF_IMG, confidence=0.8, region=STATUS_BAR_REGION
    )
    return buff_center


def is_arrow_empty():
    arrow_slot_center = pyautogui.locateCenterOnScreen(
        ARROW_IMG, confidence=0.8, region=ARROW_REGION
    )
    return arrow_slot_center


def is_ring_empty():
    ring_slot_center = pyautogui.locateCenterOnScreen(
        RING_IMG, confidence=0.8, region=RING_REGION
    )
    return ring_slot_center


def slide_on_hotkey():
    """
    Locate energy ring, and then slide it to desired position(equip or unequip).

    Returns
    -------
    None.

    """
    ring_center = pyautogui.locateCenterOnScreen(
        ERING_IMG, confidence=0.75, region=BACKPACK_AND_SLOTS_REGION
    )
    logging.info("ring_center: %s", ring_center)
    if is_ring_empty():
        logging.info("Ring slot is empty")
        back_to_mouse_position(func=slide, start=ring_center, meta=RING_SLOT)

    else:
        logging.info("ring slot is occupied")
        if is_arrow_empty():
            logging.info("arrow slot is empty")

            back_to_mouse_position(func=slide, start=ring_center, meta=ARROW_SLOT)
        else:
            logging.info("Arrow slot is occupied")
            back_to_mouse_position(
                func=slide, start=ring_center, meta=BACKPACK_FIRST_SLOT
            )


def main():
    activate_window("tibia")
    time.sleep(1)
    pyautogui.moveTo(is_arrow_empty())
    while True:
        if keyboard.is_pressed("f8"):
            slide_on_hotkey()


if __name__ == "__main__":
    main()
