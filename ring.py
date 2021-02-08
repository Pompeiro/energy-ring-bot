# -*- coding: utf-8 -*-
"""
Created on Mon Feb  8 08:18:41 2021

@author: janusz
"""
import pyautogui
import keyboard

RING_SLOT = (1760,310)
ARROW_SLOT = (1840,310)

while True:
    if keyboard.is_pressed("p"):
        print("You pressed p")
        break

def slide_from_arrow_to_ring():
    if keyboard.is_pressed("p"):
        pyautogui.moveTo(ARROW_SLOT)
        pyautogui.mouseDown()
        pyautogui.moveTo(RING_SLOT)
        pyautogui.mouseUp()

def main():
    slide_from_arrow_to_ring()

if __name__ == "__main__":
    main()