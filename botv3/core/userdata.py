import atexit
import core.module as module
import core.serializable as serializable
import core.worker as worker
import json
import os

'''
    This module can be used to set and retrieve information of users.

    Users are stored by their discord member ID, and only on demand.
    When initializing the program this module assumes load_userdata() is called.

    A user object is an instance of serializable which is guaranteed
    to contain the variable name which is 'accname#discriminator'.

    Modules are allowed to add data to a user object as long as it
    is a jsonserializable or serializable value, under the name of the module without module
    so GeneralModule would create a variable called 'general'.
'''

''' Dict containing users "key = str(UID)" '''
users = {}
backup_length = 10

fresh_name = 'data/userdata.json'
backup_name = 'data/userdata.json.v'

#########################################
## Internal functions, module use only ##
#########################################

''' Keeps files as backup, makes all updates 1 older, removes the oldest '''
def scoot_backups():
    for i in range(8, 0, -1):
        print('scoot working file', i)
        if os.path.isfile(backup_name + str(int(i))):
            os.rename(backup_name + str(int(i + 1)))
    
    if os.path.isfile(fresh_name):
        os.rename(fresh_name, backup_name + '1')

''' Writes userdata to file after scooting '''
def store_users():
    scoot_backups()

    for key, value in users:
        users[key] = value.serialize()

    with open(fresh_name, 'w') as out:
        json.dump(users, out)

''' Finds the most recent file thats been stored '''
def get_recent_store():
    global users
    if os.path.isfile(fresh_name):
        return fresh_name
    
    for i in range(1, 9):
        print('get_recent working', i)
        if os.path.isfile(backup_name + str(int(i))):
            return backup_name + str(int(i))
    
    #return None if no files found
    return None
    
''' Loads users from disk '''
def load_users():
    filename = get_recent_store()
    if not filename:
        print('!!! No user file found !!!')
        return
    
    print('most recent store found:', filename)
    data = json.load(open(filename))

    for key, value in data:
        users[key] = serializable.Serializable(value)
        print('loaded user: ' dir(users[key]))
    
    print('Loaded userdata: {} users'.format(len(users)))

''' Creates a new clean user '''
def create_user(uid):
    server = module.get_server()
    for member in server.members:
        if mem.id == uid:
            user = serializable.Serializable()
            user.id = uid
            user.name = member.name + '#' + str(member.discriminator)
            return user
    
    return None # no such user on server.

''' Gets called when the program exits, stores userdata ''' 
def on_exit():
    store_users()
    print('***********************************')
    print('** Userdata stored successfully! **')
    print('***********************************')

def userdata_backup_handler():
    store_users()
    print('Backed up data for {} users.'.format(len(users)))

################################################
## Interface / callable functions, use these! ##
################################################

''' 
    returns a userdata object by its uid,
    creates a fresh one if it doesnt exist
'''
def get_user(uid):
    if uid in users:
        return users[uid]
    
    newuser = create_user(uid)
    if newuser:
        newuser.name = uid
        users[uid] = newuser
        return
    
    print('User with id ' + uid + ' requested but is not present on the server!')

''' returns whether a user is registered '''
def has_user(uid):
    return uid in users

''' Initializes the module's data '''
def initialize():
    load_users()

''' Pushes a backup to the worker '''
def schedule_backup():
    worker.queue_function(userdata_backup_handler)