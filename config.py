import tkinter.filedialog
import customtkinter as ctk
import os

with open("config.txt", "r") as f:
    lines = f.readlines()
    targetEncDir = lines[0].replace("Target_Encrypt_dir:", "").replace('\"', "").replace("\n", "")
    targetDecDir = lines[1].replace("Target_Decrypt_dir:", "").replace('\"', "").replace("\n", "")
    toRemove = lines[2].replace("Remove_Files:", "").replace("\n", "")

def selectEncFolder():
    encFolder = tkinter.filedialog.askdirectory(title='Pick a Folder to put the Encrypted files', initialdir='./')
    lines[0] = "Target_Encrypt_dir:\""+encFolder+"\""

def selectDecFolder():
    decFolder = tkinter.filedialog.askdirectory(title='Pick a Folder to put the Decrypted files', initialdir='./')
    lines[1] = "Target_Decrypt_dir:\""+decFolder+"\""

def toRemoveFunc():
    getRadio = radio_var.get()
    if (getRadio == 1):
        lines[2] = "Remove_Files:True\n"
    elif (getRadio == 2):
        lines[2] = "Remove_Files:False\n"

def saveConfig():
    global lines
    for i in range(len(lines)):
        lines[i] += "\n"
    with open("config.txt", "w") as f:
        f.writelines(lines)
    exit()

def submitEnc():
    global lines
    if (os.path.exists(targEncDirInput.get()) == False):
        encPath = lines[0].replace("Target_Encrypt_dir:", "").replace('\"', "").replace("\n", "")
        targEncDirInput.delete(0, ctk.END)
        targEncDirInput.insert(0, encPath)

def submitDec():
    global lines
    if (os.path.exists(targDecDirInput.get()) == False):
        decPath = lines[1].replace("Target_Decrypt_dir:", "").replace('\"', "").replace("\n", "")
        targDecDirInput.delete(0, ctk.END)
        targDecDirInput.insert(0, decPath)

root = ctk.CTk()
root.geometry("750x500")

targEncDirLabel = ctk.CTkLabel(root, text="Target Encryption Directory")
targEncDirLabel.pack()
targEncDirInput = ctk.CTkEntry(root, placeholder_text=targetEncDir) # put placeholder_text
targEncDirInput.pack()
targEncDirButton = ctk.CTkButton(root, command=selectEncFolder, text="Select a Folder")
targEncDirButton.pack()
targDecDirSubmit = ctk.CTkButton(root, command=submitEnc, text="Submit")
targDecDirSubmit.pack()

targDecDirLabel = ctk.CTkLabel(root, text="Target Decryption Directory")
targDecDirLabel.pack()
targDecDirInput = ctk.CTkEntry(root, placeholder_text=targetDecDir)
targDecDirInput.pack()
targDecDirButton = ctk.CTkButton(root, command=selectDecFolder, text="Select a Folder")
targDecDirButton.pack()
targDecDirSubmit = ctk.CTkButton(root, command=submitDec, text="Submit")
targDecDirSubmit.pack()

removeFileLabel = ctk.CTkLabel(root, text="Remove Files after Encryption/Decryption")
removeFileLabel.pack()

radio_var = tkinter.IntVar(value=0)
radiobutton_1 = ctk.CTkRadioButton(root, text="True", command=toRemoveFunc, variable= radio_var, value=1)
radiobutton_1.pack()
radiobutton_2 = ctk.CTkRadioButton(root, text="False", command=toRemoveFunc, variable= radio_var, value=2)
radiobutton_2.pack()

saveButton = ctk.CTkButton(root, command=saveConfig, text="Save & Exit")
saveButton.pack()

root.mainloop()
