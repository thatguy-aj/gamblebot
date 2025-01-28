'''Handles all operations in which chips are involved, saves and loads the users "wallet" which is defined as "memberData" and pickles and assigns it ot the discord userID'''
import os
import pickle
import time

dataFilename = 'data.pickle'

class Data():
    '''Creates the Data Structure for the memberData with values chips and bank'''
    def __init__(self, chips, bank):
        self.chips = chips
        self.bank = bank


def loadData(): 
    '''Deals with saving and loading memeber data from the pickle file'''
    if os.path.isfile(dataFilename):
        with open(dataFilename, 'rb') as file:
            return pickle.load(file)
    else:
        return dict()


def loadMemberData(memberID): 
    '''Gets a specific memebers data on the pickle file'''
    data = loadData()

    if memberID not in data:
        '''Creates a new data for the member if not in the data'''
        return Data(1000, 0)
    
    return data[memberID]

def saveMemberData(memberID, memberData):
    '''Saves the new values to the pickle file'''
    data = loadData()

    data[memberID] = memberData

    with open(dataFilename, 'wb') as file:
        pickle.dump(data, file)

'''Handles commands inputed by the user'''
def depositMember(memberData, amount):
    '''Adds value from players wallet to bank'''
    if amount > memberData.chips:
        return False
    memberData.bank += amount
    memberData.chips -= amount

def withdrawlMember(memberData, amount):
    '''Adds value from players bank to wallet'''
    if amount > memberData.bank:
        return False
    memberData.bank -= amount
    memberData.chips += amount

#TODO, add intrest for members that keep chips in their bank