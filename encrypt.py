import binascii
from Crypto.Cipher import AES
from Crypto import Random
import base64
import os
import customtkinter as ctk
from tkinter import filedialog

with open("config.txt", "r") as config:
    configLines = config.readlines()
    targetDir = configLines[0].replace("Target_Encrypt_dir:", "").replace('\"', "").replace("\n", "")
    toRemove = configLines[2].replace("Remove_Files:", "").replace("\n", "")
    if (toRemove == "True"):
        toRemove = True
    else:
        toRemove = False
    if (os.path.isdir(targetDir) == False):
        os.mkdir(targetDir)

BS = 16
def pad(s):
    return s + (BS - len(s.encode('utf-8')) % BS) * chr(BS - len(s.encode('utf-8')) % BS)

unpad = lambda s : s[:-ord(s[len(s)-1:])]

def create_key():
    key = os.urandom(16)
    return key

def encrypt(key, raw):
    raw = pad(raw)
    raw = raw.encode()  # Encode string to bytes
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return base64.b64encode(iv + cipher.encrypt(raw))

def encryptFile(fname):
    keyArr = []
    newFile = []
    with open(fname, "r", encoding='utf-8') as f:
        lines = f.readlines()
    for line in lines:
        newKey = create_key()
        keyArr.append(binascii.hexlify(newKey).decode('utf-8')+"\n")
        newFile.append(encrypt(newKey, line).decode('utf-8')+"\n")
    with open(targetDir+"/"+os.path.basename(fname), 'w') as nf:
        nf.writelines(newFile)
    with open(targetDir+"/"+os.path.basename(fname).replace(os.path.splitext(fname)[1], "")+"_keys.txt", 'w') as nk:
        nk.writelines(keyArr)

def encryptSpecific(original, target):
    keyArr = []
    newFile = []
    with open(original, "r", encoding='utf-8') as f:
        lines = f.readlines()
    for line in lines:
        newKey = create_key()
        keyArr.append(binascii.hexlify(newKey).decode('utf-8') + "\n")
        newFile.append(encrypt(newKey, line).decode('utf-8') + "\n")
    with open(target, 'w') as nf:
        nf.writelines(newFile)
    with open(os.path.splitext(target)[0] + "_keys.txt", 'w') as nk:
        nk.writelines(keyArr)

def list_all_files(directory):
    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            yield os.path.join(dirpath, filename)

def list_all_subfolders(directory):
    for dirpath, dirnames, filenames in os.walk(directory):
        for dirname in dirnames:
            yield os.path.join(dirpath, dirname)

def encryptFolder(dirname):
    all_files = list(list_all_files(dirname))
    all_subfolders = list(list_all_subfolders(dirname))
    toReplace = dirname[:dirname.index(os.path.basename(dirname))]
    for folder in all_subfolders:
        print(targetDir + "/" + str(folder).replace("\\", "/").replace(toReplace, ""))
        os.makedirs(targetDir + "/" + str(folder).replace("\\", "/").replace(toReplace, ""), exist_ok=True)
    for file in all_files:
        print(targetDir+"/"+str(file).replace("\\", "/").replace(toReplace, ""))
        encryptSpecific(file, targetDir+"/"+str(file).replace("\\", "/").replace(toReplace, ""))
    if (toRemove == True):
        for file in all_files:
            os.remove(file)
        for folder in all_subfolders:
            os.removedirs(folder)

def clearEntries():
    fileEntry.delete(0, ctk.END)
    folderEntry.delete(0, ctk.END)

def pickFile():
    clearEntries()
    encFile = filedialog.askopenfilenames(title='Pick a file to Encrypt', initialdir='./')
    if len(encFile) > 1:
        filesToInsert = str(encFile[0])
        for item in encFile:
            if item != encFile[0]:
                filesToInsert = filesToInsert + "<" + str(item)
    fileEntry.insert(0, filesToInsert)
def pickFolder():
    clearEntries()
    encFolder = filedialog.askdirectory(title='Pick a folder to Encrypt', initialdir='./')
    folderEntry.insert(0, encFolder)

def fileSubmit():
    global dirErrorLabel, fileEntry
    fileToEncrypt = fileEntry.get()
    if ("<" in fileToEncrypt):
        filePaths = []
        for i in range(fileToEncrypt.count("<")):
            j = 0
            while True:
                if fileToEncrypt[j] == "<":
                    filePaths.append(fileToEncrypt[:j])
                    fileToEncrypt = fileToEncrypt[j+1:]
                    break
                j+=1
        filePaths.append(fileToEncrypt)
        for file in filePaths:
            if (os.path.exists(file) == True):
                encryptFile(file)
                dirErrorLabel.destroy()
                dirErrorLabel = ctk.CTkLabel(root, text="Error, file/dir not found.", text_color="red")
            else:
                dirErrorLabel.pack()
    else:
        if (os.path.exists(fileToEncrypt) == True):
            encryptFile(fileToEncrypt)
            dirErrorLabel.destroy()
            dirErrorLabel = ctk.CTkLabel(root, text="Error, file/dir not found.", text_color="red")
        else:
            dirErrorLabel.pack()

def folderSubmit():
    global dirErrorLabel, folderEntry
    folderToEncrypt = folderEntry.get()
    if (os.path.exists(folderToEncrypt) == True):
        encryptFolder(folderToEncrypt)
        dirErrorLabel.destroy()
        dirErrorLabel = ctk.CTkLabel(root, text="Error, file/dir not found.", text_color="red")
    else:
        dirErrorLabel.pack()


root = ctk.CTk()
root.geometry("400x300")
root.title("File/Folder Encryption")
dirErrorLabel = ctk.CTkLabel(root, text="Error, file/dir not found.", text_color="red")

fileLabel = ctk.CTkLabel(root, text="Pick a file")
fileLabel.pack()
fileEntry = ctk.CTkEntry(root, placeholder_text="File Address")
fileEntry.pack()
filePick = ctk.CTkButton(root, text="Pick", command=pickFile)
filePick.pack()
fileEncrypt = ctk.CTkButton(root, text="Submit", command=fileSubmit)
fileEncrypt.pack()

folderLabel = ctk.CTkLabel(root, text="Pick a folder")
folderLabel.pack()
folderEntry = ctk.CTkEntry(root, placeholder_text="Folder Address")
folderEntry.pack()
folderPick = ctk.CTkButton(root, text="Pick", command=pickFolder)
folderPick.pack()
folderEncrypt = ctk.CTkButton(root, text="Submit", command=folderSubmit)
folderEncrypt.pack()


root.mainloop()