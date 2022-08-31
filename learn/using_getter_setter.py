class Person:
    def __init__(self, name="none", gpx=0):
         self.name = name
         self.gpx = gpx
         self.is_good = False
        
    # @property
    # def is_good(self):
    #     return self.is_good
    
    # @is_good.setter
    # def is_good(self, gpx):
    #     if self.gpx:
    #         self.is_good = True
    #     self.is_good = False
    
    def __repr__(self):
        return f'Name: {self.name} GPX:{self.gpx} Is_Good: {self.is_good}'
    

p1 = Person("Iho", 3.8)
print(p1)