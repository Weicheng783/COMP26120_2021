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
        n = n - 1
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

        # self.rehashingg = False

        # self.hasharray = [None]*7
        # self.hash_table_size = 7
        if(self.mode == HashingModes.HASH_1_SEPARATE_CHAINING.value or self.mode == HashingModes.HASH_2_SEPARATE_CHAINING.value):
            self.hasharray = [[None]]*self.hash_table_size
        else:
            self.hasharray = [None]*self.hash_table_size

        self.double_hashing_value = self.previousPrime(self.hash_table_size)
        # print(self.double_hashing_value)
        # print(self.double_hashing_value)

        # self.mode = 2
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
        if(self.load_factor >= 0.6 and (self.mode != HashingModes.HASH_1_SEPARATE_CHAINING.value and self.mode != HashingModes.HASH_2_SEPARATE_CHAINING.value)):
            flag = 2
        elif(self.load_factor >= 0.8 and (self.mode == HashingModes.HASH_1_SEPARATE_CHAINING.value or self.mode == HashingModes.HASH_2_SEPARATE_CHAINING.value)):
            flag = 2
        if(flag != 2):
            if(self.mode != HashingModes.HASH_1_SEPARATE_CHAINING.value and self.mode != HashingModes.HASH_2_SEPARATE_CHAINING.value):
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
                            # collisions = 0
                            flag = 2
                            break
                        if(self.hasharray[index] == value):
                            # print(self.hasharray)
                            # print("duplicates detected: ", value)
                            collisions = 0
                            flag = 1
                            break
                        # Case Distinction               
                        if(self.mode == HashingModes.HASH_1_LINEAR_PROBING.value or self.mode == HashingModes.HASH_2_LINEAR_PROBING.value):
                            collisions += 1
                            if(index == self.hash_table_size-1):
                                index = 0
                            else:
                                index += 1
                            if(index == value%self.hash_table_size):
                                # print("no more space, rehashing needed.")
                                # collisions = 0 # not sure
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
                        # print("reallocated at: ", index)
                        self.hasharray[index] = value
                        self.total_obj += 1
                        self.load_factor = self.total_obj/len(self.hasharray)
                        # print(self.load_factor)
                        # print(self.hasharray)
                    self.collisions += collisions
            else:
                # print(self.hasharray)
                if(self.hasharray[value%self.hash_table_size] == None):
                    self.hasharray[value%self.hash_table_size] = [value]
                    self.total_obj += 1
                    self.load_factor = self.total_obj/self.hash_table_size
                else:

                    for i in range(len(self.hasharray[value%self.hash_table_size])):
                        # Reject this value as it is a replicate
                        if(value == self.hasharray[value%self.hash_table_size][i]):
                            break
                        elif(i == len(self.hasharray[value%self.hash_table_size])-1):
                            # if(self.rehashingg == True):
                            #     print(value)
                            #     print(self.hasharray) 
                            #     print(value%self.hash_table_size)
                            self.hasharray[value%self.hash_table_size].append(value)

                            self.collisions += len(self.hasharray[value%self.hash_table_size])
                            self.total_obj += 1
                            self.load_factor = self.total_obj/self.hash_table_size
                            break
        if(flag == 2):
            # print("Rehashing...")
            flag = 0
            self.hash_table_size = math.ceil(self.hash_table_size*1.5)
            # self.collisions = 0
            self.total_obj = 0
            self.load_factor = 0.0
            array_cpy = self.hasharray
            if(self.mode == HashingModes.HASH_1_SEPARATE_CHAINING.value or self.mode == HashingModes.HASH_2_SEPARATE_CHAINING.value):
                self.hasharray = [None]*self.hash_table_size
                for i in range(len(array_cpy)):
                    if(array_cpy[i] != None):
                        for j in range(len(array_cpy[i])):
                            if(array_cpy[i][j] != None):
                                self.insert(array_cpy[i][j])
                                # print(self.hasharray)
                # self.rehashingg = True
                self.insert(value)
            else:
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

        if(self.mode != HashingModes.HASH_1_SEPARATE_CHAINING.value and self.mode != HashingModes.HASH_2_SEPARATE_CHAINING.value):
            loop_quadratic = 1
            while(self.hasharray[index] != value):
                if(self.mode == HashingModes.HASH_1_LINEAR_PROBING.value or self.mode == HashingModes.HASH_2_LINEAR_PROBING.value):
                    if(index == self.hash_table_size-1):
                        index = 0
                    else:
                        index += 1
                    if(index == value%self.hash_table_size):
                        # print("Not Found!")
                        return False
                elif(self.mode == HashingModes.HASH_1_QUADRATIC_PROBING.value or self.mode == HashingModes.HASH_2_QUADRATIC_PROBING.value):
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
                elif(self.mode == HashingModes.HASH_1_DOUBLE_HASHING.value or self.mode == HashingModes.HASH_2_DOUBLE_HASHING.value):
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
        else:
            if(self.hasharray[index] == None):
                return False
            else:
                for i in range(len(self.hasharray[index])):
                    if(value == self.hasharray[index][i]):
                        return True
                return False
    def print_set(self):
        # TODO code for printing hash table
        print(self.hasharray)
    def print_stats(self):
        # TODO code for printing statistics
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
