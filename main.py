# --------------------------------------------------------------------

# Editeur: Matthias Glachant (glachant.matthias@gmail.com  )
# Date: 7/6/2016

# --------------------------------------------------------------------

from PyQt4 import QtGui  # Import the PyQt4 module we'll need
import sys  # We need sys so that we can pass argv to QApplication

import Horizontal_ui  # This file holds our MainWindow and all design related things
import Advancedparameters_ui
import DACposition_ui
import Micromode_ui

import time
import serial


###----------DEF_FONCTIONS--------------------------------------



def execution(commande):
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



def initialisation(motorNb):
    Nb = ('1', '2', '3', '4', '5', '6', '7', '8', '9')
    init = ('INIT1', 'INIT2', 'INIT3', 'INIT4', 'INIT5', 'INIT6', 'INIT7', 'INIT8', 'INIT9')
    execution(init[Nb.index(str(motorNb))])
    return ()



def deplacementmode(motorNb, mode):
    # mode=1 if ABSOLUTE, mode=2 if RELATIVE
    Nb = ('1', '2', '3', '4', '5', '6', '7', '8', '9')
    absol = ('ABSOL1', 'ABSOL2', 'ABSOL3', 'ABSOL4', 'ABSOL5', 'ABSOL6', 'ABSOL7', 'ABSOL8', 'ABSOL9')
    relat = ('RELAT1', 'RELAT2', 'RELAT3', 'RELAT4', 'RELAT5', 'RELAT6', 'RELAT7', 'RELAT8', 'RELAT9')
    if (mode == '1'):
        execution(absol[Nb.index(str(motorNb))])
        return ()
    if (mode == '2'):
        execution(relat[Nb.index(str(motorNb))])
        return ()


def velocity(motorNb, velocity):
    Nb = ('1', '2', '3', '4', '5', '6', '7', '8', '9')
    vel = ('IVEL1=', 'IVEL2=', 'IVEL3=', 'IVEL4=', 'IVEL5=', 'IVEL6=', 'IVEL7=', 'IVEL8=', 'IVEL9=')
    execution(vel[Nb.index(str(motorNb))] + str(velocity))
    return ()


def position(motorNb, position):
    Nb = ('1', '2', '3', '4', '5', '6', '7', '8', '9')
    pos = ('PSET1=', 'PSET2=', 'PSET3=', 'PSET4=', 'PSET5=', 'PSET6=', 'PSET7=', 'PSET8=', 'PSET9=')
    execution(pos[Nb.index(str(motorNb))] + str(position))
    return ()


def move(motorNb):
    Nb = ('1', '2', '3', '4', '5', '6', '7', '8', '9')
    mov = ('PGO1', 'PGO2', 'PGO3', 'PGO4', 'PGO5', 'PGO6', 'PGO7', 'PGO8', 'PGO9')
    execution(mov[Nb.index(str(motorNb))])
    return ()


def acceleration(motorNb, acceleration):
    Nb = ('1', '2', '3', '4', '5', '6', '7', '8', '9')
    acc = ('ACC1=', 'ACC2=', 'ACC3=', 'ACC4=', 'ACC5=', 'ACC6=', 'ACC7=', 'ACC8=', 'ACC9=')
    execution(acc[Nb.index(str(motorNb))] + str(acceleration))
    return ()


def deceleration(motorNb, deceleration):
    Nb = ('1', '2', '3', '4', '5', '6', '7', '8', '9')
    acc = ('DACC1=', 'DACC2=', 'DACC3=', 'DACC4=', 'DACC5=', 'DACC6=', 'DACC7=', 'DACC8=', 'DACC9=')
    execution(acc[Nb.index(str(motorNb))] + str(deceleration))
    return ()


def stop(motorNb):
    Nb = ('1', '2', '3', '4', '5', '6', '7', '8', '9')
    stp = ('STOP1', 'STOP2', 'STOP3', 'STOP4', 'STOP5', 'STOP6', 'STOP7', 'STOP8', 'STOP9')
    execution(stp[Nb.index(str(motorNb))])
    return ()


def positionvalue(motorNb):
    Nb = ('1', '2', '3', '4', '5', '6', '7', '8', '9')
    pos = ('?CNT1', '?CNT2', '?CNT3', '?CNT4', '?CNT5', '?CNT6', '?CNT7', '?CNT8', '?CNT9')
    position = execution(pos[Nb.index(motorNb)])
    return (position[0])


