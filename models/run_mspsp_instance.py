from minizinc import Instance, Model, Solver
from datetime import datetime


def main():
    # Capture start time
    startTime = datetime.now()
    # Load mpsp model from file
    mpsp = Model("models\parameter_model.mzn")
    # Add instance file
    mpsp.add_file("instances\set-a\inst_set1a_sf0_nc1.5_n20_m10_00.dzn")
    # Find the MiniZinc solver configuration for chuffed keywoard
    chuffed = Solver.lookup("chuffed")
    # Create an Instance of the mpsp model for Chuffed
    instance = Instance(chuffed, mpsp)
    # Set full_output to true
    instance["full_output"] = 1
    # Run solver
    result = instance.solve()
    # Capture end time
    endTime = datetime.now()
    # Output the result
    print(result)
    # Output runtime
    print(endTime - startTime)


if __name__ == "__main__": 
	main() 
