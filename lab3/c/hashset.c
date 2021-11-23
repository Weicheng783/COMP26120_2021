#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#define __USE_BSD
#include <string.h>
#include <math.h>

#include "global.h"
#include "hashset.h"

int previousPrime(int n);
// Can be redefined if Value_Type changes
int compare(Value_Type a, Value_Type b){
  return strcmp(a,b);
}

// Helper functions for finding prime numbers 
bool isPrime (int n)
{
  for (int i = 2; i*i <= n; i++)
    if (n % i == 0)
      return false;
  return true;
}


int nextPrime(int n)
{
  for (; !isPrime(n); n++);
  return n;
}

int previousPrime(int n){
    n = n - 1;
    while (!isPrime(n)){
        n = n - 1;
    }
    return n;
}
// Your code


struct hashset* initialize_set (int size)  
{

// TODO create initial hash table
    if(mode == HashingModes.HASH_1_SEPARATE_CHAINING.value || mode == HashingModes.HASH_2_SEPARATE_CHAINING.value){
		hasharray1 = malloc(size * sizeof(int *));
		if(hasharray1 == NULL) return -1;
		for(int i = 0; i<M; i++){
			hasharray1[i] = malloc(size * sizeof(int));
			if (hasharray1[i] == NULL) return -1;
		}
    }
    else{
	  	hasharray = malloc(size * sizeof(int));
	  	if(hasharray == NULL) return -1;
	}
    // For the double hashing, we select the value that is the prime just below the size of it.
    double_hashing_value = previousPrime(size);

}

void tidy(struct hashset* set)
{
// TODO tidy up
	free(set);
}

int size(struct hashset* set){
// TODO return number of values stored in table
	return set.size;
} 

struct hashset* insert (Value_Type value, struct hashset* set)
{
// TODO code for inserting into hash table
        // Code for inserting into hash table
        // Check first if the input is String or Int
        if(isinstance(value,int) == False){
            initial_value = value
            value = 0
            for (int i=0; i <= value; i++){
                if(self.mode <= 3){
                    // The First Hash Function
                    transit = ord(initial_value[i])*((31)**(len(initial_value)-1-i))
                }
                else{
                    // The Second Hash Function
                    transit = ord(initial_value[i])*(3**i)
           		}
           		value += transit
           	}
        }

        // Flag meanings for 0: Normal insert; 1: Found duplicates; 2: Rehashing needed.
        flag = 0
        # Threshold 0.6 for open addressing, 0.8 for separate chaining.
        if(self.load_factor >= 0.75 and (self.mode != HashingModes.HASH_1_SEPARATE_CHAINING.value and self.mode != HashingModes.HASH_2_SEPARATE_CHAINING.value)):
            flag = 2
        elif(self.load_factor >= 0.9 and (self.mode == HashingModes.HASH_1_SEPARATE_CHAINING.value or self.mode == HashingModes.HASH_2_SEPARATE_CHAINING.value)):
            flag = 2
        if(flag != 2):
            # Separate Chaining and Open Addressing follow different routes.
            # True for OA, False for SC.
            if(self.mode != HashingModes.HASH_1_SEPARATE_CHAINING.value and self.mode != HashingModes.HASH_2_SEPARATE_CHAINING.value):
                # Detect if a place has been occupied.
                if(self.hasharray[value%self.hash_table_size] == None):
                    if(self.load_factor >= 0.75):
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
                        if(self.load_factor >= 0.75):
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

}

bool find (Value_Type value, struct hashset* set)
{
// TODO code for looking up in hash table
}

void print_set (struct hashset* set)
{
// TODO code for printing hash table
}

void print_stats (struct hashset* set)
{
// TODO code for printing statistics
}
