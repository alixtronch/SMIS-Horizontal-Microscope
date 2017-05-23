# --------------------------------------------------------------------

# Editeur: Matthias Glachant (glachant.matthias@gmail.com  )
# Date: 7/6/2016

# --------------------------------------------------------------------

import logging
import sys  # We need sys so that we can pass argv to QApplication
import time

import numpy as np
import serial
from PyQt4 import QtGui  # Import the PyQt4 module we'll need

import Advancedparameters_ui
import DACposition_ui
import DACposition_simple
import Horizontal_ui  # This file holds our MainWindow and all design related things
import Micromode_ui

# create logger
logger = logging.getLogger('HM App:')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler('HMApp_full.log')
fh.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s\t%(name)s\t(%(levelname)s)\t:\t%(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)

logger.info('--- Starting Application ---')


###----------DEF_FONCTIONS--------------------------------------

def execution(ser, commande):
    logger.debug('Executing serial command: ' + commande)
    # Code to send a command to the controller
    # send the character to the device
    ser.write(bytes(commande + '\r\n', 'UTF-8'))
    out = ''
    # let's wait one second before reading output (let's give device time to answer)
    time.sleep(0.2)  ### is this necessary? maybe that is why the program is slow
    # Formation of the answer to something understable
    liste = []
    reponse = []
    while (ser.inWaiting() > 0):
        out = str(ser.read(1))
        liste.append(out)
    if (len(liste) > 0):
        del liste[len(liste) - 1]
        for car in liste:
            reponse.append(car[2])  # Answer is in a list of caracters --> a simple word (rep)
    rep = str()
    for i in range(len(reponse)):
        rep += reponse[i]
    return (rep)


def initialisation(ser, motorNb):
    Nb = ('1', '2', '3', '4', '5', '6', '7', '8', '9')
    init = ('INIT1', 'INIT2', 'INIT3', 'INIT4', 'INIT5', 'INIT6', 'INIT7', 'INIT8', 'INIT9')
    execution(ser, init[Nb.index(str(motorNb))])
    return ()


def deplacementmode(ser, motorNb, mode):
    # mode=1 if ABSOLUTE, mode=2 if RELATIVE
    Nb = ('1', '2', '3', '4', '5', '6', '7', '8', '9')
    absol = ('ABSOL1', 'ABSOL2', 'ABSOL3', 'ABSOL4', 'ABSOL5', 'ABSOL6', 'ABSOL7', 'ABSOL8', 'ABSOL9')
    relat = ('RELAT1', 'RELAT2', 'RELAT3', 'RELAT4', 'RELAT5', 'RELAT6', 'RELAT7', 'RELAT8', 'RELAT9')
    if (mode == '1'):
        execution(ser, absol[Nb.index(str(motorNb))])
        return ()
    if (mode == '2'):
        execution(ser, relat[Nb.index(str(motorNb))])
        return ()


def velocity(ser, motorNb, velocity):
    Nb = ('1', '2', '3', '4', '5', '6', '7', '8', '9')
    vel = ('IVEL1=', 'IVEL2=', 'IVEL3=', 'IVEL4=', 'IVEL5=', 'IVEL6=', 'IVEL7=', 'IVEL8=', 'IVEL9=')
    execution(ser, vel[Nb.index(str(motorNb))] + str(velocity))
    return ()


def position(ser, motorNb, position):
    Nb = ('1', '2', '3', '4', '5', '6', '7', '8', '9')
    pos = ('PSET1=', 'PSET2=', 'PSET3=', 'PSET4=', 'PSET5=', 'PSET6=', 'PSET7=', 'PSET8=', 'PSET9=')
    execution(ser, pos[Nb.index(str(motorNb))] + str(position))
    return ()


def move(ser, motorNb):
    Nb = ('1', '2', '3', '4', '5', '6', '7', '8', '9')
    mov = ('PGO1', 'PGO2', 'PGO3', 'PGO4', 'PGO5', 'PGO6', 'PGO7', 'PGO8', 'PGO9')
    execution(ser, mov[Nb.index(str(motorNb))])
    return ()


