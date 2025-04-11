'''Handles all operations in which chips are involved, saves and loads the users "wallet" which is defined as "memberData" and pickles and assigns it ot the discord userID'''
import os
import pickle
import time

dataFilename = 'data.pickle'

class Data():
    '''Creates the Data Structure for the memberData with values chips and bank'''
    def __init__(self, chips, bank):
        self.value = {"chips": chips, "bank": bank}

def loadData():
    if os.path.isfile(dataFilename):
        try:
            with open(dataFilename, 'rb') as file:
                return pickle.load(file)
        except (EOFError, pickle.UnpicklingError):
            print("Warning: Pickle file is corrupted or empty. Reinitializing.")
            return {}
    else:
        return {}

def loadMemberData(memberID): 
    '''Gets a specific memebers data on the pickle file'''
    data = loadData()

    if memberID not in data:
        '''Creates a new data for the member if not in the data'''
        return Data(1000, 0)
    
    return data[memberID]

def load_all_data():
    '''Loads and returns the entire member data dictionary from the pickle file, returns dictionary of members'''
    if os.path.isfile(dataFilename):
        with open(dataFilename, 'rb') as file:
            data = pickle.load(file)
            return data
    else:
        return dict()

def saveMemberData(memberID, memberData):
    '''Saves the new values to the pickle file'''
    data = loadData()

    data[memberID] = memberData

    with open(dataFilename, 'wb') as file:
        pickle.dump(data, file)

def clear_pickle_file():
    """Clears the content of the pickle file by resetting it to an empty dictionary."""
    with open(dataFilename, 'wb') as file:
        pickle.dump({}, file)  # reset to an empty dict
    print(f"Pickle file '{dataFilename}' cleared.")

'''Handles commands inputed by the user'''
def depositMember(memberData, amount):
    if amount > memberData.value["chips"]:
        return False
    memberData.value["bank"] += amount
    memberData.value["chips"] -= amount
    return True  

def withdrawlMember(memberData, amount):
    if amount > memberData.value["bank"]:
        return False
    memberData.value["bank"] -= amount
    memberData.value["chips"] += amount
    return True  

#TODO, add intrest for members that keep chips in their bank
