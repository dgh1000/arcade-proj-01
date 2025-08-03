from util import *

class Car:
    def __init__(self, mpg):
        self.mpg = mpg

    def gallons_per_mile(self):
        return 1.0/self.mpg

    def __str__(self):
        return f"miles per gallon: {self.mpg}"
    
class Honda(Car):
    def __init__(self, mpg, logo_color):
        super().__init__(mpg)
        self.logo_color = logo_color

    def __str__(self):
        return f"mpg: {self.mpg}, logo_color: {self.logo_color}"

def main():
    v1 = Vector(0, 0)
    v2 = Vector(3, 4)
    v3 = v1-v2
    print(v3)
    # car1 = Car(50)
    # # is car2 an instance of Car? yes
    # car2 = Honda(25, "red")
    # print(car2.gallons_per_mile())

    # dog : class of all dogs
    # Poodle: sub class of dogs. only some dogs
    #   are Poodles
    # Nikki: instance of the class of Poodles

    # car has the feature mpg. all cars have this feature
    # Honda: customizable logo color. not all cars have that
    # and it has miles per gallon

    # print(v2.normalize())
    

main()