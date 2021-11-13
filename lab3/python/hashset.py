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
        
    def nextPrime(self, n):
        while (not self.isPrime(n)):
            n = n + 1
        return n

    def previousPrime(self, n):
        while (not self.isPrime(n)):
            n = n - 1
        return n

    def __init__(self):
        # TODO: create initial hash table
        self.verbose = config.verbose
        self.mode = config.mode
        self.hash_table_size = config.init_size
        self.collisions = 0
        self.total_obj = 0
        self.load_factor = 0.0

        # self.hasharray = [None]*5
        # self.hash_table_size = 5
        self.hasharray = [None]*self.hash_table_size

        self.double_hashing_value = self.previousPrime(self.hash_table_size)
        # print(self.double_hashing_value)
        # print(self.double_hashing_value)

        self.mode = 2
        # print(hasharray)

    # Helper functions for finding prime numbers
        
    def insert(self, value):
        # TODO code for inserting into hash table

        if(isinstance(value,int) == False):
            initial_value = value
            value = 0
            for i in range(len(initial_value)):
                transit = ord(initial_value[i])*((31)**(len(initial_value)-1-i))
                value += transit

        
        flag = 0
        if(self.load_factor >= 0.6):
            flag = 2
        if(flag != 2):
            if(self.hasharray[value%self.hash_table_size] == None):
                if(self.load_factor >= 0.6):
                    flag = 2
                else:
                    self.hasharray[value%self.hash_table_size] = value
                    self.total_obj += 1
                    self.load_factor = self.total_obj/len(self.hasharray)
            else:
                # print("we allocated again.")
                collisions = 0
                index = value%self.hash_table_size

                loop_quadratic = 1 # This value is used in Quadratic Probing & Double Hashing
                
                while(self.hasharray[index] != None):
                    if(self.load_factor >= 0.6):
                        collisions = 0
                        flag = 2
                        break
                    if(self.hasharray[index] == value):
                        # print(self.hasharray)
                        # print("duplicates detected: ", value)
                        collisions = 0
                        flag = 1
                        break
                    # Case Distinction               
                    if(self.mode == HashingModes.HASH_1_LINEAR_PROBING.value):
                        collisions += 1
                        if(index == self.hash_table_size-1):
                            index = 0
                        else:
                            index += 1
                        if(index == value%self.hash_table_size):
                            # print("no more space, rehashing needed.")
                            collisions = 0 # not sure
                            flag = 2
                            break

                    elif(self.mode == HashingModes.HASH_1_QUADRATIC_PROBING.value):
                        collisions += 1
                        if(index+((loop_quadratic)**2) >= self.hash_table_size-1):
                            index = (index+((loop_quadratic)**2)) % self.hash_table_size
                        else:
                            index += ((loop_quadratic)**2)
                        loop_quadratic += 1

                    elif(self.mode == HashingModes.HASH_1_DOUBLE_HASHING.value):
                        
                        if( self.hasharray[(index+loop_quadratic*(value%self.double_hashing_value))%self.hash_table_size] != None):
                            collisions += 1
                            loop_quadratic += 1
                        else:
                            self.hasharray[(index+loop_quadratic*(value%self.double_hashing_value))%self.hash_table_size] = value
                            break

                if(flag != 1 and flag != 2 and self.mode != HashingModes.HASH_1_DOUBLE_HASHING.value):
                    # print("reallocated at: ", index)
                    self.hasharray[index] = value
                    self.total_obj += 1
                    self.load_factor = self.total_obj/len(self.hasharray)
                    # print(self.load_factor)
                    # print(self.hasharray)
                self.collisions += collisions

        if(flag == 2):
            # print("Rehashing...")
            flag = 0
            self.hash_table_size = math.ceil(self.hash_table_size*1.5)
            self.collisions = 0
            self.total_obj = 0
            self.load_factor = 0.0
            array_cpy = self.hasharray
            self.hasharray = [None]*self.hash_table_size
            for i in array_cpy:
                if(i != None):
                    self.insert(i)
            self.insert(value)
            # print("Rehashing Completed.")
            # print(self.hasharray)
        # print(self.hasharray)
    def find(self, value):
        # TODO code for looking up in hash table
        if(isinstance(value,int) == False):
            initial_value = value
            value = 0
            for i in range(len(initial_value)):
                transit = ord(initial_value[i])*((31)**(len(initial_value)-1-i))
                value += transit

        index = value%self.hash_table_size
        loop_quadratic = 1
        while(self.hasharray[index] != value):
            if(self.mode == HashingModes.HASH_1_LINEAR_PROBING.value):
                if(index == self.hash_table_size-1):
                    index = 0
                else:
                    index += 1
                if(index == value%self.hash_table_size):
                    # print("Not Found!")
                    return False
            elif(self.mode == HashingModes.HASH_1_QUADRATIC_PROBING.value):
                # if(value in self.hasharray):
                #     return True
                # else:
                #     return False
                if(index+((loop_quadratic)**2) >= self.hash_table_size-1):
                    index = (index+((loop_quadratic)**2)) % self.hash_table_size
                else:
                    index += ((loop_quadratic)**2)
                if(loop_quadratic == self.hash_table_size):
                    return False
                loop_quadratic += 1
            elif(self.mode == HashingModes.HASH_1_DOUBLE_HASHING.value):
                if( self.hasharray[(index+loop_quadratic*(value%self.double_hashing_value))%self.hash_table_size] != value):
                    if(loop_quadratic == self.hash_table_size):
                        return False
                    loop_quadratic += 1
                else:
                    return True
                # if(index+((loop_quadratic)**2) >= self.hash_table_size-1):
                #     index = (index+((loop_quadratic)**2)) % self.hash_table_size
                # else:
                #     index += ((loop_quadratic)**2)
                # if(loop_quadratic_recorder == self.hasharray):
                #     return False
                # else:
                #     loop_quadratic_recorder[index] = self.hasharray[index]
                #     # print(loop_quadratic_recorder)
                # loop_quadratic += 1
                # print("!index: ",index)
                # loop_quadratic_recorder = self.hasharray
                # # print("!Arrayis: ", self.hasharray)
                # print("=?:", loop_quadratic_recorder == self.hasharray)
                # return True

        # print(self.hasharray)
        # print("Found at: ", index)
        return True

    def print_set(self):
        # TODO code for printing hash table
        print(self.hasharray)
    def print_stats(self):
        # TODO code for printing statistics
        print("Total Objects in the Hash Set: ", self.total_obj)
        print("Hash Set Capacity: ", len(self.hasharray))
        print("Number of Collisions: ", self.collisions)
        print("Current Load Factor: ", self.load_factor, " (threshold:0.6)")



# aa.insert("abc")
# aa.insert("cba")
# print(aa.find("abc"))
# print(aa.find("cba"))
# aa.print_stats()
# aa.print_set()

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

# aa = hashset()
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
# print(aa.find("asdfghj"))
# print(aa.mode == HashingModes.HASH_1_QUADRATIC_PROBING.value)
# aa.print_set()
