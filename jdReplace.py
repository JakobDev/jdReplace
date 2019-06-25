#!/usr/bin/env python3
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QDir, QLocale
import glob
import sys
import os

def showMessageBox(title,text):
    messageBox = QMessageBox()
    messageBox.setWindowTitle(title)
    messageBox.setText(text)
    messageBox.setStandardButtons(QMessageBox.Ok)
    messageBox.exec_()

class TranslationHelper():
    def __init__(self, language):
        self.strings = {}
        currentDir = os.path.dirname(os.path.realpath(__file__))
        langPath = os.path.join(currentDir,"translation","en_GB.lang")
        self.readLanguageFile(langPath)
        langPath = os.path.join(currentDir,"translation",language + ".lang")
        if os.path.isfile(langPath):
            self.readLanguageFile(langPath)

    def readLanguageFile(self, path):
        with open(path) as f:
            content = f.readlines()
            for line in content:
                a,b = line.rstrip().split("=")
                self.strings[a] = b

    def translate(self, key):
        if key in self.strings:
            return self.strings[key]
        else:
            return key

class StartWindow(QWidget):
    def setup(self):
        self.texts = TranslationHelper(QLocale.system().name())
        self.directoryLabel = QLabel(self.texts.translate("label.directory"))
        self.directoryEdit = QLineEdit()
        self.directoryButton = QPushButton(self.texts.translate("button.browse"))
        self.inputTextLabel = QLabel(self.texts.translate("label.searchFor"))
        self.inputTextEdit = QPlainTextEdit()
        self.outputTextLabel = QLabel(self.texts.translate("label.replaceWith"))
        self.outputTextEdit = QPlainTextEdit()
        self.checkBox = QCheckBox(self.texts.translate("checkbox.searchSubdirectories"))
        self.progressBar = QProgressBar()
        self.aboutButton = QPushButton(self.texts.translate("button.about"))
        self.okButton = QPushButton(self.texts.translate("button.ok"))

        self.directoryEdit.setText(QDir.currentPath())
        self.directoryButton.clicked.connect(self.browse)
        self.aboutButton.clicked.connect(self.showAbout)
        self.okButton.clicked.connect(self.replaceFiles)
        self.progressBar.setValue(0)

        self.directoryLayout = QHBoxLayout()
        self.directoryLayout.addWidget(self.directoryLabel)
        self.directoryLayout.addWidget(self.directoryEdit)
        self.directoryLayout.addWidget(self.directoryButton)
        
        self.buttonLayout = QHBoxLayout()
        self.buttonLayout.addWidget(self.aboutButton)
        self.buttonLayout.addStretch(1)
        self.buttonLayout.addWidget(self.okButton)

        self.mainLayout = QVBoxLayout()
        self.mainLayout.addLayout(self.directoryLayout)
        self.mainLayout.addWidget(self.inputTextLabel)
        self.mainLayout.addWidget(self.inputTextEdit)
        self.mainLayout.addWidget(self.outputTextLabel)
        self.mainLayout.addWidget(self.outputTextEdit)
        self.mainLayout.addWidget(self.checkBox)
        self.mainLayout.addWidget(self.progressBar)
        self.mainLayout.addLayout(self.buttonLayout)
        
        self.setLayout(self.mainLayout)
        self.resize(650, 550)
        self.setWindowTitle("jdReplace")
        self.show()

    def browse(self):
        path = self.directoryEdit.text()
        if not os.path.isdir(path):
            path = QDir.currentPath()
        directory = QFileDialog.getExistingDirectory(self, self.texts.translate("filedialog.title"),path)

        if directory:
            self.directoryEdit.setText(directory)
    
    def showAbout(self):
        showMessageBox(self.texts.translate("about.title"),self.texts.translate("about.text").replace("\\n","\n"))

    def replaceFiles(self):
        path = self.directoryEdit.text()
        if not os.path.isdir(path):
            showMessageBox(self.texts.translate("messagebox.nodirectory.title"),self.texts.translate("messagebox.nodirectory.text").replace("{}",path))
            return
        searchText = self.inputTextEdit.toPlainText()
        if searchText == "":
            showMessageBox(self.texts.translate("messagebox.nosearchtext.title"),self.texts.translate("messagebox.nosearchtext.text"))
            return
        replaceText = self.outputTextEdit.toPlainText()
        if self.checkBox.checkState() == 0:
            dircontent = glob.iglob(os.path.join(path,"**"),recursive=False)
        else:
            dircontent = glob.iglob(os.path.join(path,"**"),recursive=True)
        filelist = []
        for item in dircontent:
            if not os.path.isdir(item):
                filelist.append(item)
        onePercent = len(filelist) / 100
        self.progressBar.setValue(0)
        progressValue = 0
        for filename in filelist:
            try:
                with open(filename, 'r') as file :
                    filedata = file.read()
                filedata = filedata.replace(searchText,replaceText)
                with open(filename, 'w') as file:
                    file.write(filedata)
            except:
                print(self.texts.translate("replace.error").replace("{}",filename))
            progressValue += 1
            self.progressBar.setValue(progressValue / onePercent)
        showMessageBox(self.texts.translate("messagebox.finished.title"),self.texts.translate("messagebox.finished.text"))

        
app = QApplication(sys.argv)
w = StartWindow()
w.setup()
sys.exit(app.exec_())