def speedvalue(motorNb):
    Nb = ('1', '2', '3', '4', '5', '6', '7', '8', '9')
    speed = ('?IVEL1', '?IVEL2', '?IVEL3', '?IVEL4', '?IVEL5', '?IVEL6', '?IVEL7', '?IVEL8', '?IVEL9')
    speedval = execution(speed[Nb.index(motorNb)])
    return (speedval[0])


def PcalcDiamondRaman(P_range, peak_position, diamond_peak = 1334):
    # these are the formulas that Paul Loubeyre uses to calculate his pressure
    if P_range < 200:

        return int(100*np.around(547*((peak_position-diamond_peak)/diamond_peak)*(1+0.5*(3.75-1)*
                        (peak_position-diamond_peak)/diamond_peak), decimals=3))/100
    if P_range > 200:
        return int(100*np.around(3141-4.157*peak_position+1.429e-3*peak_position**2,decimals=3))/100

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
            self.position.setText(execution('?CNT' + str(motorNB)))
        if (motorNB == 5):
            self.position.setText(str(-1 * int(execution('?CNT' + str(motorNB)))))

    def mouvementplus(self):
        motorNB = self.comboBox.currentIndex() + 1
        if (motorNB != 5):
            execution('PSET' + str(motorNB) + '=' + str(self.step.text()))
            execution('PGO' + str(motorNB))
            time.sleep(0.1)
            while (execution('?VACT' + str(motorNB)) != '0'):
                time.sleep(0.1)
            self.position.setText(execution('?CNT' + str(motorNB)))
        if (motorNB == 5):
            execution('PSET' + str(motorNB) + '=-' + str(self.step.text()))
            execution('PGO' + str(motorNB))
            time.sleep(0.1)
            while (execution('?VACT' + str(motorNB)) != '0'):
                time.sleep(0.1)
            self.position.setText(str(-1 * int(execution('?CNT' + str(motorNB)))))

    def mouvementmoins(self):
        motorNB = self.comboBox.currentIndex() + 1
        if (motorNB != 5):
            execution('PSET' + str(motorNB) + '=-' + str(self.step.text()))
            execution('PGO' + str(motorNB))
            time.sleep(0.1)
            while (execution('?VACT' + str(motorNB)) != '0'):
                time.sleep(0.1)
            self.position.setText(execution('?CNT' + str(motorNB)))
        if (motorNB == 5):
            motorNB = self.comboBox.currentIndex() + 1
            execution('PSET' + str(motorNB) + '=' + str(self.step.text()))
            execution('PGO' + str(motorNB))
            time.sleep(0.1)
            while (execution('?VACT' + str(motorNB)) != '0'):
                time.sleep(0.1)
            self.position.setText(str(-1 * int(execution('?CNT' + str(motorNB)))))

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
            execution('SAVEAXPA' + str(i))

    def seeparam(self):
        self.xyzAccAct.setText(execution('?ACC4'))
        self.xyzDecAct.setText(execution('?DACC4'))
        self.xyzSpeedAct.setText(execution('?IVEL4'))
        self.largeAccAct.setText(execution('?ACC1'))
        self.largeDecAct.setText(execution('?DACC1'))
        self.largeSpeedAct.setText(execution('?IVEL1'))

class DACpositionWindow(QtGui.QDialog, DACposition_ui.Ui_Form):
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)

        self.btnCamera.clicked.connect(self.cameramode)
        self.btnSchwa.clicked.connect(self.schwamode)

    def cameramode(self):
        execution('JACC3=2')

    def schwamode(self):
        execution('JACC3=1')

