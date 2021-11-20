import config

class bstree:
    def __init__(self):
        # Initialise variables to use
        self.verbose = config.verbose
        self.left_height = 0
        self.right_height = 0
        self.height = max(self.left_height, self.right_height)
        self.compare_no = 0
        self.ins_find = 0
        self.average_stat = 0

    def size(self):
        # Size of the whole tree, which is the number of nodes in the tree in total.
        if (self.tree()):
            return 1 + self.left.size() + self.right.size()
        return 0

    def tree(self):
        # This counts as a tree if it has a field self.value
        # it should also have sub-trees self.left and self.right
        return hasattr(self, 'value')

    def insert(self, value):
        if(isinstance(value,int) == False):
            initial_value = value
            value = 0
            for i in range(len(initial_value)):
                # Hashing Function implementation
                transit = ord(initial_value[i])*((31)**(len(initial_value)-1-i))
                value += transit

        if (self.tree()):
            # If tree is not NULL then insert into the correct sub-tree
            if(self.value == value):
                # Replicate detected, we ignore it.
                self.compare_no += 1
                self.ins_find += 1
                self.average_stat = self.compare_no/self.ins_find
                return [self.height,2,False]
            elif(value < self.value):
                # For values less than the current node value, we increment the times of comparisons & insert by 1, 
                # and compute the average, return a list showing:
                # [current_subnode_returned_height(left_node_height), current_compare_number_for_the_subnode , insert_status].
                res_arr = self.left.insert(value)
                self.left_height = res_arr[0]
                self.height = max(self.left_height, self.right_height)+1
                self.compare_no += res_arr[1]
                self.ins_find += 1
                self.average_stat = self.compare_no/self.ins_find
                return [self.height,res_arr[1]+1,res_arr[2]]
            elif(value > self.value):
                # For values more than the current node value, we increment the times of comparisons & insert by 1, 
                # and compute the average, return a list showing:
                # [current_subnode_returned_height(right_node_height), current_compare_number_for_the_subnode , insert_status].
                res_arr = self.right.insert(value)
                self.right_height = res_arr[0]
                self.height = max(self.left_height, self.right_height)+1
                self.compare_no += res_arr[1]
                self.ins_find += 1
                self.average_stat = self.compare_no/self.ins_find
                return [self.height,res_arr[1]+1,res_arr[2]]

        else:
            # Otherwise create a new node containing the value
            self.value = value
            self.left = bstree()
            self.right = bstree()
            self.left_height = 0
            self.right_height = 0
            self.height = max(self.left_height, self.right_height)+1

            self.compare_no = 0
            self.ins_find = 1
            self.average_stat = 0

            return [self.height,1,True]

    def find(self, value):
        if(isinstance(value,int) == False):
            initial_value = value
            value = 0
            for i in range(len(initial_value)):
                # Hashing Function implementation
                transit = ord(initial_value[i])*((31)**(len(initial_value)-1-i))
                value += transit

        if self.tree():
            # Complete the find function
            return self.find_helper(value)[0]
        return False

    def find_helper(self,value):
        # Complete the find helper function
        # Returned Array: [find_status, current_tree_height_at_that_node]
        if self.tree():
            # Complete the find function
            if(self.value == value):
                self.compare_no += 1
                self.ins_find += 1
                self.average_stat = self.compare_no/self.ins_find
                return [True,2]
            elif(value < self.value):
                # Left Subtree
                res_arr = self.left.find_helper(value)
                self.compare_no += res_arr[1]
                self.ins_find += 1
                self.average_stat = self.compare_no/self.ins_find
                return [res_arr[0],res_arr[1]+1]
            elif(value > self.value):
                # Right Subtree
                res_arr = self.right.find_helper(value)
                self.compare_no += res_arr[1]
                self.ins_find += 1
                self.average_stat = self.compare_no/self.ins_find
                return [res_arr[0],res_arr[1]+1]       
        return [False,1]

    def print_set_recursive(self, depth):
        if (self.tree()):
            for i in range(depth):
                print(" ", end='')
            print("%s" % self.value)
            self.left.print_set_recursive(depth + 1)
            self.right.print_set_recursive(depth + 1)

    def print_set(self):
        print("Tree:\n")
        self.print_set_recursive(0)

    def print_stats(self):
        # Update code to record and print statistic
        print("Tree Height: ", self.height)
        print("The average number of comparisons per insertion or find: ", self.average_stat)

# Debugging Area
# aa = bstree()
# aa.insert("aaa")
# print(aa.find("aaa"))

# aa.insert(1)
# aa.insert(6)
# aa.insert(-1)
# aa.insert(2)
# aa.insert(5)
# aa.insert("aaa-aaa")
# aa.insert("aab")
# # aa.insert(5.5)
# # aa.insert(5.5)
# # aa.insert(5)
# # aa.insert(1)

# aa.print_stats()
# aa.print_set()