# -*- coding: utf-8 -*-
# !/usr/bin/env python

# Example using PyQt5 QWebView() и Markdown
# Example from https://github.com/Yust11135/pyqt-md-reader/blob/master/PyQt5_QWebView__Markdown_example.py

import sys
from PyQt5.QtWidgets import QMainWindow, QAction, QFileDialog, qApp, QApplication, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QUrl
import os.path

from markdown import markdown as mk_translate_to_html_view

from PyQt5.QtWebKitWidgets import QWebView

class Reader(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        self.resize(500, 500)
        self.web_view = WebView(self)
        self.setCentralWidget(self.web_view)

        self.statusBar().showMessage('Ready')
        self.web_view.loadFinished.connect(self._load_finished)

        self.createMenu()

    def _load_finished(self):
        frame = self.web_view.page().mainFrame()
        self.web_view.page().setViewportSize(frame.contentsSize())
        self.resize(frame.contentsSize())
        html_data = frame.toHtml()

    def createMenu(self):
        exitAction = QAction(QIcon('exit.png'), '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qApp.quit)

        openAction = QAction(QIcon('open.png'), '&Open', self)
        openAction.setShortcut('Ctrl+O')
        openAction.setStatusTip('Open Markdown file')
        openAction.triggered.connect(self.openNewFile)

        self.statusBar()

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openAction)
        fileMenu.addAction(exitAction)

        aboutAction = QAction(QIcon(''), '&About', self)
        aboutAction.setStatusTip('About')
        aboutAction.triggered.connect(self.showAboutDialog)
        aboutMenu = menubar.addMenu('&About')
        aboutMenu.addAction(aboutAction)

    def showAboutDialog(self):
        self.statusBar().showMessage('source code: github.com/smoqadam/pyqt-md-reader')

    def openNewFile(self):
        self.statusBar().showMessage('OPEN')
        try:
            fname = QFileDialog.getOpenFileName(self, 'open file', '', 'All Text Files (*.md *.markdown *.txt *.*)', None)
            fname = fname[0]
            self.web_view.showMarkdown(fname)

        except UnicodeDecodeError:
            self.statusBar().showMessage('Please select only text files')
        except IOError:
            self.statusBar().showMessage('File open canceled!')
        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            QMessageBox.critical(self,
                                           "The error, error code, and reason are listed below:",
                                           message,
                                           buttons=QMessageBox.Close,
                                           defaultButton=QMessageBox.Close)


class WebView(QWebView):
    def __init__(self, parent=None):
        super(WebView, self).__init__(parent)
        self.main = parent

    def dragEnterEvent(self, event):
        u = event.mimeData().urls()
        for url in u:
            self.filePath = os.path.abspath(url.toLocalFile())

            ext = self.filePath.split('.')[-1]
            if ext in ['txt', 'md', 'markdown']:
                event.accept()
            else:
                event.ignore()

    def dropEvent(self, event):
        event.accept()
        self.showMarkdown(self.filePath)

    def contextMenuEvent(self, e):
        pass
        # 'do nothing on right click'

    def showMarkdown(self, filePath):
        markdown_file = open(filePath)
        file_content = markdown_file.read()

        html_view = mk_translate_to_html_view(file_content)

        self.setHtml(html_view)

        self.main.statusBar().showMessage(filePath)


def main():
    qtapp = QApplication(sys.argv)
    reader = Reader()
    reader.web_view.load(QUrl('blank'))
    reader.show()
    qtapp.exec_()


if __name__ == '__main__':
    main()
