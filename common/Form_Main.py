# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'gui.ui'
##
## Created by: Qt User Interface Compiler version 6.2.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QGroupBox, QLabel,
    QLineEdit, QMainWindow, QMenu, QMenuBar,
    QPushButton, QSizePolicy, QStatusBar, QWidget, QPlainTextEdit)

# try:
#     _fromUtf8 = QtCore.QString.fromUtf8
# except AttributeError:
#     def _fromUtf8(s):
#         return s

# try:
#     _encoding = QtGui.QApplication.UnicodeUTF8
#     def _translate(context, text, disambig):
#         return QtGui.QApplication.translate(context, text, disambig, _encoding)
# except AttributeError:
#     def _translate(context, text, disambig):
#         return QtGui.QApplication.translate(context, text, disambig)

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(u"Form")
        Form.resize(408, 510)
        self.iface = QComboBox(Form)
        self.iface.setGeometry(QRect(90, 30, 301, 21))
        self.iface.setObjectName(u"iface")
        self.label = QLabel(Form)
        self.label.setGeometry(QRect(10, 30, 71, 21))
        self.label.setObjectName(u"label")
        self.groupBox_2 = QGroupBox(Form)
        self.groupBox_2.setGeometry(QRect(0, 70, 391, 321))
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.label_2 = QLabel(self.groupBox_2)
        self.label_2.setGeometry(QRect(10, 20, 61, 21))
        self.label_2.setObjectName(u"label_2")
        self.leasetime = QLineEdit(self.groupBox_2)
        self.leasetime.setGeometry(QRect(70, 20, 113, 20))
        self.leasetime.setObjectName("leasetime")
        self.gateway = QLineEdit(self.groupBox_2)
        self.gateway.setGeometry(QRect(70, 50, 191, 20))
        self.gateway.setObjectName(u"gateway")
        self.label_5 = QLabel(self.groupBox_2)
        self.label_5.setGeometry(QRect(10, 50, 61, 21))
        self.label_5.setObjectName(u"label_5")
        self.submask = QLineEdit(self.groupBox_2)
        self.submask.setGeometry(QRect(260, 20, 113, 20))
        self.submask.setObjectName("submask")
        self.label_6 = QLabel(self.groupBox_2)
        self.label_6.setGeometry(QRect(200, 20, 61, 21))
        self.label_6.setObjectName(u"label_6")
        self.ippool = QLineEdit(self.groupBox_2)
        self.ippool.setGeometry(QRect(70, 80, 191, 20))
        self.ippool.setObjectName(u"ippool")
        self.label_15 = QLabel(self.groupBox_2)
        self.label_15.setGeometry(QRect(10, 80, 61, 21))
        self.label_15.setObjectName(u"label_15")
        self.dns = QLineEdit(self.groupBox_2)
        self.dns.setGeometry(QRect(70, 110, 191, 20))
        self.dns.setObjectName(u"dns")
        self.label_16 = QLabel(self.groupBox_2)
        self.label_16.setGeometry(QRect(10, 110, 61, 21))
        self.label_16.setObjectName(u"label_16")
        self.staticroute = QComboBox(self.groupBox_2)
        self.staticroute.setGeometry(QRect(70, 140, 111, 21))
        self.staticroute.setObjectName(u"staticroute")
        self.staticroute.addItem("")
        self.staticroute.addItem("")
        self.staticroute.addItem("")
        self.staticroute.addItem("")
        self.label_19 = QLabel(self.groupBox_2)
        self.label_19.setGeometry(QRect(10, 140, 61, 21))
        self.label_19.setObjectName("label_19")
        self.routers = QPlainTextEdit(self.groupBox_2)
        self.routers.setGeometry(QRect(13, 180, 371, 131))
        self.routers.setObjectName("routers")
        self.savecfg = QPushButton(self.groupBox_2)
        self.savecfg.setGeometry(QRect(270, 140, 75, 23))
        self.savecfg.setObjectName("savecfg")
        self.startbtn = QPushButton(Form)
        self.startbtn.setGeometry(QRect(20, 480, 91, 23))
        self.startbtn.setObjectName("startbtn")
        self.serstatus = QLabel(Form)
        self.serstatus.setGeometry(QRect(130, 480, 241, 21))
        self.serstatus.setObjectName("serstatus")
        self.label_20 = QLabel(Form)
        self.label_20.setGeometry(QRect(10, 400, 71, 21))
        self.label_20.setObjectName("label")
        self.waitoffer = QLineEdit(Form)
        self.waitoffer.setGeometry(QRect(100, 400, 70, 20))
        self.waitoffer.setObjectName("waitoffer")
        self.label_21 = QLabel(Form)
        self.label_21.setGeometry(QRect(200, 400, 70, 21))
        self.label_21.setObjectName("label")
        self.waitack = QLineEdit(Form)
        self.waitack.setGeometry(QRect(285, 400, 70, 20))
        self.waitack.setObjectName("waitack")
        self.label_22 = QLabel(Form)
        self.label_22.setGeometry(QRect(10, 428, 78, 21))
        self.label_22.setObjectName("label")
        self.replyrequest = QLineEdit(Form)
        self.replyrequest.setGeometry(QRect(100, 428, 70, 20))
        self.replyrequest.setObjectName("replyrequest")
        self.label_23 = QLabel(Form)
        self.label_23.setGeometry(QRect(200, 428, 113, 21))
        self.label_23.setObjectName("label")
        self.replyDiscover = QLineEdit(Form)
        self.replyDiscover.setGeometry(QRect(285, 428, 70, 20))
        self.replyDiscover.setObjectName("replyDiscover")
        self.label_24 = QLabel(Form)
        self.label_24.setGeometry(QRect(10, 456, 71, 21))
        self.label_24.setObjectName("label")
        self.t1 = QLineEdit(Form)
        self.t1.setGeometry(QRect(100, 456, 70, 20))
        self.t1.setObjectName("t1")
        self.label_25 = QLabel(Form)
        self.label_25.setGeometry(QRect(200, 456, 113, 21))
        self.label_25.setObjectName("label")
        self.t2 = QLineEdit(Form)
        self.t2.setGeometry(QRect(285, 456, 70, 20))
        self.t2.setObjectName("t2")
        self.retranslateUi(Form)
        QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", "Form", None))
        self.label.setText(QCoreApplication.translate("Form", "选择网卡:", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("Form", "Dhcp选项字段", None))
        self.label_2.setText(QCoreApplication.translate("Form", "Leasetime", None))
        self.leasetime.setText(QCoreApplication.translate("Form", "60", None))
        self.gateway.setText(QCoreApplication.translate("Form", "192.168.0.1", None))
        self.label_5.setText(QCoreApplication.translate("Form", "Routers", None))
        self.submask.setText(QCoreApplication.translate("Form", "255.255.255.0", None))
        self.label_6.setText(QCoreApplication.translate("Form", "Submask", None))
        self.ippool.setText(QCoreApplication.translate("Form", "192.168.0.100 192.168.0.200", None))
        self.label_15.setText(QCoreApplication.translate("Form", "Ip pools", None))
        self.dns.setText(QCoreApplication.translate("Form", "223.5.5.5 223.6.6.6", None))
        self.label_16.setText(QCoreApplication.translate("Form", "Dns Domain", None))
        self.staticroute.setItemText(0, QCoreApplication.translate("Form", "noStaticRouter", None))
        self.staticroute.setItemText(1, QCoreApplication.translate("Form", "options33", None))
        self.staticroute.setItemText(2, QCoreApplication.translate("Form", "options121", None))
        self.staticroute.setItemText(3, QCoreApplication.translate("Form", "options249", None))
        self.label_19.setText(QCoreApplication.translate("Form", "静态路由", None))
        self.routers.setPlainText(QCoreApplication.translate("Form", "192.168.0.0/24 192.168.88.8\n"
"192.168.1.0/24 192.168.88.8\n"
"192.168.2.0/24 192.168.88.8\n"
"192.168.3.0/24 192.168.88.8\n"
"192.168.4.0/24 192.168.88.8\n"
"192.168.5.0/24 192.168.88.8\n"
"192.168.6.0/24 192.168.88.8\n"
"192.168.7.0/24 192.168.88.8\n"
"192.168.8.0/24 192.168.88.8\n"
"192.168.9.0/24 192.168.88.8", None))
        self.savecfg.setText(QCoreApplication.translate("Form", "保存配置", None))
        self.startbtn.setText(QCoreApplication.translate("Form", "开启服务器", None))
        self.serstatus.setText(QCoreApplication.translate("Form", "服务器未开启", None))
        self.label_20.setText(QCoreApplication.translate("Form", "wait_offer", None))
        self.waitoffer.setText(QCoreApplication.translate("Form", "0", None))
        self.label_21.setText(QCoreApplication.translate("Form", "wait_ack", None))
        self.waitack.setText(QCoreApplication.translate("Form", "0", None))
        self.label_22.setText(QCoreApplication.translate("Form", "reply_request", None))
        self.replyrequest.setText(QCoreApplication.translate("Form", "0", None))
        self.label_23.setText(QCoreApplication.translate("Form", "reply_Discover", None))
        self.replyDiscover.setText(QCoreApplication.translate("Form", "0", None))
        self.label_24.setText(QCoreApplication.translate("Form", "1/2更新租约", None))
        self.t1.setText(QCoreApplication.translate("Form", "0", None))
        self.label_25.setText(QCoreApplication.translate("Form", "7/8更新租约", None))
        self.t2.setText(QCoreApplication.translate("Form", "0", None))
