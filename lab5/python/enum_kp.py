import sys

from knapsack import knapsack

class enum_knapsack(knapsack):
    def __init__(self, filename):
        knapsack.__init__(self, filename)
        
    def enumerate(self):
        # Do an exhaustive search (aka enumeration) of all possible ways to pack
        # the knapsack.
        # This is achived by creating every "binary" solution vectore of length Nitems.
        # For each solution vector, its value and weight is calculated
        
        solution = [False]*(self.Nitems + 1) # (binary/ true/false) solution vectore representing items pack
        best_solution = [False]*(self.Nitems + 1) # (binary) solution veectore for best solution found
        j = 0.0
        
        # self.QUIET = False
        self.QUIET = True
        best_value = 0 # total value packed in the best solution

        count = 0
        while (not self.next_binary(solution, self.Nitems)):
            # ADDED CODE for tracking count and update the best_value
            count += 1
            # calculates the value and weight and feasibility
            infeasible = self.check_evaluate_and_print_sol(solution)
            if(infeasible == False and best_value <= self.total_value):
                best_value = self.total_value
                best_solution = solution
                print(str((count/(2**(self.Nitems)))*100)+" %, Current Best Value: " + str(best_value))
            # ADDED CODE ALREADY
        print("100 %, Current Best Value: " + str(best_value))
    def next_binary(self, sol, Nitems):
        # Called with a "binary" vector of length Nitmes, this
        # method "adds 1" to the vector, e.g. 0001 would turn to 0010.
        # If the string overflows, then the function returs True, else it returns False
        i = Nitems
        while (i > 0):
            if (sol[i]):
                sol[i] = False
                i = i -1
            else:
                sol[i] = True
                break
        if (i == 0):
            return True
        else:
            return False
        
            


knapsk = enum_knapsack(sys.argv[1])
knapsk.print_instance()
knapsk.enumerate()