class MicromodeWindow(QtGui.QDialog, Micromode_ui.Ui_Microscopemode):
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)

        self.btnIRmode.clicked.connect(self.IRmode)
        self.btnRamanmode.clicked.connect(self.Ramanmode)

    def IRmode(self):
        execution('JACC1=1')

    def Ramanmode(self):
        execution('JACC1=2')

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
        if (execution('?JACC3') == '1'):
            self.radioButton_Schwa.setChecked(True)
        if (execution('?JACC3') == '2'):
            self.radioButton_Camera.setChecked(True)
        if (execution('?JACC1') == '1'):
            self.radioButton_IR.setChecked(True)
        if (execution('?JACC1') == '2'):
            self.radioButton_Raman.setChecked(True)
        self.btnSYZ.clicked.connect(self.SYZstatus)
        self.btnAll.clicked.connect(self.statusAll)
        self.btnAll.setStyleSheet("QPushButton {background : green}")
        self.btnAll.setText('Turn all OFF')
        self.labelSYZ.setText('Turn SYZ OFF')
        self.labelSYZ.setStyleSheet("QLabel {color : green}")
        self.btnSetzero.clicked.connect(self.SetZero)

        # Feri
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
        execution('ABSOL4')  # Motor 4
        xval = self.Position1X.text()
        position(4, xval)  # Motor 4
        move(4)  # Motor 4
        execution('RELAT4')  # Motor 4

        execution('ABSOL5')
        yval = self.Position1Y.text()
        position(5, str(-1 * int(yval)))
        move(5)
        execution('RELAT5')

        execution('ABSOL6')
        zval = self.Position1Z.text()
        position(6, zval)
        move(6)
        execution('RELAT6')

    def GoP2(self):
        execution('ABSOL4')  # Motor 4
        xval = self.Position2X.text()
        position(4, xval)  # Motor 4
        move(4)  # Motor 4
        execution('RELAT4')  # Motor 4

        execution('ABSOL5')
        yval = self.Position2Y.text()
        position(5, str(-1 * int(yval)))
        move(5)
        execution('RELAT5')

        execution('ABSOL6')
        zval = self.Position2Z.text()
        position(6, zval)
        move(6)
        execution('RELAT6')

    def GoP3(self):
        execution('ABSOL4')  # Motor 4
        xval = self.Position3X.text()
        position(4, xval)  # Motor 4
        move(4)  # Motor 4
        execution('RELAT4')  # Motor 4

        execution('ABSOL5')
        yval = self.Position3Y.text()
        position(5, str(-1 * int(yval)))
        move(5)
        execution('RELAT5')

        execution('ABSOL6')
        zval = self.Position3Z.text()
        position(6, zval)
        move(6)
        execution('RELAT6')

    def SaveP1(self):
        self.Position1X.setText(execution('?CNT4'))  # Motor 4
        self.Position1Y.setText(str(-1 * int(execution('?CNT5'))))
        self.Position1Z.setText(execution('?CNT6'))

    def SaveP2(self):
        self.Position2X.setText(execution('?CNT4'))  # Motor 4
        self.Position2Y.setText(str(-1 * int(execution('?CNT5'))))
        self.Position2Z.setText(execution('?CNT6'))

    def SaveP3(self):
        self.Position3X.setText(execution('?CNT4'))  # Motor 4
        self.Position3Y.setText(str(-1 * int(execution('?CNT5'))))
        self.Position3Z.setText(execution('?CNT6'))

    def Xsetvalue(self):  # Motor 4
        execution('ABSOL4')
        xval = self.SetpositionX.text()
        position(4, xval)
        move(4)
        execution('RELAT4')

    def Ysetvalue(self):
        execution('ABSOL5')
        yval = self.SetpositionY.text()
        position(5, str(-1 * int(yval)))
        move(5)
        execution('RELAT5')

    def Zsetvalue(self):
        execution('ABSOL6')
        zval = self.SetpositionZ.text()
        position(6, zval)
        move(6)
        execution('RELAT6')

    def Xvalue(self):
        time.sleep(0.1)
        while (execution('?VACT4') != '0'):
            time.sleep(0.1)
        self.positionX.setText(execution('?CNT4'))

    def Yvalue(self):
        time.sleep(0.1)
        while (execution('?VACT5') != '0'):
            time.sleep(0.1)
        self.positionY.setText(str(-1 * int(execution('?CNT5'))))

    def Zvalue(self):
        time.sleep(0.1)
        while (execution('?VACT6') != '0'):
            time.sleep(0.1)
        self.positionZ.setText(execution('?CNT6'))

    def micromode(self):
        if self.radioButton_IR.isChecked():
            if (execution('?JACC1') == '1'):
                execution('PSET1=0')
                execution('PSET2=0')
            if (execution('?JACC1') == '2'):
                execution('PSET1=-1500000')
                execution('PSET2=1500000')
            execution('PGO1')
            execution('PGO2')
            execution('JACC1=1')
        if self.radioButton_Raman.isChecked():
            if (execution('?JACC1') == '1'):
                execution('PSET1=1500000')
                execution('PSET2=-1500000')
            if (execution('?JACC1') == '2'):
                execution('PSET1=0')
                execution('PSET2=0')
            execution('PGO1')
            execution('PGO2')
            execution('JACC1=2')

    def DACposition(self):
        if self.radioButton_Camera.isChecked():
            if (execution('?JACC3') == '1'):
                execution('PSET3=-1500000')
            if (execution('?JACC3') == '2'):
                execution('PSET3=0')
            execution('PGO3')
            execution('JACC3=2')
        if self.radioButton_Schwa.isChecked():
            if (execution('?JACC3') == '1'):
                execution('PSET3=0')
            if (execution('?JACC3') == '2'):
                execution('PSET3=1500000')
            execution('PGO3')
            execution('JACC3=1')

    def mouvementXh(self):
        position(4, int(self.stepX.text()))
        execution('PGO4')  # Motor 4

    def mouvementXb(self):
        position(4, -1 * int(self.stepX.text()))
        execution('PGO4')  # Motor 4

    def mouvementYh(self):
        position(5, -1 * int(self.stepY.text()))
        execution('PGO5')

    def mouvementYb(self):
        position(5, 1 * int(self.stepY.text()))
        execution('PGO5')

    def mouvementZh(self):
        position(6, 1 * int(self.stepZ.text()))
        execution('PGO6')

    def mouvementZb(self):
        position(6, -1 * int(self.stepZ.text()))
        execution('PGO6')

    def color(self):
        if not (self.radioButton_4.isChecked()):
            if not (self.radioButton_5.isChecked()):
                if not (self.radioButton_6.isChecked()):
                    execution('JACC4=2')
                    self.labelSYZ.setText('Turn SYZ ON')
                    self.labelSYZ.setStyleSheet("QLabel {color : red}")
                    if not (self.radioButton_1.isChecked()):
                        if not (self.radioButton_2.isChecked()):
                            if not (self.radioButton_3.isChecked()):
                                execution('JACC5=2')
                                self.btnAll.setStyleSheet("QPushButton {background : red}")
                                self.btnAll.setText('Turn all ON')
        if (self.radioButton_4.isChecked()):
            if (self.radioButton_5.isChecked()):
                if (self.radioButton_6.isChecked()):
                    execution('JACC4=1')
                    self.labelSYZ.setText('Turn SYZ OFF')
                    self.labelSYZ.setStyleSheet("QLabel {color : green}")
                    if (self.radioButton_1.isChecked()):
                        if (self.radioButton_2.isChecked()):
                            if (self.radioButton_3.isChecked()):
                                execution('JACC5=1')
                                self.btnAll.setStyleSheet("QPushButton {background : green}")
                                self.btnAll.setText('Turn all OFF')

    def SYZstatus(self):
        if (execution('?JACC4') == '1'):  # Turn them off
            execution('MOFF4')
            execution('MOFF5')
            execution('MOFF6')
            self.radioButton_4.setChecked(False)
            self.radioButton_5.setChecked(False)
            self.radioButton_6.setChecked(False)
            status = 'off'
        if (execution('?JACC4') == '2'):  # Turn them on
            execution('MON4')
            execution('MON5')
            execution('MON6')
            self.radioButton_4.setChecked(True)
            self.radioButton_5.setChecked(True)
            self.radioButton_6.setChecked(True)
            status = 'on'
        if (status == 'on'):
            execution('JACC4=1')
            self.labelSYZ.setText('Turn SYZ OFF')
            self.labelSYZ.setStyleSheet("QLabel {color : green}")
        if (status == 'off'):
            execution('JACC4=2')
            self.labelSYZ.setText('Turn SYZ ON')
            self.labelSYZ.setStyleSheet("QLabel {color : red}")

    def statusAll(self):
        if (execution('?JACC5') == '1'):  # Turn them all off
            execution('MOFF1')
            execution('MOFF2')
            execution('MOFF3')
            execution('MOFF4')
            execution('MOFF5')
            execution('MOFF6')
            self.radioButton_1.setChecked(False)
            self.radioButton_2.setChecked(False)
            self.radioButton_3.setChecked(False)
            self.radioButton_4.setChecked(False)
            self.radioButton_5.setChecked(False)
            self.radioButton_6.setChecked(False)
            status = 'all_off'
        if (execution('?JACC5') == '2'):  # Turn them all on
            execution('MON1')
            execution('MON2')
            execution('MON3')
            execution('MON4')
            execution('MON5')
            execution('MON6')
            self.radioButton_1.setChecked(True)
            self.radioButton_2.setChecked(True)
            self.radioButton_3.setChecked(True)
            self.radioButton_4.setChecked(True)
            self.radioButton_5.setChecked(True)
            self.radioButton_6.setChecked(True)
            status = 'all_on'
        if (status == 'all_on'):
            execution('JACC5=1')
            self.btnAll.setStyleSheet("QPushButton {background : green}")
            self.btnAll.setText('Turn all OFF')
            execution('JACC4=1')
            self.labelSYZ.setText('Turn SYZ OFF')
            self.labelSYZ.setStyleSheet("QLabel {color : green}")
        if (status == 'all_off'):
            execution('JACC5=2')
            self.btnAll.setStyleSheet("QPushButton {background : red}")
            self.btnAll.setText('Turn all ON')
            execution('JACC4=2')
            self.labelSYZ.setText('Turn SYZ ON')
            self.labelSYZ.setStyleSheet("QLabel {color : red}")

    def statemotor1(self):
        if self.radioButton_1.isChecked():
            execution('MON1')
        if not (self.radioButton_1.isChecked()):
            execution('MOFF1')
        self.color()

    def statemotor2(self):
        if self.radioButton_2.isChecked():
            execution('MON2')
        if not (self.radioButton_2.isChecked()):
            execution('MOFF2')
        self.color()

    def statemotor3(self):
        if self.radioButton_3.isChecked():
            execution('MON3')
        if not (self.radioButton_3.isChecked()):
            execution('MOFF3')
        self.color()

    def statemotor4(self):
        if self.radioButton_4.isChecked():
            execution('MON4')
        if not (self.radioButton_4.isChecked()):
            execution('MOFF4')
        self.color()

    def statemotor5(self):
        if self.radioButton_5.isChecked():
            execution('MON5')
        if not (self.radioButton_5.isChecked()):
            execution('MOFF5')
        self.color()

    def statemotor6(self):
        if self.radioButton_6.isChecked():
            execution('MON6')
        if not (self.radioButton_6.isChecked()):
            execution('MOFF6')
        self.color()

    def SetZero(self):
        execution('CRES4')
        execution('CRES5')
        execution('CRES6')
        self.btnReadX.click()

    def stopall(self):
        execution('JACC5=1')
        self.statusAll()


