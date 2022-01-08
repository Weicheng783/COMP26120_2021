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
        
        self.QUIET = False
        best_value = 0 # total value packed in the best solution
        
        while (not self.next_binary(solution, self.Nitems)):
            # ADD CODE IN HERE TO KEEP TRACK OF FRACTION OF ENUMERATION DONE
            
            # calculates the value and weight and feasibility
            infeasible = self.check_evaluate_and_print_sol(solution)
            
            # ADD CODE TO PRINT OUT BEST SOLUTION
            
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