def acceleration(ser, motorNb, acceleration):
    logger.debug('function: acceleration')
    logger.debug('\tset acceleration to:', acceleration)
    Nb = ('1', '2', '3', '4', '5', '6', '7', '8', '9')
    acc = ('ACC1=', 'ACC2=', 'ACC3=', 'ACC4=', 'ACC5=', 'ACC6=', 'ACC7=', 'ACC8=', 'ACC9=')
    execution(ser, acc[Nb.index(str(motorNb))] + str(acceleration))
    return ()


def deceleration(ser, motorNb, deceleration):
    logger.debug('function: deceleration')
    logger.debug('\tset deceleration to:', deceleration)
    Nb = ('1', '2', '3', '4', '5', '6', '7', '8', '9')
    acc = ('DACC1=', 'DACC2=', 'DACC3=', 'DACC4=', 'DACC5=', 'DACC6=', 'DACC7=', 'DACC8=', 'DACC9=')
    execution(ser, acc[Nb.index(str(motorNb))] + str(deceleration))
    return ()


def stop(ser, motorNb):
    Nb = ('1', '2', '3', '4', '5', '6', '7', '8', '9')
    stp = ('STOP1', 'STOP2', 'STOP3', 'STOP4', 'STOP5', 'STOP6', 'STOP7', 'STOP8', 'STOP9')
    execution(ser, stp[Nb.index(str(motorNb))])
    return ()


def positionvalue(ser, motorNb):
    Nb = ('1', '2', '3', '4', '5', '6', '7', '8', '9')
    pos = ('?CNT1', '?CNT2', '?CNT3', '?CNT4', '?CNT5', '?CNT6', '?CNT7', '?CNT8', '?CNT9')
    position = execution(ser, pos[Nb.index(motorNb)])
    return (position[0])


def speedvalue(ser, motorNb):
    Nb = ('1', '2', '3', '4', '5', '6', '7', '8', '9')
    speed = ('?IVEL1', '?IVEL2', '?IVEL3', '?IVEL4', '?IVEL5', '?IVEL6', '?IVEL7', '?IVEL8', '?IVEL9')
    speedval = execution(ser, speed[Nb.index(motorNb)])
    return (speedval[0])


def PcalcDiamondRaman(P_range, peak_position, diamond_peak=1334):
    # these are the formulas that Paul Loubeyre uses to calculate his pressure
    if P_range < 200:
        return int(100 * np.around(547 * ((peak_position - diamond_peak) / diamond_peak) * (1 + 0.5 * (3.75 - 1) *
                                                                                            (
                                                                                                peak_position - diamond_peak) / diamond_peak),
                                   decimals=3)) / 100
    if P_range > 200:
        return int(100 * np.around(3141 - 4.157 * peak_position + 1.429e-3 * peak_position ** 2, decimals=3)) / 100


## TODO: simple table and plotting in a separate tab?


