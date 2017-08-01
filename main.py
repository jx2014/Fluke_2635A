import Fluke2635a

def main():
    test = Fluke2635a.DataLogger(port='COM4',timeout=0)
    p = test.query('FUNC? 2')
    r = test.processOutput(p)
    test.ChanConfig(1, 'VDC')
    #test.ChanConfig(1, 'OHMS', 'AUTO', 4)

main()