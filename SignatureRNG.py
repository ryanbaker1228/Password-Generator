"""
This module generates a random number based on a signature (or any other symbol) input through the mouse
"""
import math
import matplotlib.pyplot as plt

import pyautogui
import time


def SignatureRNG():
    wait_for_mouse_motion()
    signature = get_signature()
    signature_number(signature)

def wait_for_mouse_motion():
    mouse_moving = False
    mouseX, mouseY = pyautogui.position()
    points_queue = [(mouseX, mouseY)] * 100

    while not mouse_moving:
        mouseX, mouseY = pyautogui.position()

        points_queue.append((mouseX, mouseY))
        points_queue.pop(0)

        mouse_moving = len(set(points_queue)) > 1

    return

def get_signature() -> list:
    frequency = 10000
    stop_time = 0.1

    mouse_moving = True
    mouseX, mouseY = pyautogui.position()
    points_queue = [(mouseX, mouseY)] * int(stop_time * frequency)
    signature = [(mouseX, mouseY)]

    while (mouse_moving or len(signature) < int(stop_time * frequency)) and len(signature) <= frequency * 3:
        time.sleep(1 / frequency)
        mouseX, mouseY = pyautogui.position()

        points_queue.append((mouseX, mouseY))
        points_queue.pop(0)
        mouse_moving = len(set(points_queue)) > 1

        signature.append((mouseX, mouseY))


    signature = signature[0:len(signature) - int(stop_time * frequency)]

    return signature

def signature_number(signature: list):
    bitword_length = 256
    keys = []
    hash = 0
    length = len(signature)
    distance = sum(math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2) for (x1, y1), (x2, y2) in zip(signature, signature[1:]))

    for point in signature:
        keys.append((point[0] ** point[1]) % (2 ** bitword_length))

    for key in keys:
        hash ^= key

    print(str(bin(hash))[2:])





def display_signature(signature: list):
    x_coords, y_coords = zip(*signature)
    y_coords = [981 - y_val for y_val in y_coords]

    plt.scatter(x_coords, y_coords, marker='o', color='b', label='Points')
    plt.xlim(0, 1511)
    plt.ylim(0, 981)
    plt.show()