# ------------------------CLASSES------------------------------------------------------------
class AdvancedparametersWindow(QtGui.QDialog, Advancedparameters_ui.Ui_Advanced_parameters_window):
    def __init__(self, parent=None):
        # Explaining super is out of the scope of this article
        # So please google it if you're not familar with it
        # Simple reason why we use it here is that it allows us to
        # access variables, methods etc in the design.py file
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)

        self.btnSeeparam.clicked.connect(self.seeparam)
        self.btnSaveparam.clicked.connect(self.saveparam)
        self.btnposition.clicked.connect(self.positionval)
        self.btnplus.clicked.connect(self.mouvementplus)
        self.btnmoins.clicked.connect(self.mouvementmoins)

    def positionval(self):
        motorNB = self.comboBox.currentIndex() + 1
        if (motorNB != 5):
            self.position.setText(execution(ser, '?CNT' + str(motorNB)))
        if (motorNB == 5):
            self.position.setText(str(-1 * int(execution(ser, '?CNT' + str(motorNB)))))

    def mouvementplus(self):
        motorNB = self.comboBox.currentIndex() + 1
        if (motorNB != 5):
            execution(ser, 'PSET' + str(motorNB) + '=' + str(self.step.text()))
            execution(ser, 'PGO' + str(motorNB))
            time.sleep(0.1)
            while (execution(ser, '?VACT' + str(motorNB)) != '0'):
                time.sleep(0.1)
            self.position.setText(execution(ser, '?CNT' + str(motorNB)))
        if (motorNB == 5):
            execution(ser, 'PSET' + str(motorNB) + '=-' + str(self.step.text()))
            execution(ser, 'PGO' + str(motorNB))
            time.sleep(0.1)
            while (execution(ser, '?VACT' + str(motorNB)) != '0'):
                time.sleep(0.1)
            self.position.setText(str(-1 * int(execution(ser, '?CNT' + str(motorNB)))))

    def mouvementmoins(self):
        motorNB = self.comboBox.currentIndex() + 1
        if (motorNB != 5):
            execution(ser, 'PSET' + str(motorNB) + '=-' + str(self.step.text()))
            execution(ser, 'PGO' + str(motorNB))
            time.sleep(0.1)
            while (execution(ser, '?VACT' + str(motorNB)) != '0'):
                time.sleep(0.1)
            self.position.setText(execution(ser, '?CNT' + str(motorNB)))
        if (motorNB == 5):
            motorNB = self.comboBox.currentIndex() + 1
            execution(ser, 'PSET' + str(motorNB) + '=' + str(self.step.text()))
            execution(ser, 'PGO' + str(motorNB))
            time.sleep(0.1)
            while (execution(ser, '?VACT' + str(motorNB)) != '0'):
                time.sleep(0.1)
            self.position.setText(str(-1 * int(execution(ser, '?CNT' + str(motorNB)))))

    def saveparam(self):
        xyzacc = self.xyzAccNew.text()
        xyzdec = self.xyzDecNew.text()
        xyzspeed = self.xyzSpeedNew.text()
        largeacc = self.largeAccNew.text()
        largedec = self.largeDecNew.text()
        largespeed = self.largeSpeedNew.text()

        if (xyzacc != ''):
            acceleration(4, xyzacc)
            acceleration(5, xyzacc)
            acceleration(6, xyzacc)
        if (xyzdec != ''):
            deceleration(4, xyzdec)
            deceleration(5, xyzdec)
            deceleration(6, xyzdec)
        if (xyzspeed != ''):
            velocity(4, xyzspeed)
            velocity(5, xyzspeed)
            velocity(6, xyzspeed)

        if (largeacc != ''):
            acceleration(1, largeacc)
            acceleration(2, largeacc)
            acceleration(3, largeacc)
        if (largedec != ''):
            deceleration(1, largedec)
            deceleration(2, largedec)
            deceleration(3, largedec)
        if (largespeed != ''):
            velocity(1, largespeed)
            velocity(2, largespeed)
            velocity(3, largespeed)

        for i in range(1, 7):
            execution(ser, 'SAVEAXPA' + str(i))

    def seeparam(self):
        self.xyzAccAct.setText(execution(ser, '?ACC4'))
        self.xyzDecAct.setText(execution(ser, '?DACC4'))
        self.xyzSpeedAct.setText(execution(ser, '?IVEL4'))
        self.largeAccAct.setText(execution(ser, '?ACC1'))
        self.largeDecAct.setText(execution(ser, '?DACC1'))
        self.largeSpeedAct.setText(execution(ser, '?IVEL1'))


class DACpositionWindow(QtGui.QDialog, DACposition_ui.Ui_Form):
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)

        self.btnCamera.clicked.connect(self.cameramode)
        self.btnSchwa.clicked.connect(self.schwamode)

    def cameramode(self):
        execution(ser, 'JACC3=2')

    def schwamode(self):
        execution(ser, 'JACC3=1')

class InitialSetupWindow(QtGui.QDialog, DACposition_simple.Ui_Form):
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)

        self.btnCamera.clicked.connect(self.cameramode)
        self.btnSchwa.clicked.connect(self.schwamode)

    def cameramode(self):
        execution(ser, 'JACC3=2')

    def schwamode(self):
        execution(ser, 'JACC3=1')


class MicromodeWindow(QtGui.QDialog, Micromode_ui.Ui_Microscopemode):
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)

        self.btnIRmode.clicked.connect(self.IRmode)
        self.btnRamanmode.clicked.connect(self.Ramanmode)

    def IRmode(self):
        execution(ser, 'JACC1=1')

    def Ramanmode(self):
        execution(ser, 'JACC1=2')


