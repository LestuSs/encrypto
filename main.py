import binascii
from Crypto.Cipher import AES
from Crypto import Random
import base64
import os
import tkinter.filedialog
import tkinter as tk
from tkinter import PhotoImage
import subprocess

def create_custom_button(root, text, image_path, width, height):
    # Load the image (PNG format)
    image = PhotoImage(file=image_path)

    # Create a button with the image and text
    button = tk.Button(root, text=text, image=image, compound="top", width=width, height=height)
    button.image = image  # Keep a reference to the image to prevent garbage collection

    return button

def openEncrypt():
    subprocess.call([r"./venv\Scripts\python.exe", "encrypt.py"])
    exit()

def openDecrypt():
    subprocess.call([r"./venv\Scripts\python.exe", "decrypt.py"])
    exit()
def openConfig():
    subprocess.call([r"./venv\Scripts\python.exe", "config.py"])

def create_buttons():
    root = tk.Tk()
    root.title("Encrypto")
    root.geometry("400x200")

    # Set the desired button dimensions
    button_width = 125
    button_height = 150

    # Load images (replace paths with your actual PNG images)
    encrypt_img = PhotoImage(file="src/encrypt.png")
    decrypt_img = PhotoImage(file="src/decrypt.png")
    config_img = PhotoImage(file="src/config.png")

    # Create buttons
    button1 = tk.Button(root, text="Encrypt", image=encrypt_img, command=openEncrypt, width=button_width, height=button_height)
    button2 = tk.Button(root, text="Decrypt", image=decrypt_img, command=openDecrypt, width=button_width, height=button_height)
    button3 = tk.Button(root, text="Config", image=config_img, command=openConfig, width=button_width, height=button_height)

    # Pack the buttons horizontally
    button1.pack(side="left")
    button2.pack(side="left")
    button3.pack(side="left")

    root.mainloop()

if __name__ == "__main__":
    create_buttons()
