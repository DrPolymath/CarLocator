from tkinter import StringVar

from Main import main

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from PIL import ImageTk, Image

from djitellopy import tello
import cv2
import time

root = ttk.Window()
root.geometry("600x350")
root.title("Car Locator")
input_text = StringVar()

logo = ImageTk.PhotoImage(Image.open("Car Locator.png"))
print(Image.open("Car Locator.png"))
title = ttk.Label(root, image=logo)
title.place(relx=.5, rely=.2, anchor=CENTER)

inputFrame = ttk.Frame(root)
inputFrame.place(relx=.5, rely=.6, anchor=CENTER)

inputLabel = ttk.Label(inputFrame, text="Number Plate", padding=10)
inputLabel.grid(row=0, column=0)

inputField = ttk.Entry(inputFrame, textvariable=input_text)
inputField.grid(row=0, column=1)


def search():
    global outputImage

    donna = tello.Tello()
    donna.connect()

    donna.streamon()

    donna.takeoff()

    i = 0
    image = None
    while True:
        time.sleep(2)
        donna.move_right(40)
        time.sleep(3)
        img = donna.get_frame_read().frame
        time.sleep(1)
        scanned = main(img)

        if scanned.replace(" ", "") == input_text.get():
            print('Plate number matched!')
            donna.move_back(20)
            time.sleep(2)
            image = donna.get_frame_read().frame
            break
        else:
            i += 1
            print('Plate number not matched! Continue searching...')

        if (i == 5):
            break
    retDistance = (i + 1) * 40
    print(retDistance)
    donna.move_left(retDistance)
    donna.land()

    if image is not None:
        cv2.imshow("Location of your car at Lot " + str(i + 1), image)
        cv2.waitKey(0)
    else:
        print("Your car cannot be found")


searchButton = ttk.Button(inputFrame, text="Search", command=search)
searchButton.grid(row=1, columnspan=2)

root.mainloop()
