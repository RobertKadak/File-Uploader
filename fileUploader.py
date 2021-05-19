from urllib.parse import ParseResult, urljoin, urlparse
from tkinter import Tk, filedialog
from zipfile import ZipFile
import requests
import json
import os

class Main():
    def __init__(self):
        self.includedFiles = []
        self.includedDirs = []
        self.files = []
        self.running = True

    def main(self):
        while self.running:
            os.system('cls')
            print('1: Add file\n2: Add folder\nType help for more info\n')
            choise = input(':')

            if choise == 'help':
                os.system('cls')
                print('help - Show this page\n1 - Add file\n2 - Add folder\n3 - Upload\n')
                input('Enter to continue')

            if choise == '1':
                fileUploader.includeFile()

            if choise == '2':
                fileUploader.includeDir()

            if choise == '3':
                fileUploader.processFiles()

    def processFiles(self):
        for dir in self.includedDirs:
            for path, subdirs, files in os.walk(dir):
                for name in files:
                    self.files.append(path + '\\' + name)
        self.files.extend(self.includedFiles)

        self.files = set(self.files)

        zipObj = ZipFile('blob.zip', 'w')

        for file in self.files:
            zipObj.write(file)
        zipObj.close()
        fileUploader.upload()

    def upload(self):
        self.running = False
        with open("blob.zip", "rb") as f:
            r = requests.post("https://api.anonfiles.com/upload", files={"file": f})
        os.remove('blob.zip')

        uploadedUrl = urlparse(r.json()['data']['file']['url']['full']).geturl()

        with open("uploaded.txt", "w") as f:
            f.writelines(uploadedUrl)

    def includeFile(self):
        path = filedialog.askopenfilename()
        if path in self.includedFiles:
            return False
        else:
            self.includedFiles.append(path)
            return True

    def includeDir(self):
        path = filedialog.askdirectory()
        if path in self.includedDirs:
            return False
        else:
            self.includedDirs.append(path)
            return True

if __name__ == "__main__":
    root = Tk()
    root.withdraw()

    fileUploader = Main()
    fileUploader.main()