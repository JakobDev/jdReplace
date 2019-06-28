#!/usr/bin/env python3
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QDir, QLocale, Qt
from PyQt5.QtGui import QFont
import webbrowser
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

class AboutWindow(QWidget):
    def setup(self):
        self.titleLabel = QLabel("jdReplace Version " + version)
        self.descriptionLabel = QLabel(texts.translate("about.description"))
        self.copyrightLabel = QLabel("Copyright © 2019 JakobDev")
        self.licenseLabel = QLabel(texts.translate("about.license"))
        self.viewSourceButton = QPushButton(texts.translate("about.viewSource"))
        self.closeButton = QPushButton(texts.translate("about.close"))
        
        self.titleLabelFont = QFont()
        self.titleLabelFont.setBold(True)
        self.titleLabelFont.setPointSize(16)

        self.legalFont = QFont()
        self.legalFont.setPointSize(8)

        self.titleLabel.setFont(self.titleLabelFont)
        self.copyrightLabel.setFont(self.legalFont)
        self.licenseLabel.setFont(self.legalFont)

        self.titleLabel.setAlignment(Qt.AlignCenter)
        self.descriptionLabel.setAlignment(Qt.AlignCenter)
        self.copyrightLabel.setAlignment(Qt.AlignCenter)
        self.licenseLabel.setAlignment(Qt.AlignCenter)

        self.viewSourceButton.clicked.connect(self.viewSourceAction)
        self.closeButton.clicked.connect(self.closeAction)

        self.buttonLayout = QHBoxLayout()
        self.buttonLayout.addWidget(self.viewSourceButton)
        self.buttonLayout.addWidget(self.closeButton)

        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.titleLabel)
        self.mainLayout.addWidget(self.descriptionLabel)
        self.mainLayout.addWidget(self.copyrightLabel)
        self.mainLayout.addWidget(self.licenseLabel)
        self.mainLayout.addLayout(self.buttonLayout)
        
        self.setLayout(self.mainLayout)
        self.setWindowTitle(texts.translate("about.title"))
        
    def viewSourceAction(self):
        webbrowser.open("https://gitlab.com/JakobDev/jdReplace")

    def closeAction(self):
        self.close()

class StartWindow(QWidget):
    def setup(self):
        self.about = AboutWindow()
        self.about.setup()

        self.directoryLabel = QLabel(texts.translate("label.directory"))
        self.directoryEdit = QLineEdit()
        self.directoryButton = QPushButton(texts.translate("button.browse"))
        self.inputTextLabel = QLabel(texts.translate("label.searchFor"))
        self.inputTextEdit = QPlainTextEdit()
        self.outputTextLabel = QLabel(texts.translate("label.replaceWith"))
        self.outputTextEdit = QPlainTextEdit()
        self.checkBox = QCheckBox(texts.translate("checkbox.searchSubdirectories"))
        self.progressBar = QProgressBar()
        self.aboutButton = QPushButton(texts.translate("button.about"))
        self.okButton = QPushButton(texts.translate("button.ok"))

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
        directory = QFileDialog.getExistingDirectory(self, texts.translate("filedialog.title"),path)

        if directory:
            self.directoryEdit.setText(directory)
    
    def showAbout(self):
        self.about.show()

    def replaceFiles(self):
        path = self.directoryEdit.text()
        if not os.path.isdir(path):
            showMessageBox(texts.translate("messagebox.nodirectory.title"),texts.translate("messagebox.nodirectory.text").replace("{}",path))
            return
        searchText = self.inputTextEdit.toPlainText()
        if searchText == "":
            showMessageBox(texts.translate("messagebox.nosearchtext.title"),texts.translate("messagebox.nosearchtext.text"))
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
                print(texts.translate("replace.error").replace("{}",filename))
            progressValue += 1
            self.progressBar.setValue(progressValue / onePercent)
        showMessageBox(texts.translate("messagebox.finished.title"),texts.translate("messagebox.finished.text"))

  
version = "1.1" 
app = QApplication(sys.argv)
texts = TranslationHelper(QLocale.system().name())
w = StartWindow()
w.setup()
sys.exit(app.exec_())