# ------Open the windows-----
def setup():
    app = QtGui.QApplication(sys.argv)  # A new instance of QApplication
    form2 = DACpositionWindow()  # We set the form to be our ExampleApp (design)
    form2.show()
    form3 = MicromodeWindow()  # We set the form to be our ExampleApp (design)
    form3.show()
    app.exec_()  # and execute the app

def main():
    app = QtGui.QApplication(sys.argv)
    form = MainHorizontalWindow()  # We set the form to be our ExampleApp (design)
    form.show()
    app.exec_()  # and execute the app



def discover_and_connect():
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
    for port in range(50):# (choixport == 1):
        try:
            # Open the port
            ser = serial.Serial(port='COM' + str(port+1),
                                baudrate=9600,
                                stopbits=serial.STOPBITS_ONE,
                                bytesize=serial.EIGHTBITS)

            # try to get an answer from the PS90 controller. The answer would identify the system
            #  see ?ASTAT documentation
            longueur = len(execution('?ASTAT'))
            if (longueur == 9 and str(ser.isOpen()) == 'True'):  # this could be done without the "str()"
                choixport = 2
            if not (longueur == 9):
                choixport = 1
        except:
            if (port < 50):
                port += 1
            else:
                print(port, 'Make sure that the controller is connected to your computer')
                # input()
                # exit()

    print('controler connected on', 'COM' + str(port), ':', ser.isOpen())

    return(ser)
    # Emptying the buffer
    # ser.reset_input_buffer()
    # ser.reset_output_buffer()

def init_motors(ser):
    relat = ('RELAT1', 'RELAT2', 'RELAT3', 'RELAT4', 'RELAT5', 'RELAT6')
    mon = ('MON1', 'MON2', 'MON3', 'MON4', 'MON5', 'MON6')
    for i in range(0, 6, 1):
        execution(relat[i])
        execution(mon[i])
        initialisation(str(i + 1))

    # ---Variables---
    execution('JACC4=1')
    execution('JACC5=1')

if __name__ == '__main__':  # if we're running file directly and not importing it

    serial_port = discover_and_connect()
    init_motors(ser)
    setup()  # run the two configuration functions
    main()  # run the main function
