from hash_table import HashTable
from package import Package

# Opens and reads packages.csv file
def load_packages():
    with open("packages.csv", 'r', encoding="utf-8-sig") as file:

        # Creates a new hash table.
        hash_table = HashTable()

        # Skips the header line.
        next(file)

        # For each row in csv file, parses package data and instantiates a new package object to add to hash table.
        for row in file:
            row = row.strip()
            fields = row.split(',')
            if len(fields) > 8:
                notes = ','.join(fields[7:]).replace('"', '')
                fields = fields[:7] + [notes]
            package = Package(int(fields[0]), fields[1], fields[2], fields[3], fields[4], fields[5], int(fields[6]), fields[7])
            hash_table.insert(package)

    return hash_table