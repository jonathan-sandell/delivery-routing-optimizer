from datetime import datetime, time

class Truck:
    def __init__(self, truck_number, packages, mileage = 0, speed = 18, current_time = datetime.combine(datetime.today().date(), time(8, 0)), current_address = "4001 South 700 East"):
        self.truck_number = truck_number
        self.speed = speed
        self.mileage = mileage
        self.current_time = current_time
        self.current_address = current_address
        self.packages = packages

    def __str__(self):
        string = []
        for package in self.packages:
            string.append(str(package))
        return "\n".join(string)

    def __repr__(self):
        return self.__str__()