class MainHorizontalWindow(QtGui.QMainWindow, Horizontal_ui.Ui_MainWindow):
    def __init__(self):
        # Explaining super is out of the scope of this article
        # So please google it if you're not familar with it
        # Simple reason why we use it here is that it allows us to
        # access variables, methods etc in the design.py file
        super(self.__class__, self).__init__()
        self.setupUi(self)

        self.btnStop.clicked.connect(self.stopall)
        self.radioButton_1.clicked.connect(self.statemotor1)
        self.radioButton_2.clicked.connect(self.statemotor2)
        self.radioButton_3.clicked.connect(self.statemotor3)
        self.radioButton_4.clicked.connect(self.statemotor4)
        self.radioButton_5.clicked.connect(self.statemotor5)
        self.radioButton_6.clicked.connect(self.statemotor6)
        self.btnxh.clicked.connect(self.mouvementXh)
        self.btnxb.clicked.connect(self.mouvementXb)
        self.btnxh.clicked.connect(self.Xvalue)
        self.btnxb.clicked.connect(self.Xvalue)
        self.btnyh.clicked.connect(self.mouvementYh)
        self.btnyb.clicked.connect(self.mouvementYb)
        self.btnyh.clicked.connect(self.Yvalue)
        self.btnyb.clicked.connect(self.Yvalue)
        self.btnzh.clicked.connect(self.mouvementZh)
        self.btnzb.clicked.connect(self.mouvementZb)
        self.btnzh.clicked.connect(self.Zvalue)
        self.btnzb.clicked.connect(self.Zvalue)
        self.btnMicromode.clicked.connect(self.micromode)
        self.btnMicromode.clicked.connect(self.DACposition)
        self.btnReadX.clicked.connect(self.Xvalue)
        self.btnReadX.clicked.connect(self.Yvalue)
        self.btnReadX.clicked.connect(self.Zvalue)
        self.btnSetX.clicked.connect(self.Xsetvalue)
        self.btnSetX.clicked.connect(self.Xvalue)
        self.btnSetX.clicked.connect(self.Ysetvalue)
        self.btnSetX.clicked.connect(self.Yvalue)
        self.btnSetX.clicked.connect(self.Zsetvalue)
        self.btnSetX.clicked.connect(self.Zvalue)
        self.btnSaveP1.clicked.connect(self.SaveP1)
        self.btnSaveP2.clicked.connect(self.SaveP2)
        self.btnSaveP3.clicked.connect(self.SaveP3)
        self.btnGoP1.clicked.connect(self.GoP1)
        self.btnGoP2.clicked.connect(self.GoP2)
        self.btnGoP3.clicked.connect(self.GoP3)
        self.btnGoP1.clicked.connect(self.Xvalue)
        self.btnGoP1.clicked.connect(self.Yvalue)
        self.btnGoP1.clicked.connect(self.Zvalue)
        self.btnGoP2.clicked.connect(self.Xvalue)
        self.btnGoP2.clicked.connect(self.Yvalue)
        self.btnGoP2.clicked.connect(self.Zvalue)
        self.btnGoP3.clicked.connect(self.Xvalue)
        self.btnGoP3.clicked.connect(self.Yvalue)
        self.btnGoP3.clicked.connect(self.Zvalue)
        self.btnsettings.clicked.connect(self.openparameters)
        if (execution(ser, '?JACC3') == '1'):
            self.radioButton_Schwa.setChecked(True)
        if (execution(ser, '?JACC3') == '2'):
            self.radioButton_Camera.setChecked(True)
        if (execution(ser, '?JACC1') == '1'):
            self.radioButton_IR.setChecked(True)
        if (execution(ser, '?JACC1') == '2'):
            self.radioButton_Raman.setChecked(True)
        self.btnSYZ.clicked.connect(self.SYZstatus)
        self.btnAll.clicked.connect(self.statusAll)
        self.btnAll.setStyleSheet("QPushButton {background : green}")
        self.btnAll.setText('Turn all OFF')
        self.labelSYZ.setText('Turn SYZ OFF')
        self.labelSYZ.setStyleSheet("QLabel {color : green}")
        self.btnSetzero.clicked.connect(self.SetZero)

        self.btnPosText.clicked.connect(self.PosTextChange)

    def PosTextChange(self):
        print(self.btnSaveP1.text())
        if self.btnSaveP1.text() == 'BKG':
            self.btnSaveP1.setText('Save P1')
            self.btnSaveP2.setText('Save P2')
            self.btnSaveP3.setText('Save P3')

            self.btnGoP1.setText('Go to P1')
            self.btnGoP2.setText('Go to P2')
            self.btnGoP3.setText('Go to P3')

        else:
            self.btnSaveP1.setText('BKG')
            self.btnSaveP2.setText('Sample')
            self.btnSaveP3.setText('Ruby')

            self.btnGoP1.setText('BKG')
            self.btnGoP2.setText('Sample')
            self.btnGoP3.setText('Ruby')

    def openparameters(self):
        AdvancedparametersWindow().setModal(True)
        AdvancedparametersWindow().show()
        AdvancedparametersWindow().exec_()

    def GoP1(self):
        execution(ser, 'ABSOL4')  # Motor 4
        xval = self.Position1X.text()
        position(ser, 4, xval)  # Motor 4
        move(ser, 4)  # Motor 4
        execution(ser, 'RELAT4')  # Motor 4

        execution(ser, 'ABSOL5')
        yval = self.Position1Y.text()
        position(ser, 5, str(-1 * int(yval)))
        move(ser, 5)
        execution(ser, 'RELAT5')

        execution(ser, 'ABSOL6')
        zval = self.Position1Z.text()
        position(ser, 6, zval)
        move(ser, 6)
        execution(ser, 'RELAT6')

    def GoP2(self):
        execution(ser, 'ABSOL4')  # Motor 4
        xval = self.Position2X.text()
        position(ser, 4, xval)  # Motor 4
        move(ser, 4)  # Motor 4
        execution(ser, 'RELAT4')  # Motor 4

        execution(ser, 'ABSOL5')
        yval = self.Position2Y.text()
        position(ser, 5, str(-1 * int(yval)))
        move(ser, 5)
        execution(ser, 'RELAT5')

        execution(ser, 'ABSOL6')
        zval = self.Position2Z.text()
        position(ser, 6, zval)
        move(ser, 6)
        execution(ser, 'RELAT6')

    def GoP3(self):
        execution(ser, 'ABSOL4')  # Motor 4
        xval = self.Position3X.text()
        position(ser, 4, xval)  # Motor 4
        move(ser, 4)  # Motor 4
        execution(ser, 'RELAT4')  # Motor 4

        execution(ser, 'ABSOL5')
        yval = self.Position3Y.text()
        position(ser, 5, str(-1 * int(yval)))
        move(ser, 5)
        execution(ser, 'RELAT5')

        execution(ser, 'ABSOL6')
        zval = self.Position3Z.text()
        position(ser, 6, zval)
        move(ser, 6)
        execution(ser, 'RELAT6')

    def SaveP1(self):
        self.Position1X.setText(execution(ser, '?CNT4'))  # Motor 4
        self.Position1Y.setText(str(-1 * int(execution(ser, '?CNT5'))))
        self.Position1Z.setText(execution(ser, '?CNT6'))

    def SaveP2(self):
        self.Position2X.setText(execution(ser, '?CNT4'))  # Motor 4
        self.Position2Y.setText(str(-1 * int(execution(ser, '?CNT5'))))
        self.Position2Z.setText(execution(ser, '?CNT6'))

    def SaveP3(self):
        self.Position3X.setText(execution(ser, '?CNT4'))  # Motor 4
        self.Position3Y.setText(str(-1 * int(execution(ser, '?CNT5'))))
        self.Position3Z.setText(execution(ser, '?CNT6'))

    def Xsetvalue(self):  # Motor 4
        execution(ser, 'ABSOL4')
        xval = self.SetpositionX.text()
        position(ser, 4, xval)
        move(ser, 4)
        execution(ser, 'RELAT4')

    def Ysetvalue(self):
        execution(ser, 'ABSOL5')
        yval = self.SetpositionY.text()
        position(ser, 5, str(-1 * int(yval)))
        move(ser, 5)
        execution(ser, 'RELAT5')

    def Zsetvalue(self):
        execution(ser, 'ABSOL6')
        zval = self.SetpositionZ.text()
        position(ser, 6, zval)
        move(ser, 6)
        execution(ser, 'RELAT6')

    def Xvalue(self):
        time.sleep(0.1)
        while (execution(ser, '?VACT4') != '0'):
            time.sleep(0.1)
        self.positionX.setText(execution(ser, '?CNT4'))

    def Yvalue(self):
        time.sleep(0.1)
        while (execution(ser, '?VACT5') != '0'):
            time.sleep(0.1)
        self.positionY.setText(str(-1 * int(execution(ser, '?CNT5'))))

    def Zvalue(self):
        time.sleep(0.1)
        while (execution(ser, '?VACT6') != '0'):
            time.sleep(0.1)
        self.positionZ.setText(execution(ser, '?CNT6'))

    def micromode(self):
        if self.radioButton_IR.isChecked():
            if (execution(ser, '?JACC1') == '1'):
                execution(ser, 'PSET1=0')
                execution(ser, 'PSET2=0')
            if (execution(ser, '?JACC1') == '2'):
                execution(ser, 'PSET1=-1500000')
                execution(ser, 'PSET2=1500000')
            execution(ser, 'PGO1')
            execution(ser, 'PGO2')
            execution(ser, 'JACC1=1')
        if self.radioButton_Raman.isChecked():
            if (execution(ser, '?JACC1') == '1'):
                execution(ser, 'PSET1=1500000')
                execution(ser, 'PSET2=-1500000')
            if (execution(ser, '?JACC1') == '2'):
                execution(ser, 'PSET1=0')
                execution(ser, 'PSET2=0')
            execution(ser, 'PGO1')
            execution(ser, 'PGO2')
            execution(ser, 'JACC1=2')

    def DACposition(self):
        if self.radioButton_Camera.isChecked():
            if (execution(ser, '?JACC3') == '1'):
                execution(ser, 'PSET3=-1500000')
            if (execution(ser, '?JACC3') == '2'):
                execution(ser, 'PSET3=0')
            execution(ser, 'PGO3')
            execution(ser, 'JACC3=2')
        if self.radioButton_Schwa.isChecked():
            if (execution(ser, '?JACC3') == '1'):
                execution(ser, 'PSET3=0')
            if (execution(ser, '?JACC3') == '2'):
                execution(ser, 'PSET3=1500000')
            execution(ser, 'PGO3')
            execution(ser, 'JACC3=1')

    def mouvementXh(self):
        position(ser, 4, int(self.stepX.text()))
        execution(ser, 'PGO4')  # Motor 4

    def mouvementXb(self):
        position(ser, 4, -1 * int(self.stepX.text()))
        execution(ser, 'PGO4')  # Motor 4

    def mouvementYh(self):
        position(ser, 5, -1 * int(self.stepY.text()))
        execution(ser, 'PGO5')

    def mouvementYb(self):
        position(ser, 5, 1 * int(self.stepY.text()))
        execution(ser, 'PGO5')

    def mouvementZh(self):
        position(ser, 6, 1 * int(self.stepZ.text()))
        execution(ser, 'PGO6')

    def mouvementZb(self):
        position(ser, 6, -1 * int(self.stepZ.text()))
        execution(ser, 'PGO6')

    def color(self):
        if not (self.radioButton_4.isChecked()):
            if not (self.radioButton_5.isChecked()):
                if not (self.radioButton_6.isChecked()):
                    execution(ser, 'JACC4=2')
                    self.labelSYZ.setText('Turn SYZ ON')
                    self.labelSYZ.setStyleSheet("QLabel {color : red}")
                    if not (self.radioButton_1.isChecked()):
                        if not (self.radioButton_2.isChecked()):
                            if not (self.radioButton_3.isChecked()):
                                execution(ser, 'JACC5=2')
                                self.btnAll.setStyleSheet("QPushButton {background : red}")
                                self.btnAll.setText('Turn all ON')
        if (self.radioButton_4.isChecked()):
            if (self.radioButton_5.isChecked()):
                if (self.radioButton_6.isChecked()):
                    execution(ser, 'JACC4=1')
                    self.labelSYZ.setText('Turn SYZ OFF')
                    self.labelSYZ.setStyleSheet("QLabel {color : green}")
                    if (self.radioButton_1.isChecked()):
                        if (self.radioButton_2.isChecked()):
                            if (self.radioButton_3.isChecked()):
                                execution(ser, 'JACC5=1')
                                self.btnAll.setStyleSheet("QPushButton {background : green}")
                                self.btnAll.setText('Turn all OFF')

    def SYZstatus(self):
        if (execution(ser, '?JACC4') == '1'):  # Turn them off
            execution(ser, 'MOFF4')
            execution(ser, 'MOFF5')
            execution(ser, 'MOFF6')
            self.radioButton_4.setChecked(False)
            self.radioButton_5.setChecked(False)
            self.radioButton_6.setChecked(False)
            status = 'off'
        if (execution(ser, '?JACC4') == '2'):  # Turn them on
            execution(ser, 'MON4')
            execution(ser, 'MON5')
            execution(ser, 'MON6')
            self.radioButton_4.setChecked(True)
            self.radioButton_5.setChecked(True)
            self.radioButton_6.setChecked(True)
            status = 'on'
        if (status == 'on'):
            execution(ser, 'JACC4=1')
            self.labelSYZ.setText('Turn SYZ OFF')
            self.labelSYZ.setStyleSheet("QLabel {color : green}")
        if (status == 'off'):
            execution(ser, 'JACC4=2')
            self.labelSYZ.setText('Turn SYZ ON')
            self.labelSYZ.setStyleSheet("QLabel {color : red}")

    def statusAll(self):
        if (execution(ser, '?JACC5') == '1'):  # Turn them all off
            execution(ser, 'MOFF1')
            execution(ser, 'MOFF2')
            execution(ser, 'MOFF3')
            execution(ser, 'MOFF4')
            execution(ser, 'MOFF5')
            execution(ser, 'MOFF6')
            self.radioButton_1.setChecked(False)
            self.radioButton_2.setChecked(False)
            self.radioButton_3.setChecked(False)
            self.radioButton_4.setChecked(False)
            self.radioButton_5.setChecked(False)
            self.radioButton_6.setChecked(False)
            status = 'all_off'
        if (execution(ser, '?JACC5') == '2'):  # Turn them all on
            execution(ser, 'MON1')
            execution(ser, 'MON2')
            execution(ser, 'MON3')
            execution(ser, 'MON4')
            execution(ser, 'MON5')
            execution(ser, 'MON6')
            self.radioButton_1.setChecked(True)
            self.radioButton_2.setChecked(True)
            self.radioButton_3.setChecked(True)
            self.radioButton_4.setChecked(True)
            self.radioButton_5.setChecked(True)
            self.radioButton_6.setChecked(True)
            status = 'all_on'
        if (status == 'all_on'):
            execution(ser, 'JACC5=1')
            self.btnAll.setStyleSheet("QPushButton {background : green}")
            self.btnAll.setText('Turn all OFF')
            execution(ser, 'JACC4=1')
            self.labelSYZ.setText('Turn SYZ OFF')
            self.labelSYZ.setStyleSheet("QLabel {color : green}")
        if (status == 'all_off'):
            execution(ser, 'JACC5=2')
            self.btnAll.setStyleSheet("QPushButton {background : red}")
            self.btnAll.setText('Turn all ON')
            execution(ser, 'JACC4=2')
            self.labelSYZ.setText('Turn SYZ ON')
            self.labelSYZ.setStyleSheet("QLabel {color : red}")

    def statemotor1(self):
        if self.radioButton_1.isChecked():
            execution(ser, 'MON1')
        if not (self.radioButton_1.isChecked()):
            execution(ser, 'MOFF1')
        self.color()

    def statemotor2(self):
        if self.radioButton_2.isChecked():
            execution(ser, 'MON2')
        if not (self.radioButton_2.isChecked()):
            execution(ser, 'MOFF2')
        self.color()

    def statemotor3(self):
        if self.radioButton_3.isChecked():
            execution(ser, 'MON3')
        if not (self.radioButton_3.isChecked()):
            execution(ser, 'MOFF3')
        self.color()

    def statemotor4(self):
        if self.radioButton_4.isChecked():
            execution(ser, 'MON4')
        if not (self.radioButton_4.isChecked()):
            execution(ser, 'MOFF4')
        self.color()

    def statemotor5(self):
        if self.radioButton_5.isChecked():
            execution(ser, 'MON5')
        if not (self.radioButton_5.isChecked()):
            execution(ser, 'MOFF5')
        self.color()

    def statemotor6(self):
        if self.radioButton_6.isChecked():
            execution(ser, 'MON6')
        if not (self.radioButton_6.isChecked()):
            execution(ser, 'MOFF6')
        self.color()

    def SetZero(self):
        execution(ser, 'CRES4')
        execution(ser, 'CRES5')
        execution(ser, 'CRES6')
        self.btnReadX.click()

    def stopall(self):
        execution(ser, 'JACC5=1')
        self.statusAll()


