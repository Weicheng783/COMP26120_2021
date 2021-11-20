from enum import Enum
import config
import math

class hashset:
    def isPrime(self, n):
        i = 2
        while (i * i < n):
            if (n % i == 0):
                return False
            i = i + 1
        return True

    # Helper function for finding the next prime number of n
    # Return n if n is already prime
    def nextPrime(self, n):
        while (not self.isPrime(n)):
            n = n + 1
        return n

    # Helper function for finding the last prime number of n
    def previousPrime(self, n):
        n = n - 1
        while (not self.isPrime(n)):
            n = n - 1
        return n

    def __init__(self):
        # Create initial hash table
        # Initialise variables: Collisions, load factor, hash array.
        self.verbose = config.verbose
        self.mode = config.mode
        self.hash_table_size = config.init_size
        self.collisions = 0
        self.total_obj = 0
        self.load_factor = 0.0

        # self.hasharray = [None]*7
        # self.hash_table_size = 7
        # Different Data Structures for Open Addr. and Separate Chaining.
        if(self.mode == HashingModes.HASH_1_SEPARATE_CHAINING.value or self.mode == HashingModes.HASH_2_SEPARATE_CHAINING.value):
            self.hasharray = [[None]]*self.hash_table_size
        else:
            self.hasharray = [None]*self.hash_table_size

        # For the double hashing, we select the value that is the prime just below the size of it.
        self.double_hashing_value = self.previousPrime(self.hash_table_size)

    def insert(self, value):
        # Code for inserting into hash table
        # Check first if the input is String or Int
        if(isinstance(value,int) == False):
            initial_value = value
            value = 0
            for i in range(len(initial_value)):
                if(self.mode <= 3):
                    # The First Hash Function
                    transit = ord(initial_value[i])*((31)**(len(initial_value)-1-i))
                else:
                    # The Second Hash Function
                    transit = ord(initial_value[i])*(3**i)
                value += transit

        # Flag meanings for 0: Normal insert; 1: Found duplicates; 2: Rehashing needed.
        flag = 0
        # Threshold 0.6 for open addressing, 0.8 for separate chaining.
        if(self.load_factor >= 0.6 and (self.mode != HashingModes.HASH_1_SEPARATE_CHAINING.value and self.mode != HashingModes.HASH_2_SEPARATE_CHAINING.value)):
            flag = 2
        elif(self.load_factor >= 0.8 and (self.mode == HashingModes.HASH_1_SEPARATE_CHAINING.value or self.mode == HashingModes.HASH_2_SEPARATE_CHAINING.value)):
            flag = 2
        if(flag != 2):
            # Separate Chaining and Open Addressing follow different routes.
            # True for OA, False for SC.
            if(self.mode != HashingModes.HASH_1_SEPARATE_CHAINING.value and self.mode != HashingModes.HASH_2_SEPARATE_CHAINING.value):
                # Detect if a place has been occupied.
                if(self.hasharray[value%self.hash_table_size] == None):
                    if(self.load_factor >= 0.6):
                        flag = 2
                    else:
                        self.hasharray[value%self.hash_table_size] = value
                        self.total_obj += 1
                        self.load_factor = self.total_obj/len(self.hasharray)
                else:
                    # Do the reallocation, this means we encountered a collision.
                    collisions = 0
                    index = value%self.hash_table_size

                    # This value is used in Quadratic Probing & Double Hashing
                    loop_quadratic = 1

                    # Looping to find a suitable blank to put the value in.
                    while(self.hasharray[index] != None):
                        if(self.load_factor >= 0.6):
                            # Flag it to rehashing.
                            flag = 2
                            break
                        if(self.hasharray[index] == value):
                            # Duplicates detected, we drop it and not add to the array.
                            collisions = 0
                            flag = 1
                            break
                        # Case Distinction for linear_probing, quadratic_probing, double_hashing.          
                        if(self.mode == HashingModes.HASH_1_LINEAR_PROBING.value or self.mode == HashingModes.HASH_2_LINEAR_PROBING.value):
                            collisions += 1
                            if(index == self.hash_table_size-1):
                                index = 0
                            else:
                                index += 1
                            if(index == value%self.hash_table_size):
                                # No more space, rehashing needed, this is a special case.
                                flag = 2
                                break

                        elif(self.mode == HashingModes.HASH_1_QUADRATIC_PROBING.value or self.mode == HashingModes.HASH_2_QUADRATIC_PROBING.value):
                            collisions += 1
                            if(index+((loop_quadratic)**2) >= self.hash_table_size-1):
                                index = (index+((loop_quadratic)**2)) % self.hash_table_size
                            else:
                                index += ((loop_quadratic)**2)
                            loop_quadratic += 1

                        elif(self.mode == HashingModes.HASH_1_DOUBLE_HASHING.value or self.mode == HashingModes.HASH_2_DOUBLE_HASHING.value):

                            if( self.hasharray[(index+loop_quadratic*(value%self.double_hashing_value))%self.hash_table_size] != None):
                                collisions += 1
                                loop_quadratic += 1
                            else:
                                self.hasharray[(index+loop_quadratic*(value%self.double_hashing_value))%self.hash_table_size] = value
                                break

                    if(flag != 1 and flag != 2 and (self.mode != HashingModes.HASH_1_DOUBLE_HASHING.value and self.mode != HashingModes.HASH_2_DOUBLE_HASHING.value)):
                        # We confirm the reallocation and update the array when it finds a place to put the value in.
                        self.hasharray[index] = value
                        self.total_obj += 1
                        self.load_factor = self.total_obj/len(self.hasharray)
                    # Summing up the total collisions occurred, keep it up to date.
                    self.collisions += collisions
            else:
                # Case for Separate Chaining -- insert -- empty
                if(self.hasharray[value%self.hash_table_size] == None):
                    self.hasharray[value%self.hash_table_size] = [value]
                    self.total_obj += 1
                    self.load_factor = self.total_obj/self.hash_table_size
                else:
                    # For Separate Chaining -- insert -- space occupied
                    for i in range(len(self.hasharray[value%self.hash_table_size])):
                        # Reject this value as it is a replicate
                        if(value == self.hasharray[value%self.hash_table_size][i]):
                            break
                        elif(i == len(self.hasharray[value%self.hash_table_size])-1):
                            # Else we append this value to the relevant key array.
                            self.hasharray[value%self.hash_table_size].append(value)
                            self.collisions += len(self.hasharray[value%self.hash_table_size])
                            self.total_obj += 1
                            self.load_factor = self.total_obj/self.hash_table_size
                            break
        if(flag == 2):
            # Rehashing Code Snippet
            # We initialise all variables for rehashing, except collisions.
            flag = 0
            self.hash_table_size = self.nextPrime(2*(math.ceil(self.hash_table_size*1.5)))
            self.total_obj = 0
            self.load_factor = 0.0
            array_cpy = self.hasharray
            # The way to rehashing a value for Separate Chaining and Open Addressing are different.
            if(self.mode == HashingModes.HASH_1_SEPARATE_CHAINING.value or self.mode == HashingModes.HASH_2_SEPARATE_CHAINING.value):
                self.hasharray = [None]*self.hash_table_size
                for i in range(len(array_cpy)):
                    if(array_cpy[i] != None):
                        for j in range(len(array_cpy[i])):
                            if(array_cpy[i][j] != None):
                                self.insert(array_cpy[i][j])

                self.insert(value)
            else:
                self.hasharray = [None]*self.hash_table_size
                for i in array_cpy:
                    if(i != None):
                        self.insert(i)
                self.insert(value)

    def find(self, value):
        # Code for looking up in hash table
        if(isinstance(value,int) == False):
            initial_value = value
            value = 0
            for i in range(len(initial_value)):
                if(self.mode <= 3):
                    # The First Hash Function
                    transit = ord(initial_value[i])*((31)**(len(initial_value)-1-i))
                else:
                    # The Second Hash Function
                    transit = ord(initial_value[i])*(3**i)
                value += transit

        index = value%self.hash_table_size

        # Distinguish Separate Chaining or Quadratic Probing.
        if(self.mode != HashingModes.HASH_1_SEPARATE_CHAINING.value and self.mode != HashingModes.HASH_2_SEPARATE_CHAINING.value):
            loop_quadratic = 1
            while(self.hasharray[index] != value):
                # Open Addressing cases: linear_probing, quaratic_probing and double_hashing.
                if(self.mode == HashingModes.HASH_1_LINEAR_PROBING.value or self.mode == HashingModes.HASH_2_LINEAR_PROBING.value):
                    if(index == self.hash_table_size-1):
                        index = 0
                    else:
                        index += 1
                    if(index == value%self.hash_table_size):
                        # Not Found
                        return False
                elif(self.mode == HashingModes.HASH_1_QUADRATIC_PROBING.value or self.mode == HashingModes.HASH_2_QUADRATIC_PROBING.value):
                    if(index+((loop_quadratic)**2) >= self.hash_table_size-1):
                        index = (index+((loop_quadratic)**2)) % self.hash_table_size
                    else:
                        index += ((loop_quadratic)**2)
                    if(loop_quadratic == self.hash_table_size):
                        return False
                    loop_quadratic += 1
                elif(self.mode == HashingModes.HASH_1_DOUBLE_HASHING.value or self.mode == HashingModes.HASH_2_DOUBLE_HASHING.value):
                    if(self.hasharray[(index+loop_quadratic*(value%self.double_hashing_value))%self.hash_table_size] != value):
                        if(loop_quadratic == self.hash_table_size):
                            return False
                        loop_quadratic += 1
                    else:
                        return True

            return True
        else:
            # Separate Chaining -- Searching
            if(self.hasharray[index] == None):
                return False
            else:
                for i in range(len(self.hasharray[index])):
                    if(value == self.hasharray[index][i]):
                        return True
                return False
    def print_set(self):
        # Code for printing hash table
        print(self.hasharray)
    def print_stats(self):
        # Code for printing statistics
        print("Total Objects in the Hash Set: ", self.total_obj)
        if(self.mode != 3 and self.mode != 7):
            print("Hash Set Capacity: ", len(self.hasharray))
        elif(self.hasharray != None):
            print("Hash Set Capacity: ", len(self.hasharray))
        print("Number of Collisions: ", self.collisions)
        print("Current Load Factor: ", self.load_factor, " (threshold:0.6 or 0.8 for separate chaining)")

