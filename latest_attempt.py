"""See https://nfcpy.readthedocs.io/en/latest/topics/get-started.html#installation
and https://stackoverflow.com/questions/7991251/read-serial-id-mifare-with-pyscard
https://ludovicrousseau.blogspot.com/2010/04/pcsc-sample-in-python.html
https://pyscard.sourceforge.io/user-guide.html#the-answer-to-reset-atr

"""
import nfc
clf = nfc.ContactlessFrontend('usb')
while True:
    tag = clf.connect(rdwr={'on-connect': lambda tag: False})
    print(tag)
