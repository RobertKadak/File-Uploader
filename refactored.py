from tkinter import Tk, filedialog, messagebox
from cryptography.fernet import Fernet
from urllib.parse import urlparse
from zipfile import ZipFile
from time import sleep
import requests
import easygui
import os

try:
    import colorama
    importColorama = True
except:
    importColorama = False

def info(text):
    if importColorama:
        print(colorama.Fore.YELLOW + '[?] ' + text + colorama.Style.RESET_ALL)
    else:
        print('[?] ' + text)
def success(text):
    if importColorama:
        print(colorama.Fore.GREEN + '[+] ' + text + colorama.Style.RESET_ALL)
    else:
        print('[+] ' + text)
def fail(text):
    if importColorama:
        print(colorama.Fore.RED + '[-] ' + text + colorama.Style.RESET_ALL)
    else:
        print('[-] ' + text)
colorama.init()

class fileUploader:
    def __init__(self):
        '''FileUploader'''

        self.running = True
        self.files = []
        self.dirs = []
        self.cryptionKey = self.config(os.path.expanduser('~') + '\\hBUJtrUbkLYPKbY.fukey')
        self.gui(self.cryptionKey)

    def gui(self, cryptionKey):
        '''FileUploader GUI'''

        while self.running:
            choise = easygui.indexbox('Upload files\n\nKey: ' + str(cryptionKey), 'File Uploader', ('Full Upload', 'Select File', 'Select Directory', 'Check files', 'Upload', 'Decrypt'))

            if choise == None:
                self.running = False

            elif choise == 0:
                fail('For now, Full Upload will only count files in drives and highest sized files.')
                self.fullUpload()

            elif choise == 1:
                self.includeFile()

            elif choise == 2:
                self.includeDir()

            elif choise == 3:
                info(str(self.files) + ', ' + str(self.dirs))

            elif choise == 4:
                self.upload()

            elif choise == 5:
                self.decryptFiles()

    def upload(self):
        self.zipFiles()
        self.encryptFiles()

        with open('blobEncrypted.zip', 'rb') as file:
            r = requests.post('https://api.anonfiles.com/upload', files={'file': file})
        os.remove('blobEncrypted.zip')
        os.remove('blob.zip')

        uploadedUrl = urlparse(r.json()['data']['file']['url']['full']).geturl()

        with open('uploaded.txt', 'a') as file:
            file.write(uploadedUrl + '\n')

    def decryptFiles(self):
        fernet = Fernet(self.cryptionKey)

        with open(filedialog.askopenfilename(), 'rb') as file:
            encrypted = file.read()

        original = fernet.decrypt(encrypted)

        with open('blobDecrypted.zip', 'wb') as file:
            file.write(original)

    def encryptFiles(self):
        fernet = Fernet(self.cryptionKey)

        with open('blob.zip', 'rb') as file:
            original = file.read()

        encrypted = fernet.encrypt(original)

        with open('blobEncrypted.zip', 'wb') as encrypted_file:
            encrypted_file.write(encrypted)

    def zipFiles(self):
        for dir in self.dirs:
            for path, subdirs, files in os.walk(dir):
                for name in files:
                    self.files.append(path + '\\' + name)

        zipObj = ZipFile('blob.zip', 'w')

        for file in self.files:
            zipObj.write(file)
        zipObj.close()

    def includeDir(self):
        dirChosen = filedialog.askdirectory()

        self.dirs.append(dirChosen)

    def includeFile(self):
        fileChosen = filedialog.askopenfilename()

        self.files.append(fileChosen)

    def fullUpload(self):
        drives = []
        count = 0
        highest = 0

        for drive in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            drive = drive + ':\\'
            if os.path.exists(drive):
                success('Found Drive: ' + drive)
                drives.append(drive)

        for dir in drives:
            for path, subdirs, files in os.walk(dir):
                for name in files:
                    try:
                        current = os.path.getsize(path + '\\' + name)
                    except:
                        current = 0
                    if current>highest:
                        highest = current
                        print('New Highest Sized File: ' + path + '\\' + name + ', with the size of: ' + str(highest) + ' bytes')
                    count += 1
            print('Files in drive ' + dir[0] + ': ' + str(count))
            count = 0

        print('Total Files: ' + str(count))


    def config(self, cryptionKeyPath):
        '''FileUploader Configuration'''

        cryptionKeyExists = os.path.exists(cryptionKeyPath)

        if (cryptionKeyExists):
            with open(cryptionKeyPath, 'rb') as configFile:
                cryptionKey = configFile.readline()

        if (cryptionKeyExists==False):
            with open(cryptionKeyPath, 'wb') as configFile:
                cryptionKey = Fernet.generate_key()
                configFile.write(cryptionKey)

        info('Key: ' + str(cryptionKey))
        return cryptionKey

if __name__ == '__main__':
    root = Tk()
    root.withdraw()
    Uploader = fileUploader()
