# Name: Kyrne Li
# OSU Email: liky@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: Assignment 6 - HashMap
# Due Date: 06/05/2022
# Description: Implementation of HashMap using Dynamic Arrays and Linked Lists


from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()
        for _ in range(capacity):
            self._buckets.append(LinkedList())

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
        Updates a key/value pair in the hash map. If the key already exists, then the existing
        values will be overwritten with the new one. If the key doesn't exist, then the key/value pair
        will be added.
        """

        # calculates index and gets the slot in the buckets
        # slots is the LinkedList
        index = self._hash_function(key) % self.get_capacity()
        slot = self._buckets.get_at_index(index)

        # checks if SLL contains the node, if it returns None, then insert and increment size
        # otherwise assumes node exists and edits
        if slot.contains(key) is None:
            slot.insert(key, value)
            self._size += 1
        else:
            slot.contains(key).value = value

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in the hash table.
        """

        count = 0
        for i in range(0, self.get_capacity()):
            if self._buckets.get_at_index(i).length() == 0:
                count += 1

        return count

    def table_load(self) -> float:
        """
        Returns the current hash table load factor.
        """

        return self.get_size()/self.get_capacity()

    def clear(self) -> None:
        """
        Clears the contents of the hash map, it will not change the underlying hash table capacity.
        """

        self._buckets = DynamicArray()
        self._size = 0
        for i in range(0, self.get_capacity()):
            self._buckets.append(LinkedList())

    def resize_table(self, new_capacity: int) -> None:
        """
        Changes the capacity of the internal hash table. All exists key/value pairs will be kept and
        all hash table links will be rehashed. If new_capacity is less than 1, this method does nothing.
        """

        # checks for new capacity to be > 1
        if new_capacity < 1:
            return

        # creates a new table and adds empty linked lists
        new_table = DynamicArray()

        # makes a new table to hold current key/value pairs
        for i in range(0, self._capacity):
            current = self._buckets.get_at_index(i)
            for j in current:
                new_table.append(j)

        # new information for underlying storage/capacity
        self._buckets = DynamicArray()
        self._capacity = new_capacity
        for i in range(0, self.get_capacity()):
            self._buckets.append(LinkedList())
        self._size = 0

        # rehash all the links
        for i in range(0, new_table.length()):
            current = new_table.get_at_index(i)
            self.put(current.key, current.value)

    def get(self, key: str) -> object:
        """
        Returns the value associated with the given key, returns None is key is not in the hash table.
        """

        for i in range(0, self.get_capacity()):
            slot = self._buckets.get_at_index(i)
            if slot.contains(key) is not None:
                return slot.contains(key).value

        return None

    def contains_key(self, key: str) -> bool:
        """
        Returns true if the key is in the hash map, otherwise returns False. An empty hash does not contain
        keys.
        """

        for i in range(0, self.get_capacity()):
            if self._buckets.get_at_index(i).contains(key):
                return True

        return False

    def remove(self, key: str) -> None:
        """
        Removes the given key and its associated values from the hash map. If the key does not exist,
        this method does nothing.
        """

        for i in range(0, self.get_capacity()):
            slot = self._buckets.get_at_index(i)
            if slot.contains(key) is not None:
                self._size -= 1
                slot.remove(key)

    def get_keys(self) -> DynamicArray:
        """
        Returns a dynamic array containing all keys in stored in the hash map. There is no specific ordering
        of the keys in the returned array.
        """

        return_array = DynamicArray()

        for i in range(0, self._capacity):
            current = self._buckets.get_at_index(i)
            for j in current:
                return_array.append(j.key)

        return return_array


def find_mode(da: DynamicArray) -> (DynamicArray, int):
    """
    Takes a dynamic array and returns a tuple containing the mode and mode frequency of the value(s) of
    the array. If there is more than one value with the highest frequency, then all of those values will be
    returned. If there is only one more, it will only return an array with that value.
    """
    # if you'd like to use a hash map,
    # use this instance of your Separate Chaining HashMap

    map = HashMap(da.length() // 3, hash_function_1)

    # case if there's only one element
    if da.length() == 1:
        return_array = DynamicArray()
        return_array.append(da.get_at_index(0))
        return return_array, 1

    # creates a hash map of the given array
    for i in range(0, da.length()):
        map.put(da.get_at_index(i), da.get_at_index(i))

    # initializes the array and info for holding mode data
    mode_array = DynamicArray()
    mode_array.append(da.get_at_index(0))

    mode_word = da.get_at_index(0)
    mode_count = 1
    temp_mode = None
    temp_count = 0

    # iterates through the hash map for keys
    for i in range(1, da.length()):
        current = map.get(da.get_at_index(i))

        # current iteration is equal to the current mode
        if current == mode_word:
            mode_count += 1

        elif current == temp_mode:
            temp_count += 1

        else:
            # temp_count is same, add to array
            if temp_count == mode_count:
                mode_array.append(temp_mode)
                temp_mode = current
                temp_count = 1

            # makes a new array and adds temp into it
            elif temp_count > mode_count:
                mode_word = temp_mode
                mode_count = temp_count
                mode_array = DynamicArray()
                mode_array.append(mode_word)
                temp_mode = current
                temp_count = 1

            # reset temp array
            else:
                temp_mode = current
                temp_count = 1

    if temp_count > mode_count:
        temp_array = DynamicArray()
        temp_array.append(temp_mode)
        return temp_array, temp_count
    elif temp_count == mode_count:
        mode_array.append(temp_mode)

    return mode_array, mode_count


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
    # #
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
    # print("\nPDF - resize example 1")
    # print("----------------------")
    # m = HashMap(20, hash_function_1)
    # m.put('key1', 10)
    # print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    # m.resize_table(30)
    # print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    #
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
    # #
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
    # print("\nPDF - remove example 1")
    # print("----------------------")
    # m = HashMap(50, hash_function_1)
    # print(m.get('key1'))
    # m.put('key1', 10)
    # print(m.get('key1'))
    # m.remove('key1')
    # print(m.get('key1'))
    # m.remove('key4')
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

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "melon", "peach"])
    map = HashMap(da.length() // 3, hash_function_1)
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode: {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        map = HashMap(da.length() // 3, hash_function_2)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode: {mode}, Frequency: {frequency}\n")
