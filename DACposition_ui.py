# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DACposition.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.setWindowModality(QtCore.Qt.WindowModal)
        Form.resize(935, 480)
        self.label = QtGui.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(0, 10, 880, 31))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.layoutWidget = QtGui.QWidget(Form)
        self.layoutWidget.setGeometry(QtCore.QRect(20, 60, 886, 390))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setSpacing(60)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.btnSchwa = QtGui.QPushButton(self.layoutWidget)
        self.btnSchwa.setText(_fromUtf8(""))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("../../Desktop/Horizon 4.0/Script/Logo/c4-90.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnSchwa.setIcon(icon)
        self.btnSchwa.setIconSize(QtCore.QSize(400, 380))
        self.btnSchwa.setObjectName(_fromUtf8("btnSchwa"))
        self.horizontalLayout.addWidget(self.btnSchwa)
        self.btnCamera = QtGui.QPushButton(self.layoutWidget)
        self.btnCamera.setText(_fromUtf8(""))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8("../../Desktop/Horizon 4.0/Script/Logo/c5-90.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnCamera.setIcon(icon1)
        self.btnCamera.setIconSize(QtCore.QSize(400, 380))
        self.btnCamera.setObjectName(_fromUtf8("btnCamera"))
        self.horizontalLayout.addWidget(self.btnCamera)
        self.label_2 = QtGui.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(40, 70, 371, 31))
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_3 = QtGui.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(513, 70, 371, 31))
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName(_fromUtf8("label_3"))

        self.retranslateUi(Form)
        QtCore.QObject.connect(self.btnCamera, QtCore.SIGNAL(_fromUtf8("clicked()")), Form.close)
        QtCore.QObject.connect(self.btnSchwa, QtCore.SIGNAL(_fromUtf8("clicked()")), Form.close)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "DAC position", None))
        self.label.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:18pt;\">Define current DAC position</span></p></body></html>", None))
        self.label_2.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:18pt;\">Schwarzschild</span></p></body></html>", None))
        self.label_3.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:18pt;\">Camera</span></p></body></html>", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Form = QtGui.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

