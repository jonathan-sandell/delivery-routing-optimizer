class HashTable:
    def __init__(self, size=10):
        self.size = size
        self.table = []
        for i in range(size):
            self.table.append([])

    # Inserts a package to the hash table.
    def insert(self, package):
        key = package.package_id
        index = key % self.size
        bucket = self.table[index]
        bucket.append(package)

    # Shows a package object from given ID.
    def lookup(self, package_id):
        index = package_id % self.size
        bucket = self.table[index]
        for package in bucket:
            if package.package_id == package_id:
                return package
        return None

    def __str__(self):
        # Prints full hash table in easy to read format.
        hash_string = ''
        for i, bucket in enumerate(self.table):
            # hash_string += "\n"
            hash_string += f"Bucket {i}\n"
            # hash_string += "- - - - - \n"
            for package in bucket:
                hash_string += "   "
                hash_string += str(package)
                hash_string += '\n'
        return hash_string

