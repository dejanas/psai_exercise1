from minizinc import Instance, Model, Solver


def main():
    # Load mpsp model from file
    mpsp = Model("models\mspsp.mzn")
    # Add instance file
    mpsp.add_file("instances\set-a\inst_set1a_sf0_nc1.5_n20_m10_00.dzn")
    # Find the MiniZinc solver configuration for chuffed keywoard
    chuffed = Solver.lookup("chuffed")
    # Create an Instance of the mpsp model for Chuffed
    instance = Instance(chuffed, mpsp)
    # Set full_output to true
    instance["full_output"] = 1

    result = instance.solve()
    # Output the result
    print(result)


if __name__ == "__main__": 
	main() 
