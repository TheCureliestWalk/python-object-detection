name = ["Iho", "Pui", "Keq", "Raph"]
gpx = [3.8, 3.7, 2.0, 2.3]
# x = range(len(name))

# print(x)

# ----------------
# Class with no default values

# class Person:
#     def __init__(self, name, gpx):
#         self.name = name
#         self.gpx = gpx

#         def check_good(self):
#             if self.gpx >= 3.5:
#                 self.is_good = True
#         check_good(self) #must have 'self'
# p1 = Person("Iho", 3.8)
# print(p1.name, p1.gpx, p1.is_good)

# ----------------

# ----------------
# Class with default values
class Person:
    def __init__(self, name="none", gpx=0, is_good = False):
         self.name = name
         self.gpx = gpx
         self.is_good = is_good
         
         if self.gpx >= 3.5:
             self.is_good = True
    
    def __repr__(self):
        return f'Name: {self.name} GPX:{self.gpx} Is_Good: {self.is_good}'
    
# quickly create new object
p1 = Person("Iho", 3.8)

# slowly ver. but in class declaration, it need to have default values
p2 = Person()
p2.name = "Keq"
p2.gpx = 3.0

print(p2)
print(p1)   

print(p2.__dict__)   # export as dict
# ----------------


# ----------------
# class AutoPerson:
#     def __init__(self, name = "No Name", age = 0):
#         self.name = name
#         self.age = age
        
        
# ap1 = AutoPerson()
# print(ap1.name, ap1.age)
# ----------------
        
