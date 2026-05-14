# Opens and reads distances.csv file
def load_distance():
    with open("distances.csv", 'r', encoding="utf-8-sig") as file:

        # Creates a dictionary to assign each address an index.
        distance_dict = {}

        # Creates a list of lists to assign distance values to each address index.
        distance_list = []
        index = 0

        # For each row in csv file, parses distance data and creates a list of lists for each address and its distance data.
        for row in file:
            row = row.strip()
            fields = row.split(",")
            address = fields[0]
            distances = [float(d) for d in fields[1:]]
            distance_dict[address] = index
            distance_list.append(distances)
            index += 1

    return distance_dict, distance_list

# Function to determine the distance between 2 addresses.
def get_distance(address1, address2, distance_dict, distance_list):
    i = distance_dict[address1]
    j = distance_dict[address2]

    if i > j:
        # print("The distance between", address1, "and", address2, "is", distance_list[i][j])
        return distance_list[i][j]

    else:
        # print("The distance between", address1, "and", address2, "is", distance_list[j][i])
        return distance_list[j][i]