# This is a cell structure assuming Open Addressing
# It should contain and element that is the key and a state which is empty, in_use or deleted
# You will need alternative data-structures for separate chaining
class cell:
    def __init__(self):
        pass
        
class state(Enum):
    empty = 0
    in_use = 1
    deleted = 2
        
# Hashing Modes
class HashingModes(Enum):
    HASH_1_LINEAR_PROBING=0
    HASH_1_QUADRATIC_PROBING=1
    HASH_1_DOUBLE_HASHING=2
    HASH_1_SEPARATE_CHAINING=3
    HASH_2_LINEAR_PROBING=4
    HASH_2_QUADRATIC_PROBING=5
    HASH_2_DOUBLE_HASHING=6
    HASH_2_SEPARATE_CHAINING=7

# Debugging Code Area
# aa = hashset()
# aa.mode = 3
# aa.insert("asdfghj")
# aa.insert("jhgfdsa")
# aa.insert("asdfghk")
# aa.insert("asdfghl")
# aa.insert("a")
# aa.insert("b")
# aa.insert("a0")
# aa.insert("c")
# aa.insert("d")
# aa.insert("e")
# # print(aa.find("asdfghj"))
# # # print(aa.mode == HashingModes.HASH_1_SEPARATE_CHAINING.value)
# # # print(aa.mode == HashingModes.HASH_1_SEPARATE_CHAINING)
# # # print(aa.mode == HashingModes.HASH_1_QUADRATIC_PROBING.value)
# aa.print_set()
# aa.print_stats()