import nfc
clf = nfc.ContactlessFrontend('usb')
while True:
    tag = clf.connect(rdwr={'on-connect': lambda tag: False})
    print(tag)
