import binascii
from Crypto.Cipher import AES
from Crypto import Random
import base64
import os
import customtkinter as ctk
from tkinter import filedialog

with open("config.txt", "r") as config:
    configLines = config.readlines()
    targetDir = configLines[1].replace("Target_Decrypt_dir:", "").replace('\"', "").replace("\n", "")
    toRemove = configLines[2].replace("Remove_Files:", "").replace("\n", "")
    if (toRemove == "True"):
        toRemove = True
    else:
        toRemove = False
    if (os.path.isdir(targetDir) == False):
        os.mkdir(targetDir)

BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
unpad = lambda s : s[:-ord(s[len(s)-1:])]

def decrypt(key, enc):
    enc = base64.b64decode(enc)
    iv = enc[:16]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted = unpad(cipher.decrypt(enc[16:]))
    return decrypted.decode()  # Decode bytes to string

def decryptFile(inpFile, toReplace):
    keyFile = os.path.splitext(inpFile)[0]+"_keys.txt"
    decryptedFile = []
    with open(keyFile, 'r') as kf:
        keys = kf.readlines()
    with open(inpFile, 'r') as inpF:
        encLines = inpF.readlines()
    for i in range(len(keys)):
        keys[i] = binascii.unhexlify(keys[i].replace("\n", ""))
        encLines[i] = encLines[i].replace("\n", "").encode('utf-8')
        decryptedFile.append(decrypt(keys[i], encLines[i]))
    with open(targetDir+"/"+inpFile.replace(toReplace, ""), 'wb') as f:
        for line in decryptedFile:
            f.write(line.encode())

def list_all_files(directory):
    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            yield os.path.join(dirpath, filename)

def list_all_subfolders(directory):
    for dirpath, dirnames, filenames in os.walk(directory):
        for dirname in dirnames:
            yield os.path.join(dirpath, dirname)

def decryptFolder(dirname):
    all_files = list(list_all_files(dirname))
    all_subfolders = list(list_all_subfolders(dirname))
    toReplace = dirname[:dirname.index(os.path.basename(dirname))]
    if all_subfolders == []:
        os.makedirs(targetDir+"/"+os.path.basename(dirname))
    else:
        for folder in all_subfolders:
            os.makedirs(targetDir + "/" + str(folder).replace("\\", "/").replace(toReplace, ""), exist_ok=True)
    for file in all_files:
        if "_keys.txt" in file:
            pass
        else:
            decryptFile(file, toReplace)
    if (toRemove == True):
        for file in all_files:
            os.remove(file)
        for folder in all_subfolders:
            os.removedirs(folder)

def list_all_files(directory):
    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            yield os.path.join(dirpath, filename)

def list_all_subfolders(directory):
    for dirpath, dirnames, filenames in os.walk(directory):
        for dirname in dirnames:
            yield os.path.join(dirpath, dirname)

def clearEntries():
    fileEntry.delete(0, ctk.END)
    folderEntry.delete(0, ctk.END)

def pickFile():
    clearEntries()
    encFile = filedialog.askopenfilenames(title='Pick a file to Decrypt', initialdir='./')
    if len(encFile) > 1:
        filesToInsert = str(encFile[0])
        for item in encFile:
            if item != encFile[0]:
                filesToInsert = filesToInsert + "<" + str(item)
    fileEntry.insert(0, filesToInsert)

def pickFolder():
    clearEntries()
    encFolder = filedialog.askdirectory(title='Pick a folder to Decrypt', initialdir='./')
    folderEntry.insert(0, encFolder)

def fileSubmit():
    global dirErrorLabel, fileEntry
    fileToDecrypt = fileEntry.get()
    if ("<" in fileToDecrypt):
        filePaths = []
        for i in range(fileToDecrypt.count("<")):
            j = 0
            while True:
                if fileToDecrypt[j] == "<":
                    filePaths.append(fileToDecrypt[:j])
                    fileToDecrypt = fileToDecrypt[j+1:]
                    break
                j+=1
        filePaths.append(fileToDecrypt)
        for file in filePaths:
            if (os.path.exists(file) == True):
                toReplace = os.path.splitext(file)[0][:len(file)-len(os.path.basename(file))]
                decryptFile(file, toReplace)
                dirErrorLabel.destroy()
                dirErrorLabel = ctk.CTkLabel(root, text="Error, file/dir not found.", text_color="red")
            else:
                dirErrorLabel.pack()
    else:
        if (os.path.exists(fileToDecrypt) == True):
            toReplace = os.path.splitext(fileToDecrypt)[0][:len(fileToDecrypt)-len(os.path.basename(fileToDecrypt))]
            decryptFile(fileToDecrypt, toReplace)
            dirErrorLabel.destroy()
            dirErrorLabel = ctk.CTkLabel(root, text="Error, file/dir not found.", text_color="red")
        else:
            dirErrorLabel.pack()

def folderSubmit():
    global dirErrorLabel, folderEntry
    folderToDecrypt = folderEntry.get()
    if (os.path.exists(folderToDecrypt) == True):
        decryptFolder(folderToDecrypt)
        dirErrorLabel.destroy()
        dirErrorLabel = ctk.CTkLabel(root, text="Error, file/dir not found.", text_color="red")
    else:
        dirErrorLabel.pack()

root = ctk.CTk()
root.geometry("400x300")
root.title("File/Folder Decryption")
dirErrorLabel = ctk.CTkLabel(root, text="Error, file/dir not found.", text_color="red")

fileLabel = ctk.CTkLabel(root, text="Pick a file")
fileLabel.pack()
fileEntry = ctk.CTkEntry(root, placeholder_text="File Address")
fileEntry.pack()
filePick = ctk.CTkButton(root, text="Pick", command=pickFile)
filePick.pack()
fileDecrypt = ctk.CTkButton(root, text="Submit", command=fileSubmit)
fileDecrypt.pack()

folderLabel = ctk.CTkLabel(root, text="Pick a folder")
folderLabel.pack()
folderEntry = ctk.CTkEntry(root, placeholder_text="Folder Address")
folderEntry.pack()
folderPick = ctk.CTkButton(root, text="Pick", command=pickFolder)
folderPick.pack()
folderDecrypt = ctk.CTkButton(root, text="Submit", command=folderSubmit)
folderDecrypt.pack()


root.mainloop()