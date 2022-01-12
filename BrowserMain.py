import sys
from PyQt5 import QtPrintSupport
from PyQt5.QtWidgets import QMainWindow, QApplication, QStatusBar, QWidget
from browserGUI import *
import time
from os import environ
from PyQt5 import QtCore, QtWebEngineWidgets, QtGui
from PyQt5.QtPrintSupport import *
import psutil
import threading

def suppress_qt_warnings():
    environ["QT_DEVICE_PIXEL_RATIO"] = "0"
    environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    environ["QT_SCREEN_SCALE_FACTORS"] = "1"
    environ["QT_SCALE_FACTOR"] = "1"
x_url = []
y_url = []
back_press = 0
forward_press = 0
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        try:
            self.setWindowIcon(QtGui.QIcon("/home/rawbeen/Desktop/browser.png"))
        except:
            pass
        url = QtCore.QUrl(self.ui.lineEdit.text())
        self.ui.progressBar.setValue(0)
        self.ui.comboBox.setCurrentIndex(1)
        self.ui.progressBar.setStyleSheet("QProgressBar::chunk "
                                          "{"
                                          "background-color: red;"
                                          "}")
        x = 0
        while x <= 100:
            self.ui.progressBar.setValue(x)
            x += 0.1
            if x > 99:
                self.ui.progressBar.setValue(0)
                break

        self.ui.widget = QtWebEngineWidgets.QWebEngineView(self.ui.tabWidget)
        self.ui.widget.setGeometry(QtCore.QRect(0, 60, 1341, 581))
        self.ui.widget.setWhatsThis("")
        self.ui.widget.setStyleSheet("")
        self.ui.widget.setObjectName("widget")
        label = "New Tab"
        i = self.ui.tabWidget.addTab(self.ui.widget, label)
        self.ui.tabWidget.setCurrentIndex(i)
        self.ui.widget.load(QtCore.QUrl("https://www.google.com"))
        self.ui.pushButtonNewTab.clicked.connect(self.add_new_tab)
        self.ui.tabWidget.tabCloseRequested.connect(self.close_tab)
        self.ui.lineEdit.returnPressed.connect(self.nagivate_url)
        self.ui.comboBox.currentIndexChanged.connect(
            self.change_search_engines)
        self.ui.pushButtonRefresh.clicked.connect(self.refresh_tab)
        self.ui.pushButtonBackward.clicked.connect(self.back_tab)
        self.ui.pushButtonForward.clicked.connect(self.forward_tab)
        self.ui.pushButtonYoutube.clicked.connect(self.youtube)
        self.ui.pushButtonFacebook.clicked.connect(self.facebook)
        self.ui.pushButtonGoogle.clicked.connect(self.google)
        self.ui.pushButtonGmail.clicked.connect(self.gmail)
        self.ui.pushButton.clicked.connect(self.bookmarks)
        self.ui.listWidget.itemClicked.connect(self.bookmark_link)
        qurl = QtCore.QUrl("")
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.lcd_animation_th)
        timer.start(1100)
        

        # if
        self.ui.widget.urlChanged.connect(lambda qurl, browser=self.ui.widget:
                                          self.update_url(qurl))
        self.ui.widget.loadFinished.connect(lambda _, i=i, browser=self.ui.widget:
                                            self.ui.tabWidget.setTabText(i, self.ui.widget.page().title()))

    def add_new_tab(self, qurl=None):
        self.ui.progressBar.setStyleSheet("QProgressBar::chunk "
                                          "{"
                                          "background-color: red;"
                                          "}")
        x = 0
        while x <= 100:
            self.ui.progressBar.setValue(x)
            x += 0.1
            if x > 99:
                self.ui.progressBar.setValue(0)
                break

        if qurl is None:
            qurl = QtCore.QUrl("")
        # self.ui.widget = QtWebEngineWidgets.QWebEngineView(self.ui.tab)
        self.ui.widget = QtWebEngineWidgets.QWebEngineView(self.ui.tabWidget)
        self.ui.widget.setGeometry(QtCore.QRect(0, 60, 1341, 581))
        self.ui.widget.setWhatsThis("")
        self.ui.widget.setStyleSheet("")
        self.ui.widget.setObjectName("widget")
        label = "New Tab"
        i = self.ui.tabWidget.addTab(self.ui.widget, label)
        self.ui.tabWidget.setCurrentIndex(i)
        self.ui.widget.load(QtCore.QUrl("https://www.google.com"))

        # if
        self.ui.widget.urlChanged.connect(lambda qurl, browser=self.ui.widget:
                                          self.update_url(qurl))
        self.ui.widget.loadFinished.connect(lambda _, i=i, browser=self.ui.widget:
                                            self.ui.tabWidget.setTabText(i, self.ui.widget.page().title()))

    def close_tab(self, i):
        self.ui.progressBar.setStyleSheet("QProgressBar::chunk "
                                          "{"
                                          "background-color: red;"
                                          "}")
        x = 0
        while x <= 100:
            self.ui.progressBar.setValue(x)
            x += 0.01
            if x > 90:
                self.ui.progressBar.setValue(0)
                break
        if self.ui.tabWidget.count() == 1:
            return
        else:
            self.ui.tabWidget.removeTab(i)

    def update_title(self):
        if self.ui.widget != self.ui.tabWidget.currentWidget():
            return
        else:
            title = self.ui.tabWidget.currentWidget().page().title()
            self.ui.setWindowTitle("%s" % title)

    def nagivate_url(self):
        url = QtCore.QUrl(self.ui.lineEdit.text())
        s = self.ui.lineEdit.text()
        if ".com" in s or ".net" in s or ".org" in s or ".np" in s or ".in" in s:
            if "http" in s or "https" in s:
                self.ui.widget.load(QtCore.QUrl(s))
                x_url.append(self.ui.lineEdit.text())

            elif "www." in s:

                self.ui.widget.load(QtCore.QUrl("http://" + s))
                x_url.append(self.ui.lineEdit.text())

            else:

                self.ui.widget.load(QtCore.QUrl("http://www." + s))
                x_url.append(self.ui.lineEdit.text())

        else:
            if s == "fb" or s == "google" or s == "youtube":

                self.ui.widget.load(QtCore.QUrl("https://www." + s + ".com"))
                x_url.append(self.ui.lineEdit.text())

            elif s == "yt":

                self.ui.widget.load(QtCore.QUrl("https://www.youtube.com"))
                x_url.append(self.ui.lineEdit.text())


            else:
                if self.ui.comboBox.currentText().lower() == "google" or self.ui.comboBox.currentText().lower() == "bing":

                    self.ui.widget.load(QtCore.QUrl(
                        "https://www." + self.ui.comboBox.currentText().lower() + ".com/search?q=" + s))
                    
                elif self.ui.comboBox.currentText().lower() == "duckduckgo":
                    

                    self.ui.widget.load(QtCore.QUrl(
                        "https://www." + self.ui.comboBox.currentText().lower() + ".com/?q=" + s))
                    x_url.append(self.ui.lineEdit.text())

                elif self.ui.comboBox.currentText().lower() == "yahoo":

                    self.ui.widget.load(QtCore.QUrl(
                        "https://search." + self.ui.comboBox.currentText().lower() + ".com/search?p=" + s))
                    x_url.append(self.ui.lineEdit.text())
                    
                elif self.ui.comboBox.currentText().lower() == "ask":
                    x_url.append(self.ui.lineEdit.text())

                    self.ui.widget.load(QtCore.QUrl(
                        "https://www." + self.ui.comboBox.currentText().lower() + ".com/web?q=" + s))
               

    def update_url(self, url):
        self.ui.progressBar.setStyleSheet("QProgressBar::chunk "
                                          "{"
                                          "background-color: red;"
                                          "}")
        x = 0
        while x <= 100:
            self.ui.progressBar.setValue(x)
            x += 0.01
            if x > 95:
                self.ui.progressBar.setValue(0)
                break
        if self.ui.widget != self.ui.tabWidget.currentWidget():
            return
        str_url = str(url)
        s = str_url[0:-2]
        s = s[19:]
        if "file:/" in s:
            return
        self.ui.lineEdit.setText(s)
        x_url.append(self.ui.lineEdit.text())
        y_url.append(self.ui.lineEdit.text())
       
    def change_search_engines(self):
        s = self.ui.lineEdit.text()
        self.ui.lineEdit.setPlaceholderText(
            "Search "+self.ui.comboBox.currentText()+" or Type a URL")
    def refresh_tab(self):
        self.ui.widget.load(QtCore.QUrl(self.ui.lineEdit.text()))

    def back_tab(self):
        global back_press
        back_press += 1
        global x_url
        print(x_url)
        print(len(x_url))
        if len(x_url) == 0:
            pass
        elif len(x_url) == 1:
            self.ui.widget.load(QtCore.QUrl("https:www.google.com"))

            
        else:
            try:
                self.ui.widget.load(QtCore.QUrl(x_url[len(x_url) - (back_press+1)]))
                x_url.remove(x_url[len(x_url) - (back_press+1)])
            except:
                pass

    def forward_tab(self):
        global forward_press
        forward_press += 1
        global y_url
        if len(y_url) == 0 and len(y_url) == 1:
            pass
        else:
            try:
                self.ui.widget.load(QtCore.QUrl(y_url[-forward_press - 1]))
                y_url.remove(y_url[len(y_url)-(forward_press+1)])
            except:
                pass



    def youtube(self):

        self.ui.widget.load(QtCore.QUrl("http://www.youtube.com"))

    def facebook(self):
        self.ui.widget.load(QtCore.QUrl("http://www.facebook.com"))

    def google(self):

        self.ui.widget.load(QtCore.QUrl("http://www.google.com"))

    def gmail(self):
        self.ui.widget.load(QtCore.QUrl("http://www.gmail.com"))

    def bookmarks(self):
        self.ui.listWidget.addItem(
            " "+self.ui.tabWidget.currentWidget().page().title()+"  ")
        self.ui.listWidget2.addItem(self.ui.lineEdit.text())

    def bookmark_link(self):
        indx_num = self.ui.listWidget.currentRow()
        self.ui.widget.load(QtCore.QUrl(
            self.ui.listWidget2.item(indx_num).text()))

    def lcd_animation_th(self):
        th = threading.Thread(target=self.lcd_animation)
        th.start()

    def lcd_animation(self):
        data = psutil.cpu_percent(interval=3)
        self.ui.lcdNumber.display(data)


if __name__ == "__main__":
    suppress_qt_warnings()
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
