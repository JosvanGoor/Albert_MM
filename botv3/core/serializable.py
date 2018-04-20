import json

'''
    This class offers a (very) simple (de-)serialization interface to and from json.
'''

class Serializable:

    '''
        Recursively reconstructs the original data structure
        If an object inherits Serializable it must call 
        "super(x).__init__(dict)" to be reconstructed.
    '''
    def __init__(self, input={}):
        for key, val in input.items():
            if isinstance(val, dict):
                self.__dict__[key] = Serializable(val)
            else:
                self.__dict__[key] = val

    '''
        Recursively serializes the object, does not account for circular
        references or objects that are not Serializable of supertype.
    '''
    def serialize(self):
        buffer = {}

        for key, val in self.__dict__.items():
            if isinstance(val, Serializable):
                buffer[key] = val.serialize()
            else:
                buffer[key] = val
        
        return buffer