# ------Open the windows-----
def setup_old():
    logger.info('STEP: initial setup')
    app = QtGui.QApplication(sys.argv)  # A new instance of QApplication
    logger.info('\tDAC Position')
    form2 = DACpositionWindow()  # We set the form to be our ExampleApp (design)
    form2.show()
    logger.info('\tOptical Arrangement')
    form3 = MicromodeWindow()  # We set the form to be our ExampleApp (design)
    form3.show()
    app.exec_()  # and execute the app

def setup():
    logger.info('STEP: setup')
    app = QtGui.QApplication(sys.argv)  # A new instance of QApplication
    logger.info('\tDAC Position')
    form2 = DACpositionWindow()  # We set the form to be our ExampleApp (design)
    form2.show()
    logger.info('\tOptical Arrangement')
    form3 = MicromodeWindow()  # We set the form to be our ExampleApp (design)
    form3.show()
    app.exec_()  # and execute the app


def main():
    logger.info('STEP: main')
    logger.info('\tlaunching main window...')
    app = QtGui.QApplication(sys.argv)
    form = MainHorizontalWindow()  # We set the form to be our ExampleApp (design)
    form.show()
    app.exec_()  # and execute the app


def discover_and_connect():
    logger.info('STEP: discover_and_connect')
    logger.info('\tfind serial port and connect')
    # Code to choose the serial port used
    ## this could be done much more elegantyl. what is the way of finding out the # of com ports in a machine?
    # consider this
    # import serial.tools.list_ports
    #
    # ports = list(serial.tools.list_ports.comports())
    # for p in ports:
    #     print p
    # then just loop over these

    # choixport = 1
    # port = 0
    ser = serial.Serial  # why is this here?
    for port in range(50):  # (choixport == 1):
        logger.debug('\tChecking COM' + str(port + 1))
        try:
            # Open the port
            ser = serial.Serial(port='COM' + str(port + 1),
                                baudrate=9600,
                                stopbits=serial.STOPBITS_ONE,
                                bytesize=serial.EIGHTBITS)

            # try to get an answer from the PS90 controller. The answer would identify the system
            #  see ?ASTAT documentation
            longueur = len(execution(ser, '?ASTAT'))
            if (longueur == 9 and str(ser.isOpen()) == 'True'):  # this could be done without the "str()"
                choixport = 2
                logger.debug('\t...attempting to connect to COM' + str(port + 1) + ': success.')
                logger.info('\tConnected to COM' + str(port + 1) + '.')
                break
            if not (longueur == 9):
                logger.debug('\t...attempting to connect to COM' + str(port + 1) + ': failed')
                choixport = 1
        except:
            if (port < 50):
                port += 1
            else:
                logger.error('*** Connection error. Make sure USB cable is connected.')
                # input()
                # exit()
    if (port >= 49):
        logger.error(
            '*** Connection error, did not find PS90 controller below port<50. Make sure USB cable is connected.')
        ### would be nice to add a window here or at least a pause
        logger.error('--- Shutting down ---')
        exit()

    return (ser)
    # Emptying the buffer
    # ser.reset_input_buffer()
    # ser.reset_output_buffer()


def init_motors(ser):
    logger.info('STEP: init_motors')
    relat = ('RELAT1', 'RELAT2', 'RELAT3', 'RELAT4', 'RELAT5', 'RELAT6')
    mon = ('MON1', 'MON2', 'MON3', 'MON4', 'MON5', 'MON6')
    for i in range(0, 6, 1):
        execution(ser, relat[i])
        execution(ser, mon[i])
        initialisation(ser, str(i + 1))

    # ---Variables---
    execution(ser, 'JACC4=1')
    execution(ser, 'JACC5=1')


if __name__ == '__main__':  # if we're running file directly and not importing it

    ser = discover_and_connect()
    # init_motors(ser)
    init_motors(ser)
    setup()  # run the two configuration functions
    main()  # run the main function
    ser.close()
    logger.info('--- Clean Exit ---')
