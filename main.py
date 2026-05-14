from distance_import import load_distance, get_distance
from package_import import load_packages
from truck import Truck
from datetime import datetime, time, timedelta


# Delivery routing algorithm
def routing_algorithm(truck):
    while len(truck.packages) > 0:

        minimum = None
        nearest_address = None
        current_package = None

        # For Truck 3, prioritize packages 6 and 25 because they have deadlines and were delayed.
        if truck.truck_number == 3 and any(pkg.package_id in (6, 25) for pkg in truck.packages):
            priority_list = [pkg for pkg in truck.packages if pkg.package_id in (6,25)]
            candidates = priority_list

        else:
            candidates = truck.packages
        for pkg in candidates:

            pkg.truck_num = truck.truck_number

            # If time is before 10:20 am, skip package 9 because it has wrong address
            # and will be corrected at 10:20 am.
            if truck.truck_number == 3:
                if pkg.package_id == 9:
                    if truck.current_time < datetime.combine(datetime.today().date(), time(10, 20)):
                        continue
                    else:
                        pkg.address = "410 S State St"
                        pkg.zip_code = "84111"

            # Determines next nearest address after comparing all package addresses to current truck address
            distance = get_distance(truck.current_address, pkg.address, distance_dict, distance_list)
            if minimum is None or distance < minimum:
                minimum = distance
                nearest_address = pkg.address
                current_package = pkg
        truck.current_address = nearest_address
        truck.mileage += minimum
        minutes_passed = (minimum / truck.speed) * 60
        truck.current_time += timedelta(minutes=minutes_passed)
        current_package.status = "DELIVERED"
        current_package.delivery_time = truck.current_time
        truck.packages.remove(current_package)

        # When truck has delivered all packages, return truck to hub.
        if len(truck.packages) == 0:
            hub_distance = get_distance(truck.current_address, "4001 South 700 East", distance_dict, distance_list)
            truck.mileage += hub_distance
            truck.current_address = "4001 South 700 East"
            minutes_passed = (hub_distance / truck.speed) * 60
            truck.current_time += timedelta(minutes=minutes_passed)

# Loads all packages into the hash table.
hash_table = load_packages()

distance_dict, distance_list = load_distance()

# Creates package list for each truck.
truck1_packages = []
truck2_packages = []
truck3_packages = []

# Assigns packages to Truck 1 if they have a deadline and are not delayed.
for i in range(1, 41):
    package = hash_table.lookup(i)
    if package.deadline != "EOD" and package.notes != "Delayed on flight---will not arrive to depot until 9:05 am":
        truck1_packages.append(package)

# Package 19 must be with specific packages that are on Truck 1.
truck1_packages.append(hash_table.lookup(19))

# Assigns packages that are required to be on Truck 2.
for i in range(1, 41):
    package = hash_table.lookup(i)
    if package.notes == "Can only be on truck 2":
        truck2_packages.append(package)

# Assigns delayed packages to Truck 3.
for i in range(1, 41):
    package = hash_table.lookup(i)
    if package.notes == "Delayed on flight---will not arrive to depot until 9:05 am":
        package.status = "DELAYED"
        truck3_packages.append(package)

# Assigns remaining packages to Truck 2 and Truck 3.
# Truck 1 will only deliver its originally assigned packages.
truck2_packages.append(hash_table.lookup(2))
truck2_packages.append(hash_table.lookup(4))
truck2_packages.append(hash_table.lookup(5))
truck2_packages.append(hash_table.lookup(7))
truck2_packages.append(hash_table.lookup(8))
truck2_packages.append(hash_table.lookup(10))
truck2_packages.append(hash_table.lookup(11))
truck2_packages.append(hash_table.lookup(12))
truck2_packages.append(hash_table.lookup(17))
truck2_packages.append(hash_table.lookup(21))
truck2_packages.append(hash_table.lookup(22))

truck3_packages.append(hash_table.lookup(9))
truck3_packages.append(hash_table.lookup(23))
truck3_packages.append(hash_table.lookup(24))
truck3_packages.append(hash_table.lookup(26))
truck3_packages.append(hash_table.lookup(27))
truck3_packages.append(hash_table.lookup(33))
truck3_packages.append(hash_table.lookup(35))
truck3_packages.append(hash_table.lookup(39))

# Creates truck objects with assigned packages.
truck1 = Truck(packages=truck1_packages, truck_number=1)
for package in truck1_packages:
    package.loading_time = truck1.current_time
    package.status = "EN ROUTE"
