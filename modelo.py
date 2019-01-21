class Vehicle(object):   
"""Represent a vehicle."""
    DEFAULTS = {'wheels':4, 'doors':2, 'fuel':'gasoline', 'passengers':2}

    def __init__(self, **kwargs):
       kwargs.update(self.DEFAULTS)
       self.info = kwargs 

    def drive(self):
       print "Vroom"


class Sedan(Vehicle):
    DEFAULTS = {'wheels':4, 'doors':4, 'fuel':'gasoline', 'passengers':5}

def Hybrid(Sedan):
    DEFAULTS = {'wheels':4, 'doors':4, 'fuel':'smug', 'passengers':4}

    def drive(self):
        print "purrrrrr..."

class Van(Vehicle):
    DEFAULTS = {'wheels':4, 'doors':3, 'fuel':'gasoline', 'passengers':2, 'cargo':[]}

    def unload(self):
       if not self.cargo:
          print "no cargo loaded"
       else:
          print "unloading"
       return self.cargo