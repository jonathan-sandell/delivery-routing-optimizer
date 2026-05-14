class Package:
    def __init__(self, package_id, address, city, state, zip_code, deadline, weight, notes, status = "AT THE HUB", loading_time = None, delivery_time = None, query_status = None, query_delivery_time = None, truck_num = None):
        self.package_id = package_id
        self.truck_num = truck_num
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.deadline = deadline
        self.weight = weight
        self.notes = notes
        self.status = status
        self.loading_time = loading_time
        self.delivery_time = delivery_time
        self.query_status = query_status
        self.query_delivery_time = query_delivery_time


    def __str__(self):
        return (f'ID: {self.package_id} ||'
                f' Address: {self.address} ||'
                f' Deadline: {self.deadline} ||'
                f' City: {self.city} ||'
                f' Zip: {self.zip_code} ||'
                f' Weight: {self.weight} ||'
                f' Status: {self.status} ||'
                f' Delivered on: {self.delivery_time}'
                )

    def __repr__(self):
        return self.__str__()