truck2 = Truck(packages=truck2_packages, truck_number=2)
for package in truck2_packages:
    package.loading_time = truck2.current_time
    package.status = "EN ROUTE"
truck3 = Truck(packages=truck3_packages, truck_number=3)

# Runs the delivery simulation in sequence.
# Truck 1 and Truck 2 deliver first since there are 2 drivers available.
# Once a driver returns and time is at least 9:05 am (accounting for delayed package), Truck 3 is loaded and dispatched.
routing_algorithm(truck1)
routing_algorithm(truck2)

# Check to determine whether Truck 1 or 2 returns to hub first so Truck 3 can be loaded and dispatched.
# Cannot load Truck 3 before 9:05 due to delayed package.
truck3_earliest_load_time = datetime.combine(datetime.today().date(), time(9, 5))
first_return_time = min(truck1.current_time, truck2.current_time)

# Sets the current time for Truck 3 based on Truck 1/Truck 2 return time.
truck3.current_time = max(first_return_time, truck3_earliest_load_time)
for package in truck3_packages:
    package.loading_time = truck3.current_time
    package.status = "EN ROUTE"
routing_algorithm(truck3)

# Final status after all packages have been delivered.
print(hash_table)

# User interface
while True:
    # User choices
    choice = input("Enter \"status\" to display package status\nEnter \"miles\" to display total mileage for all trucks\nPress \"q\" to exit\n")

    if choice == "status":
        while True:
            user_time = input("Enter a time: (HH:MM AM/PM)\n")
            try:
                user_time = datetime.strptime(user_time, "%I:%M %p").time()
                user_time = datetime.combine(datetime.today().date(), user_time)
                print(f'WGUPS Package Status at {user_time.strftime("%I:%M %p")}\n'
                      f'-----------------------------------')

                # Generates package info for each package based on user input time.
                for i in range(1, 41):
                    user_pkg = hash_table.lookup(i)
                    query_address = user_pkg.address
                    query_zip = user_pkg.zip_code

                    # Shows wrong address if time is before 10:20 am.
                    # Shows corrected address after 10:20 am.
                    if user_pkg.package_id == 9:
                        if user_time < datetime.combine(datetime.today().date(), time(10, 20)):
                            query_address = "300 State St"
                            query_zip = "84103"

                    # Shows status for delayed packages depending on user input time.
                    if user_pkg.notes == "Delayed on flight---will not arrive to depot until 9:05 am":
                        if user_time < truck3_earliest_load_time:
                            user_pkg.query_status = "DELAYED"
                        elif user_time >= user_pkg.delivery_time:
                            user_pkg.query_status = "DELIVERED"
                            user_pkg.query_delivery_time = user_pkg.delivery_time
                        else:
                            user_pkg.query_status = "EN ROUTE"

                    # Shows status for all other packages depending on user input time.
                    elif user_time < user_pkg.loading_time:
                        user_pkg.query_status = "AT THE HUB"
                    elif user_time >= user_pkg.delivery_time:
                        user_pkg.query_status = "DELIVERED"
                        user_pkg.query_delivery_time = user_pkg.delivery_time
                    else:
                        user_pkg.query_status = "EN ROUTE"

                    if user_pkg.query_delivery_time is not None:
                        delivery_time = user_pkg.query_delivery_time
                        delivery_time = delivery_time.strftime("%I:%M:%S %p")
                    else:
                        delivery_time = None

                    # Formatting for delivered packages
                    if delivery_time is not None:
                        print(f'ID: {user_pkg.package_id} || Truck Number: {user_pkg.truck_num} || Address: {query_address} || Deadline: {user_pkg.deadline} || City: {user_pkg.city} || Zip: {query_zip} || Weight: {user_pkg.weight} || Status: {user_pkg.query_status} || Delivered on: {delivery_time}\n')

                    # Formatting for undelivered packages
                    else:
                        print(f'ID: {user_pkg.package_id} || Truck Number: {user_pkg.truck_num} || Address: {query_address} || Deadline: {user_pkg.deadline} || City: {user_pkg.city} || Zip: {query_zip} || Weight: {user_pkg.weight} || Status: {user_pkg.query_status}\n')

                break
            # Prompts user to try again if invalid time value is input.
            except ValueError:
                print(f'Not a valid time value. Try again!')

    elif choice == "miles":
        print(f'Total mileage for all trucks: {truck1.mileage + truck2.mileage + truck3.mileage}\n')


    elif choice == 'q':
        break
    # Prompts user to try again if invalid choice option is input
    else:
        print(f'Invalid choice. Try again!')