# Name: Kyrne Li
# OSU Email: liky@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: Assignment 6 - HashMap
# Due Date: 06/05/2022
# Description: Implementation of HashMap using Dynamic Arrays and HashEntry


from a6_include import (DynamicArray, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()
        for _ in range(capacity):
            self._buckets.append(None)

        self._capacity = capacity
        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Updates a key/value pair in the hash map. If the given key already exists in the map, then it will
        replace the value. If it isn't in the hash map, then it will add the key/value pair. The table will be
        resized to double its capacity if the load factor >= .5.
        """
        # remember, if the load factor is greater than or equal to 0.5,
        # resize the table before putting the new key/value pair

        # checks if table load is under the required threshold of .5, if not double capacity
        if self.table_load() >= .5:
            self.resize_table(self.get_capacity() * 2)

        index = self._hash_function(key) % self.get_capacity()
        spot = self._buckets.get_at_index(index)

        # checks if the key exists in the hash map to replace value
        if self.contains_key(key) is True:
            for i in range(0, self.get_capacity()):
                current = self._buckets.get_at_index(i)
                if current is not None and current.is_tombstone is False and current.key == key:
                    current.value = value
                    return

        # current spot is open for putting at index
        if spot is None:
            self._buckets.set_at_index(index, HashEntry(key, value))
            self._size += 1

        # case for spot being a tombstone
        elif spot is not None and spot.is_tombstone is True:
            spot.key = key
            spot.value = value
            spot.is_tombstone = False
            self._size += 1

        else:
            for i in range(1, self._capacity):
                new_index = (index + (i ** 2)) % self._capacity
                new_spot = self._buckets.get_at_index(new_index)

                # new spot free for putting
                if new_spot is None:
                    self._buckets.set_at_index(new_index, HashEntry(key, value))
                    self._size += 1
                    return

                # case for new spot being a tombstone
                elif new_spot is not None and new_spot.is_tombstone is True:
                    print('2')
                    new_spot.key = key
                    new_spot.value = value
                    self._size += 1
                    new_spot.is_tombstone = False
                    return

    def table_load(self) -> float:
        """
        Returns the current hash table load factor.
        """
        return self.get_size()/self.get_capacity()

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in the hash map.
        """

        count = 0

        for i in range(0, self.get_capacity()):
            current = self._buckets.get_at_index(i)
            if current is None:
                count += 1

        return count

    def resize_table(self, new_capacity: int) -> None:
        """
        Changes the capacity of the internal hash table. All exists key/value pairs will be kept and
        all hash table links will be rehashed. If new_capacity is less than 1, this method does nothing.
        """
        # remember to rehash non-deleted entries into new table

        # check for new capacity to be over 0:
        if new_capacity < 1:
            return

        elif new_capacity < self.get_size():
            return

        new_table = DynamicArray()

        # copy contents from current buckets to new table for rehashing
        for i in range(0, self._capacity):
            new_table.append(self._buckets.get_at_index(i))

        # reset buckets and capacity
        self._buckets = DynamicArray()
        self._capacity = new_capacity
        for i in range(0, self.get_capacity()):
            self._buckets.append(None)
        self._size = 0

        for i in range(0, new_table.length()):
            current = new_table.get_at_index(i)
            if current is not None:
                if current.is_tombstone is False:
                    self.put(current.key, current.value)

    def get(self, key: str) -> object:
        """
        Returns the value associated with the given key, if the key is not in the hash table, then
        it returns None:
        """

        for i in range(0, self.get_capacity()):
            current = self._buckets.get_at_index(i)
            if current is not None and current.is_tombstone is False:
                if current.key == key:
                    return current.value

        return None

    def contains_key(self, key: str) -> bool:
        """
        Returns if the given key is in the hash map. If it doesn't exist, then it will return False.
        An empty hash map does not contain any keys.
        """

        if self.get_size() == 0:
            return False

        for i in range(0, self.get_capacity()):
            current = self._buckets.get_at_index(i)
            if current is not None and current.is_tombstone is False:
                if current.key == key:
                    return True

        return False

    def remove(self, key: str) -> None:
        """
        Removes the given key and its associated value from the hash map. if the key is not in the map,
        then this function does nothing
        """

        for i in range(0, self.get_capacity()):
            current = self._buckets.get_at_index(i)
            if current is not None and current.is_tombstone is False:
                if current.key == key:
                    current.is_tombstone = True
                    self._size -= 1
                    return None

        return None

    def clear(self) -> None:
        """
        Clears the current contents of the hash map, it will not change the underlying hash table
        capacity.
        """

        self._size = 0
        for i in range(0, self.get_capacity()):
            self._buckets.set_at_index(i, None)

    def get_keys(self) -> DynamicArray:
        """
        Returns a dynamic array containing all the keys in the hash map.
        """

        keys_array = DynamicArray()

        for i in range(0, self.get_capacity()):
            current = self._buckets.get_at_index(i)
            if current is not None:
                if current.is_tombstone is False:
                    keys_array.append(current.key)

        return keys_array


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    # print("\nPDF - put example 1")
    # print("-------------------")
    # m = HashMap(50, hash_function_1)
    # for i in range(150):
    #     m.put('str' + str(i), i * 100)
    #     if i % 25 == 24:
    #         print(m.empty_buckets(), m.table_load(), m.get_size(), m.get_capacity())
    #
    # print("\nPDF - put example 2")
    # print("-------------------")
    # m = HashMap(40, hash_function_2)
    # for i in range(50):
    #     m.put('str' + str(i // 3), i * 100)
    #     if i % 10 == 9:
    #         print(m.empty_buckets(), m.table_load(), m.get_size(), m.get_capacity())
    #
    # print("\nPDF - table_load example 1")
    # print("--------------------------")
    # m = HashMap(100, hash_function_1)
    # print(m.table_load())
    # m.put('key1', 10)
    # print(m.table_load())
    # m.put('key2', 20)
    # print(m.table_load())
    # m.put('key1', 30)
    # print(m.table_load())
    #
    # print("\nPDF - table_load example 2")
    # print("--------------------------")
    # m = HashMap(50, hash_function_1)
    # for i in range(50):
    #     m.put('key' + str(i), i * 100)
    #     if i % 10 == 0:
    #         print(m.table_load(), m.get_size(), m.get_capacity())
    #
    # print("\nPDF - empty_buckets example 1")
    # print("-----------------------------")
    # m = HashMap(100, hash_function_1)
    # print(m.empty_buckets(), m.get_size(), m.get_capacity())
    # m.put('key1', 10)
    # print(m.empty_buckets(), m.get_size(), m.get_capacity())
    # m.put('key2', 20)
    # print(m.empty_buckets(), m.get_size(), m.get_capacity())
    # m.put('key1', 30)
    # print(m.empty_buckets(), m.get_size(), m.get_capacity())
    # m.put('key4', 40)
    # print(m.empty_buckets(), m.get_size(), m.get_capacity())
    #
    # print("\nPDF - empty_buckets example 2")
    # print("-----------------------------")
    # m = HashMap(50, hash_function_1)
    # for i in range(150):
    #     m.put('key' + str(i), i * 100)
    #     if i % 30 == 0:
    #         print(m.empty_buckets(), m.get_size(), m.get_capacity())
    #
    # print("\nPDF - resize example 1")
    # print("----------------------")
    # m = HashMap(20, hash_function_1)
    # m.put('key1', 10)
    # print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    # m.resize_table(30)
    # print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    #
    # print("\nPDF - resize example 2")
    # print("----------------------")
    # m = HashMap(75, hash_function_2)
    # keys = [i for i in range(1, 1000, 13)]
    # for key in keys:
    #     m.put(str(key), key * 42)
    # print(m.get_size(), m.get_capacity())
    #
    # for capacity in range(111, 1000, 117):
    #     m.resize_table(capacity)
    #
    #     if m.table_load() >= 0.5:
    #         print("Check that capacity gets updated during resize(); "
    #               "don't wait until the next put()")
    #
    #     m.put('some key', 'some value')
    #     result = m.contains_key('some key')
    #     m.remove('some key')
    #
    #     for key in keys:
    #         # all inserted keys must be present
    #         result &= m.contains_key(str(key))
    #         # NOT inserted keys must be absent
    #         result &= not m.contains_key(str(key + 1))
    #     print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))
    #
    # print("\nPDF - get example 1")
    # print("-------------------")
    # m = HashMap(30, hash_function_1)
    # print(m.get('key'))
    # m.put('key1', 10)
    # print(m.get('key1'))
    #
    # print("\nPDF - get example 2")
    # print("-------------------")
    # m = HashMap(150, hash_function_2)
    # for i in range(200, 300, 7):
    #     m.put(str(i), i * 10)
    # print(m.get_size(), m.get_capacity())
    # for i in range(200, 300, 21):
    #     print(i, m.get(str(i)), m.get(str(i)) == i * 10)
    #     print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)
    #
    # print("\nPDF - contains_key example 1")
    # print("----------------------------")
    # m = HashMap(10, hash_function_1)
    # print(m.contains_key('key1'))
    # m.put('key1', 10)
    # m.put('key2', 20)
    # m.put('key3', 30)
    # print(m.contains_key('key1'))
    # print(m.contains_key('key4'))
    # print(m.contains_key('key2'))
    # print(m.contains_key('key3'))
    # m.remove('key3')
    # print(m.contains_key('key3'))
    #
    # print("\nPDF - contains_key example 2")
    # print("----------------------------")
    # m = HashMap(75, hash_function_2)
    # keys = [i for i in range(1, 1000, 20)]
    # for key in keys:
    #     m.put(str(key), key * 42)
    # print(m.get_size(), m.get_capacity())
    # result = True
    # for key in keys:
    #     # all inserted keys must be present
    #     result &= m.contains_key(str(key))
    #     # NOT inserted keys must be absent
    #     result &= not m.contains_key(str(key + 1))
    # print(result)
    #
    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(50, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')
    #
    # print("\nPDF - clear example 1")
    # print("---------------------")
    # m = HashMap(100, hash_function_1)
    # print(m.get_size(), m.get_capacity())
    # m.put('key1', 10)
    # m.put('key2', 20)
    # m.put('key1', 30)
    # print(m.get_size(), m.get_capacity())
    # m.clear()
    # print(m.get_size(), m.get_capacity())
    #
    # print("\nPDF - clear example 2")
    # print("---------------------")
    # m = HashMap(50, hash_function_1)
    # print(m.get_size(), m.get_capacity())
    # m.put('key1', 10)
    # print(m.get_size(), m.get_capacity())
    # m.put('key2', 20)
    # print(m.get_size(), m.get_capacity())
    # m.resize_table(100)
    # print(m.get_size(), m.get_capacity())
    # m.clear()
    # print(m.get_size(), m.get_capacity())
    #
    # print("\nPDF - get_keys example 1")
    # print("------------------------")
    # m = HashMap(10, hash_function_2)
    # for i in range(100, 200, 10):
    #     m.put(str(i), str(i * 10))
    # print(m.get_keys())
    #
    # m.resize_table(1)
    # print(m.get_keys())
    #
    # m.put('200', '2000')
    # m.remove('100')
    # m.resize_table(2)
    # print(m.get_keys())
