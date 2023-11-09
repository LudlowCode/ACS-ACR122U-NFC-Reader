#! /usr/bin/env python3
"""
Using pyscard to log NFC taps.
"""

from smartcard.scard import *
import smartcard.util

srTreeATR = \
    [0x3B, 0x77, 0x94, 0x00, 0x00, 0x82, 0x30, 0x00, 0x13, 0x6C, 0x9F, 0x22]
srTreeMask = \
    [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]



def printstate(state):
    reader, eventstate, atr = state
    print(reader + " " + smartcard.util.toHexString(atr, smartcard.util.HEX))
    with open("users.txt", "a") as users_file:
        users_file.write(smartcard.util.toHexString(atr, smartcard.util.HEX) +"\tUnknown\n")
    if eventstate & SCARD_STATE_ATRMATCH:
        print('\tCard found')
    if eventstate & SCARD_STATE_UNAWARE:
        print('\tState unware')
        
    if eventstate & SCARD_STATE_IGNORE:
        print('\tIgnore reader')
    if eventstate & SCARD_STATE_UNAVAILABLE:
        print('\tReader unavailable')
    if eventstate & SCARD_STATE_EMPTY:
        print('\tReader empty')
    if eventstate & SCARD_STATE_PRESENT:
        print('\tCard present in reader')
    if eventstate & SCARD_STATE_EXCLUSIVE:
        print('\tCard allocated for exclusive use by another application')
    if eventstate & SCARD_STATE_INUSE:
        print('\tCard in used by another application but can be shared')
    if eventstate & SCARD_STATE_MUTE:
        print('\tCard is mute')
    if eventstate & SCARD_STATE_CHANGED:
        print('\tState changed')
    if eventstate & SCARD_STATE_UNKNOWN:
        print('\tState unknowned')

def log_cards():
    while True:
        try:
            hresult, hcontext = SCardEstablishContext(SCARD_SCOPE_USER)
            if hresult != SCARD_S_SUCCESS:
                raise error(
                    'Failed to establish context: ' +
                    SCardGetErrorMessage(hresult))
            print('Context established!')

            try:
                hresult, readers = SCardListReaders(hcontext, [])
                if hresult != SCARD_S_SUCCESS:
                    raise error(
                        'Failed to list readers: ' +
                        SCardGetErrorMessage(hresult))
                print('PCSC Readers:', readers)

                readerstates = []
                for i in range(len(readers)):
                    readerstates += [(readers[i], SCARD_STATE_UNAWARE)]

                print('----- Current reader and card states are: -------')
                hresult, newstates = SCardGetStatusChange(hcontext, 0, readerstates)
                for i in newstates:
                    printstate(i)

                print('----- Please insert or remove a card ------------')
                hresult, newstates = SCardGetStatusChange(
                                        hcontext,
                                        INFINITE,
                                        newstates)

                print('----- New reader and card states are: -----------')
                for i in newstates:
                    printstate(i)

            finally:
                hresult = SCardReleaseContext(hcontext)
                if hresult != SCARD_S_SUCCESS:
                    raise error(
                        'Failed to release context: ' +
                        SCardGetErrorMessage(hresult))
                print('Released context.')

        except error as e:
            print(e)
        
log_cards()