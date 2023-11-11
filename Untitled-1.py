#! /usr/bin/env python3
"""
Using pyscard to log NFC taps.
"""

from smartcard.scard import *
import smartcard.util
import time
import os.path
import shutil
import json
USERS_FILENAME = "users.json"
debug_mode = False
srTreeATR = \
    [0x3B, 0x77, 0x94, 0x00, 0x00, 0x82, 0x30, 0x00, 0x13, 0x6C, 0x9F, 0x22]
srTreeMask = \
    [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]

def backup_file(filename):
    timestr = time.strftime("%Y-%m-%d-%H-%M-%S")
    new_filename = "backup-"+timestr+filename
    print(f"Backing up {filename} to {new_filename} at {timestr}")
    shutil.copy(filename, new_filename)

def get_users_dict():
    """WARNING: this will wipe previous user data!
    """
    if os.path.exists(USERS_FILENAME):
        backup_file(USERS_FILENAME)
        with open(USERS_FILENAME,'r') as json_file:
            users = json.load(json_file)
    else:
        users = {}
    return users
def log_user(card_atr:str, users:dict):
    if card_atr == '':
        return
    if users.get(card_atr)==None:
        users[card_atr] = {}
        print('\a')
        users[card_atr]["name"]=input("Unknown user; please type your name and press enter... ")
        users[card_atr]["logs"]=[]
    name = users[card_atr]["name"]
    print("Hi", name)
    users[card_atr]["logs"].append(time.ctime())
    save_user_data(users)

def save_user_data(users:dict, filename = USERS_FILENAME):
    with open(filename,'w') as f:
        json.dump(users, f)

def printstate(state, users):
    reader, eventstate, atr = state
    #if eventstate & SCARD
    print(f"Event state is {eventstate}")
    #print(reader + " " + smartcard.util.toHexString(atr, smartcard.util.HEX))
    log_user(smartcard.util.toHexString(atr, smartcard.util.HEX), users)
    if debug_mode:
        
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

def log_cards(users:dict):
    while True:
        try:
            hresult, hcontext = SCardEstablishContext(SCARD_SCOPE_USER)
            if hresult != SCARD_S_SUCCESS:
                raise error(
                    'Failed to establish context: ' +
                    SCardGetErrorMessage(hresult))
            #print('Context established!')

            try:
                hresult, readers = SCardListReaders(hcontext, [])
                if hresult != SCARD_S_SUCCESS:
                    raise error(
                        'Failed to list readers: ' +
                        SCardGetErrorMessage(hresult))
                #print('PCSC Readers:', readers)

                readerstates = []
                for i in range(len(readers)):
                    readerstates += [(readers[i], SCARD_STATE_UNAWARE)]

                #print('----- Current reader and card states are: -------')
                hresult, newstates = SCardGetStatusChange(hcontext, 0, readerstates)
                if debug_mode:
                    for i in newstates:
                        printstate(i, users)

                #print('----- Please insert or remove a card ------------')
                hresult, newstates = SCardGetStatusChange(
                                        hcontext,
                                        INFINITE,
                                        newstates)

                #print('----- New reader and card states are: -----------')
                for i in newstates:
                    printstate(i, users)

            finally:
                hresult = SCardReleaseContext(hcontext)
                if hresult != SCARD_S_SUCCESS:
                    raise error(
                        'Failed to release context: ' +
                        SCardGetErrorMessage(hresult))
                #print('Released context.')

        except error as e:
            print(e)
users = get_users_dict()       
log_cards(users)