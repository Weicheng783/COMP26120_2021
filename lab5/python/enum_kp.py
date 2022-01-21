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
        
        # solution = [False]*(self.Nitems + 1) # (binary/ true/false) solution vectore representing items pack
        # best_solution = [False]*(self.Nitems + 1) # (binary) solution veectore for best solution found
        solution = []
        for i in range(0,self.Nitems + 1):
            solution.append(False)

        best_solution = []
        for i in range(0,self.Nitems + 1):
            best_solution.append(False)
        j = 0.0

        self.QUIET = True
        best_value = 0 # total value packed in the best solution

        count = 0
        temp_sol = []
        while (not self.next_binary(solution, self.Nitems)):

            # ADDED CODE for tracking count and update the best_value
            count += 1
            # calculates the value and weight and feasibility
            infeasible = self.check_evaluate_and_print_sol(solution)
            if(infeasible == False and best_value <= self.total_value):
                best_value = self.total_value
                best_solution = solution
                # print(self.best_solution)
                print(str((count/(2**(self.Nitems)))*100)+" %, Current Best Value: " + str(best_value))
                for i in range(0, len(best_solution)):
                    temp_sol.append(best_solution[i])

            if(self.next_binary(solution, self.Nitems)):
                # print(temp_sol)
                print("100 %, Current Best Value: " + str(best_value))
                # print(temp_sol[len(temp_sol)-1-self.Nitems:len(temp_sol)])
                return temp_sol[len(temp_sol)-1-self.Nitems:len(temp_sol)]

    def next_binary(self, sol, Nitems):
        # Called with a "binary" vector of length Nitmes, this
        # method "adds 1" to the vector, e.g. 0001 would turn to 0010.
        # If the string overflows, then the function returns True, else it returns False
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
best_sol = knapsk.enumerate()
knapsk.QUIET = False
knapsk.check_evaluate_and_print_sol(best_sol)

