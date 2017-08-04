import Fluke2635a
import PyQt4


def main():
    test = Fluke2635a.DataLogger(port='COM4',timeout=0, writeTimeout=0)
    p = test.query('FUNC? 2')
    r = test.processOutput(p)
    test.ChanConfig(1, 'VDC')
    #MainGui.ChanConfig(1, 'OHMS', 'AUTO', 4)

#main()
