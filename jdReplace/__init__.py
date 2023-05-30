#!/usr/bin/env python3
from PyQt6.QtWidgets import QMessageBox, QApplication, QWidget, QLabel, QPlainTextEdit, QPushButton, QHBoxLayout, QVBoxLayout, QLineEdit, QCheckBox, QProgressBar, QFileDialog
from PyQt6.QtCore import QDir, QLocale, Qt, QThread, QCoreApplication, QTranslator, QLibraryInfo, pyqtSignal
from PyQt6.QtGui import QFont, QIcon
import webbrowser
import sys
import os


logo = QIcon(os.path.join(os.path.dirname(__file__), "Logo.svg"))
currentDir = os.path.dirname(os.path.realpath(__file__))


with open(os.path.join(currentDir, "version.txt"), "r", encoding="utf-8") as f:
    version = f.read().strip()


class AboutWindow(QWidget):
    def setup(self):
        logoLabel = QLabel()
        logoLabel.setPixmap(logo.pixmap(64, 64))

        self.titleLabel = QLabel("jdReplace " + version)
        self.descriptionLabel = QLabel(QCoreApplication.translate("AboutWindow", "With this program you can search and replace a text in all files of a folder"))
        self.copyrightLabel = QLabel("Copyright © 2019-2023 JakobDev")
        self.licenseLabel = QLabel(QCoreApplication.translate("AboutWindow", "This program is licensed under GNU GPL 3"))
        self.viewSourceButton = QPushButton(QCoreApplication.translate("AboutWindow", "View Source"))
        self.closeButton = QPushButton(QCoreApplication.translate("AboutWindow", "Close"))

        self.closeButton.setIcon(QIcon.fromTheme("window-close"))

        self.titleLabelFont = QFont()
        self.titleLabelFont.setBold(True)
        self.titleLabelFont.setPointSize(16)

        self.legalFont = QFont()
        self.legalFont.setPointSize(8)

        self.titleLabel.setFont(self.titleLabelFont)
        self.copyrightLabel.setFont(self.legalFont)
        self.licenseLabel.setFont(self.legalFont)

        logoLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.titleLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.descriptionLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.copyrightLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.licenseLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.viewSourceButton.clicked.connect(self.viewSourceAction)
        self.closeButton.clicked.connect(self.closeAction)

        self.buttonLayout = QHBoxLayout()
        self.buttonLayout.addWidget(self.viewSourceButton)
        self.buttonLayout.addWidget(self.closeButton)

        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(logoLabel)
        self.mainLayout.addWidget(self.titleLabel)
        self.mainLayout.addWidget(self.descriptionLabel)
        self.mainLayout.addWidget(self.copyrightLabel)
        self.mainLayout.addWidget(self.licenseLabel)
        self.mainLayout.addLayout(self.buttonLayout)

        self.setLayout(self.mainLayout)
        self.setWindowTitle(QCoreApplication.translate("AboutWindow", "About"))

    def viewSourceAction(self) -> None:
        webbrowser.open("https://codeberg.org/JakobDev/jdReplace")

    def closeAction(self) -> None:
        self.close()


class ReplaceThread(QThread):
    count = pyqtSignal("int")
    progress = pyqtSignal("int")
    text = pyqtSignal("QString")

    def __init__(self):
        QThread.__init__(self)

    def setup(self ,recursive: bool, path: str, searchText: str, replaceText: str, skipHidden: bool, followSymlinks: bool) -> None:
        self.recursive = recursive
        self.path = path
        self.searchText = searchText
        self.replaceText = replaceText
        self.skipHidden = skipHidden
        self.followSymlinks = followSymlinks

    def listFiles(self, path: str) -> None:
        self.text.emit(QCoreApplication.translate("ReplaceThread", "Searching {{path}}...").replace("{{path}}", path))
        try:
            for f in os.listdir(path):
                if f.startswith(".") and self.skipHidden:
                    continue
                filename = os.path.join(path,f)
                if os.path.islink(filename) and not self.followSymlinks:
                    continue
                if os.path.isdir(filename):
                    if self.recursive:
                        self.listFiles(filename)
                else:
                    self.filelist.append(filename)
        except Exception:
            print("Could not read " + path, file=sys.stderr)

    def run(self) -> None:
        self.filelist = []
        self.listFiles(self.path)
        self.count.emit(len(self.filelist))
        progressCount = 0
        for filename in self.filelist:
            try:
                with open(filename, 'r') as file :
                    filedata = file.read()
                if filedata.find(self.searchText) != -1:
                    filedata = filedata.replace(self.searchText,self.replaceText)
                    with open(filename, 'w') as file:
                        file.write(filedata)
            except Exception:
                print(QCoreApplication.translate("ReplaceThread", "Could not replace text in {{path}}. Maybe it's a binary file.").replace("{{path}}", filename), file=sys.stderr)
            progressCount += 1
            self.progress.emit(progressCount)


