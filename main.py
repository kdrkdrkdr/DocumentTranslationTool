from lib.MainUI import Ui_MainWindow

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from lib.utils import *
from lib.client import *
from qdarkstyle import load_stylesheet_pyside2


class DocumentTranslator(QMainWindow, Ui_MainWindow):
    
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setFont(QFont('나눔고딕OTF', 10))
        self.setFixedSize(self.size())

        self.lbl = DropLabel('Drag and drop the file to translate.\n\nSupport Extension: .docx .doc .pptx .ppt .xlsx .xls .hwp\n\nHWP file requires Hancom office.', self)
        self.lbl.setGeometry(10, 70, 391, 171)
        self.lbl.setAcceptDrops(True)
        self.lbl.setAlignment(Qt.AlignCenter)

        self.lbl.filepath.connect(self.run_document_translation)

        self.rt = RunTranslate(self)
        self.rt.changeValue.connect(self.progressBar.setValue)
        self.rt.status_message.connect(self.statusbar.showMessage)

        self.statusbar.showMessage('Ready to translate.')
        
        self.dev_page.triggered.connect(lambda: webbrowser.open_new('https://github.com/kdrkdrkdr'))
        self.instruction.triggered.connect(lambda: webbrowser.open_new('https://github.com/kdrkdrkdr/DocumentTranslationTool/blob/main/README.md'))

        languageList = list(langDict.keys())
        self.fromLang.addItems(languageList); self.fromLang.setCurrentText('English')
        self.toLang.addItems(languageList)

        self.setStyleSheet(load_stylesheet_pyside2())
        self.setWindowIcon(QIcon('lib/sayo.ico'))
        self.show()

    
    def run_document_translation(self, fpath):
        if self.rt.isRunning():
            ret = QMessageBox.warning(
                self,
                "Warning",
                "Do you want to cancel the current translation and translate it again?",
                QMessageBox.Yes | QMessageBox.No
            )
            if ret == QMessageBox.No:
                return
            else:
                self.rt.terminate()

        fromLang = self.fromLang.currentText()
        toLang = self.toLang.currentText()
        
        if fromLang == toLang:
            QMessageBox.warning(
                self,
                "Error",
                "The starting language and the arriving language cannot be the same.\nPlease choose the language again.",
                QMessageBox.Ok
            )
        else:
            self.progressBar.setValue(0)
            self.rt.fileLoc = fpath
            self.rt.fromLang = langDict[fromLang]
            self.rt.toLang = langDict[toLang]
            self.statusbar.showMessage(f'Translating "{os.path.basename(fpath)}"... ')
            self.rt.start()
            


if __name__ == '__main__':
    # import ctypes
    # ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
    import sys
    app = QApplication(sys.argv)
    dt = DocumentTranslator()
    app.exec_()