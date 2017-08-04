import sys
from PyQt4 import QtGui, QtCore
import Fluke2635a
import serial
import configparser
import os
import csv

config = configparser.ConfigParser()
config.read('userConfig.cfg')

resultFolder = config['DEFAULT']['resultFolder']
limits = {'WN_pin2_hi':int(config['LIMITS']['ch1_hi']),
          'WN_pin2_lo':int(config['LIMITS']['ch1_lo']),
          'WN_pin11_hi':int(config['LIMITS']['ch2_hi']),
          'WN_pin11_lo':int(config['LIMITS']['ch2_lo']),         
          }


class mainGui(QtGui.QWidget):
        
    def __init__(self, **kwargs):
        super(mainGui, self).__init__()
        self.n = 0
        self.info1 = 0
        self.info2 = 0        
        self.measurementTaken = 0
        self.result = 'n/a'
        self.fieldnames = ['PCBA', 'MacID', 'Result', 'Pin2', 'Pin11']
        self.limits = kwargs["limits"]
        logDir = kwargs["resultFolder"]
        self.logFile = os.path.join(logDir, "ZC_Log.csv")
        self.initLogFile(self.logFile)
        self.ComPortUI()
        self.UI()
    
    def ComPortUI(self):
        availablePorts = Fluke2635a.ScanSeiralPorts()
        self.comPortBox = QtGui.QComboBox()
        self.comPortBox.addItems(availablePorts)
        self.comPortTestBtn = QtGui.QPushButton("Test Connection")
        self.comPortTestBtn.clicked.connect(self.testComPort)
    
    def initLogFile(self, logFile):        
        if not os.path.exists(os.path.dirname(logFile)):
            try:
                os.makedirs(os.path.dirname(logFile))
            except:
                pass        
        if not os.path.exists(logFile):
            with open(logFile, 'w') as of:
                csv_writer = csv.DictWriter(of, fieldnames=self.fieldnames, lineterminator='\n')
                csv_writer.writeheader()
    
    def testComPort(self):
        currentPort = str(self.comPortBox.currentText())
        test = Fluke2635a.DataLogger(port=currentPort,timeout=0, writeTimeout=0)
        if test.PortTest():
            self.statusLabel.setText('Connection to Fluke Datalogger Ok.')
            self.MeasureBtn.setEnabled(True)
        else:
            self.statusLabel.setText('Port test failed, try another port.')
            self.MeasureBtn.setEnabled(False)
        test.close()
        
        
    
    def UI(self):        
        self.EnterInfo1 = QtGui.QLineEdit('enter p/n')
        validator = QtGui.QRegExpValidator(QtCore.QRegExp("17[3|4]\d{6}.{1}"))
        self.EnterInfo1.setValidator(validator)
        self.EnterInfo1.setFocus()
        self.EnterInfo1.selectAll()
        self.EnterInfo1.editingFinished.connect(self.info1changed)
        
        
        self.EnterInfo2 = QtGui.QLineEdit('enter mac ID')
        validator = QtGui.QRegExpValidator(QtCore.QRegExp(r'00[:\.]{0,1}13[:\.]{0,1}50[:\.]{0,1}[0-9a-fA-F]{2}[:.]{0,1}[0-9a-fA-F]{2}[:.]{0,1}[0-9a-fA-F]{2}[:.]{0,1}[0-9a-fA-F]{2}[:.]{0,1}[0-9a-fA-F]{2}'))
        self.EnterInfo2.setValidator(validator)        
        self.EnterInfo2.editingFinished.connect(self.info2changed)
            
        self.MeasureBtn = QtGui.QPushButton('Manual Measure')
        self.MeasureBtn.clicked.connect(self.measure)
        self.MeasureBtn.setEnabled(False)
        
        self.RecordBtn = QtGui.QPushButton('Record Data')
        self.RecordBtn.setEnabled(False)
        self.RecordBtn.clicked.connect(self.recordData)
        
        self.Label1 = QtGui.QLabel('0L', self)
        self.Label1.setAlignment(QtCore.Qt.AlignCenter)
        self.Label2 = QtGui.QLabel('0L', self)
        self.Label2.setAlignment(QtCore.Qt.AlignCenter)
        self.statusLabel = QtGui.QLabel('status', self)
        
        someLayout = QtGui.QGridLayout()
        
        someLayout.addWidget(self.comPortBox, 5, 0, 1, 1)
        someLayout.addWidget(self.comPortTestBtn, 5, 1, 1, 1)        
        someLayout.addWidget(self.EnterInfo1, 10, 0, 1, 2)
        someLayout.addWidget(self.EnterInfo2, 15, 0, 1, 2)        
        someLayout.addWidget(self.RecordBtn, 25, 0, 1, 2)
        someLayout.addWidget(self.Label1, 30, 0, 1, 1)
        someLayout.addWidget(self.Label2, 30, 1, 1, 1)    
        someLayout.addWidget(self.MeasureBtn, 40, 0, 1, 2)
        someLayout.addWidget(self.statusLabel, 50, 0, 1, 2)
        
        self.setLayout(someLayout)
        
        
        self.setGeometry(300, 300, 300, 150)
        self.setWindowTitle('Check Ohms')
        self.show()

    
    def info1changed(self):
        #print "Hello, you entered: %s" % self.EnterInfo1.text()        
        self.info1 = 1
        self.EnterInfo2.setFocus()
        self.EnterInfo2.selectAll()
        if self.info2 == 1 and self.measurementTaken == 0:
            #print 'pn and mac Id is valid'            
            self.measure()        
            self.RecordBtn.setEnabled(True)
        elif self.info2 == 1 and self.measurementTaken == 1:
            self.RecordBtn.setEnabled(True)
            self.RecordBtn.setFocus()
    
    def info2changed(self):
        #print "Hello, you entered: %s" % self.EnterInfo2.text()
        self.info2 = 1
        if self.info1 == 1 and self.measurementTaken == 0:
            #print 'pn and mac Id is valid'
            self.RecordBtn.setEnabled(True)
            self.measure()  
            self.RecordBtn.setFocus()
        elif self.info1 == 1 and self.measurementTaken == 1:
            self.RecordBtn.setEnabled(True)
            self.RecordBtn.setFocus()
    
    def measure(self):
        currentPort = str(self.comPortBox.currentText())
        test = Fluke2635a.DataLogger(port=currentPort,timeout=0, writeTimeout=0)
        if test.PortTest():
            result =  test.ReadOhmsCh1and2()
            self.ch1 = result[0][1]
            self.ch2 = result[1][1]
            self.testData(self.ch1, self.ch2)
            #self.Label1.setText(str(ch1))
            #self.Label2.setText(str(ch2))
            self.measurementTaken = 1
            if self.info1 == 1 and self.info2 == 1:            
                self.RecordBtn.setEnabled(True)
        else:
            self.statusLabel.setText('Port test failed, try another port.')
            self.RecordBtn.setEnabled(False)            
        test.close()
    
    def recordData(self):
        #print "perform data recording"
        self.info1 = 0
        self.info2 = 0
        self.measurementTaken = 0
        #print self.Label1.text(), self.Label2.text()
        allResults = {'PCBA':str(self.EnterInfo1.text()),
               'MacID':'\''+str(self.EnterInfo2.text()),
               'Result':self.result,
               'Pin2':self.ch1,
               'Pin11':self.ch2}
        
        while True:
            try:
                with open(self.logFile, 'ab') as result_file:
                    result_writer = csv.DictWriter(result_file, fieldnames=self.fieldnames, lineterminator='\n')
                    result_writer.writerow(allResults)
                    self.resetUI()
                    break
            except IOError:
                self.saveFileFailMessage()
    
    def saveFileFailMessage(self):
        MESSAGE = "<p>Unable to save result.csv, did you open it somewhere else?"\
                  " Please close it and try again.</p>"
                  
        reply = QtGui.QMessageBox.critical(self, "Unable To Save Results",
                MESSAGE,
                QtGui.QMessageBox.Retry)
        if reply == QtGui.QMessageBox.Retry:
            return True  
    
    def resetUI(self):
        self.resetLabeln2()
        self.EnterInfo1.setText('enter p/n')
        self.EnterInfo2.setText('enter mac ID')
        self.EnterInfo1.setFocus()
        self.EnterInfo1.selectAll()
        self.RecordBtn.setEnabled(False)
        self.testComPort()
        self.ch1 = 999999999999
        self.ch1 = 999999999999
        self.result = 'N/A'
    
    def resetLabeln2(self):
        self.Label1.setText('0L')
        self.Label2.setText('0L')
        self.Label1.setStyleSheet("QLabel { color: %s;}" % 'black')
        self.Label2.setStyleSheet("QLabel { color: %s;}" % 'black')        
    
    def verifySingleData(self, value, label, hi_limit=200000, lo_limit=100000):        
        if value > lo_limit and value < hi_limit:            
            resultColor = 'green'
            fail_code = 0
        elif value < lo_limit:
            resultColor = 'red'
            fail_code = 1
        elif value > hi_limit:
            resultColor = 'red'
            fail_code = 2
            
        label.setText(str(value))
        label.setStyleSheet("QLabel { color: %s;}" % resultColor)
        return fail_code

    def testData(self, ch1, ch2):
        ch1_result = self.verifySingleData(ch1, self.Label1, 
                                           hi_limit=self.limits.get("WN_pin2_hi"),
                                           lo_limit=self.limits.get("WN_pin2_lo"),)
        ch2_result = self.verifySingleData(ch2, self.Label2,
                                           hi_limit=self.limits.get("WN_pin11_hi"),
                                           lo_limit=self.limits.get("WN_pin11_lo"),)
        
        if ch1_result > 0 and ch2_result > 0:
            self.statusLabel.setText("Unlikely both channel failed\ncheck if probe is plugged in correctly\nVerify with DMM, if still fails.\nscan pn and mac ID then record data and continue.")
            self.result = 'Fail'        
        elif ch1_result == 2 or ch2_result == 2:
            self.statusLabel.setText("Verify Test Probe Plugged in Correctly")
            self.result = 'Fail'
        elif ch1_result == 1 or ch2_result == 1:
            self.statusLabel.setText("Fail, scan p/n and mac ID then click Record Data.")
            self.result = 'Fail'
        elif ch1_result == 0 and ch2_result == 0:
            self.statusLabel.setText("Pass")
            self.result = 'Pass'
        
        
        
        
    
def main():    
    app = QtGui.QApplication(sys.argv)
    ex = mainGui(resultFolder = resultFolder, limits = limits)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()