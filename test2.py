import sys
from PyQt4 import QtGui, QtCore

class Example(QtGui.QWidget):
    
    def __init__(self):
        super(Example, self).__init__()
        
        self.initUI()
        
    def initUI(self):
        
        # Declare widgets
        self.templbl = QtGui.QLabel("Enter Temperature : ", self)
        self.temp2lbl = QtGui.QLabel("Degrees", self)
        self.tempLEdit= QtGui.QLineEdit(self)
        self.calculateBtn = QtGui.QPushButton("Calculate")
        self.clearBtn = QtGui.QPushButton("Clear")
        
        self.calculateBtn.clicked.connect(self.result)
        self.clearBtn.clicked.connect(self.clearEntry)

        someLayout = QtGui.QGridLayout()
        someLayout.addWidget(self.templbl)
        someLayout.addWidget(self.tempLEdit)
        someLayout.addWidget(self.temp2lbl)
        someLayout.addWidget(self.calculateBtn)
        someLayout.addWidget(self.clearBtn)
        someLayout.addWidget(self.tempLEdit)
        self.setLayout(someLayout)
        
#         # first line widgets
#         self.hBox1 = QtGui.QHBoxLayout()
#         self.hBox1.addWidget(self.templbl)
#         self.hBox1.addStretch(1)
#         self.hBox1.addWidget(self.tempLEdit)
#         
#         # second line widgets
#         self.hBox2 = QtGui.QHBoxLayout()
#         self.hBox2.addWidget(self.temp2lbl)
# 
#         
#         # third line widgets
#         self.hBox3 = QtGui.QHBoxLayout()
#         self.hBox3.addStretch(1)
#         self.hBox3.addWidget(self.calculateBtn)
#         self.hBox3.addWidget(self.clearBtn)
#         
#         self.vbox = QtGui.QVBoxLayout()
#         self.vbox.addLayout(self.hBox1)
#         self.vbox.addLayout(self.hBox2)
#         self.vbox.addStretch(1)
#         self.vbox.addLayout(self.hBox3)
#         
#         self.setLayout(self.vbox) 
        
        self.setGeometry(300, 300, 500, 250)
        self.setWindowTitle("Temperature Converter")    
        self.show()
    
    def calculateCelsius(self,n):
        ans =  5 * (float(n) - 32)/9
        return ans
    
    def result(self):
        num = self.tempLEdit.text()
        answer = self.calculateCelsius(num)
        self.temp2lbl.setText("Is " + str("%.2f" % answer) + " Degrees Celsius")
        
    def clearEntry(self):
        self.tempLEdit.clear()
     
    

        
def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