class StartWindow(QWidget):
    def setup(self):
        self.about = AboutWindow()
        self.about.setup()
        self.thread = ReplaceThread()

        self.directoryLabel = QLabel(QCoreApplication.translate("StartWindow", "Directory:"))
        self.directoryEdit = QLineEdit()
        self.directoryButton = QPushButton(QCoreApplication.translate("StartWindow", "Browse"))
        self.inputTextLabel = QLabel(QCoreApplication.translate("StartWindow", "Search for:"))
        self.inputTextEdit = QPlainTextEdit()
        self.outputTextLabel = QLabel(QCoreApplication.translate("StartWindow", "Replace with:"))
        self.outputTextEdit = QPlainTextEdit()
        self.subdirCheckBox = QCheckBox(QCoreApplication.translate("StartWindow", "Search Subdirectories"))
        self.hiddenCheckBox = QCheckBox(QCoreApplication.translate("StartWindow", "Skip Hidden"))
        self.symlinkCheckBox = QCheckBox(QCoreApplication.translate("StartWindow", "Follow Symlinks"))
        self.progressBar = QProgressBar()
        self.aboutButton = QPushButton(QCoreApplication.translate("StartWindow", "About"))
        self.okButton = QPushButton(QCoreApplication.translate("StartWindow", "OK"))

        self.directoryButton.setIcon(QIcon.fromTheme("folder"))
        self.aboutButton.setIcon(QIcon.fromTheme("help-about"))

        self.directoryEdit.setText(QDir.currentPath())
        self.inputTextEdit.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
        self.outputTextEdit.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
        self.directoryButton.clicked.connect(self.browse)
        self.aboutButton.clicked.connect(self.showAbout)
        self.okButton.clicked.connect(self.replaceFiles)
        self.thread.count.connect(self.setMax)
        self.thread.progress.connect(self.setProgress)
        self.thread.text.connect(self.setBarText)
        self.thread.finished.connect(self.threadFinish)
        self.progressBar.setValue(0)
        self.progressBar.setTextVisible(True)
        self.progressBar.setFormat("0")

        self.directoryLayout = QHBoxLayout()
        self.directoryLayout.addWidget(self.directoryLabel)
        self.directoryLayout.addWidget(self.directoryEdit)
        self.directoryLayout.addWidget(self.directoryButton)

        self.checkBoxLayout = QHBoxLayout()
        self.checkBoxLayout.addWidget(self.subdirCheckBox)
        self.checkBoxLayout.addWidget(self.hiddenCheckBox)
        self.checkBoxLayout.addWidget(self.symlinkCheckBox)

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
        self.mainLayout.addLayout(self.checkBoxLayout)
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
        directory = QFileDialog.getExistingDirectory(self, QCoreApplication.translate("StartWindow", "Browse"),path)

        if directory:
            self.directoryEdit.setText(directory)

    def showAbout(self):
        self.about.show()

    def setMax(self,count):
        self.progressBar.setMaximum(count)
        self.filecount = count

    def setProgress(self,count):
        self.progressBar.setValue(count)
        self.progressBar.setFormat(str(count) + "/" + str(self.filecount))

    def setBarText(self,text):
        self.progressBar.setFormat(text)

    def threadFinish(self):
        self.okButton.setEnabled(True)
        QMessageBox.information(self, QCoreApplication.translate("StartWindow", "Finished"), QCoreApplication.translate("StartWindow", "The text has been successfully replaced in all files"))

    def replaceFiles(self):
        path = self.directoryEdit.text()
        if not os.path.isdir(path):
            QMessageBox.critical(self, QCoreApplication.translate("StartWindow", "Not a directory"), QCoreApplication.translate("StartWindow", "'{{path}}' is not a directory!").replace("{{path}}", path))
            return

        searchText = self.inputTextEdit.toPlainText()
        if searchText == "":
            QMessageBox.critical(self, QCoreApplication.translate("StartWindow", "No search text"), QCoreApplication.translate("StartWindow", "Please enter a text to search for"))
            return

        replaceText = self.outputTextEdit.toPlainText()
        self.okButton.setEnabled(False)
        self.progressBar.setValue(0)
        self.thread.setup(self.subdirCheckBox.isChecked(), path, searchText, replaceText, self.hiddenCheckBox.isChecked(), self.symlinkCheckBox.isChecked())
        self.thread.start()

def main():
    app = QApplication(sys.argv)

    app.setDesktopFileName("page.codeberg.JakobDev.jdReplace")
    app.setApplicationName("jdReplace")
    app.setWindowIcon(logo)

    qt_translator = QTranslator()
    app_translator = QTranslator()
    system_language = QLocale.system().name().split("_")[0]
    qt_translator.load(os.path.join(QLibraryInfo.path(QLibraryInfo.LibraryPath.TranslationsPath), "qt_" + system_language + ".qm"))
    app_translator.load(os.path.join(currentDir, "translations", "jdReplace_" + system_language + ".qm"))
    app.installTranslator(app_translator)
    app.installTranslator(qt_translator)

    w = StartWindow()
    w.setup()
    sys.exit(app.exec())
