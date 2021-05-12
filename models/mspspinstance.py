mport minizinc
from minizinc import Instance, Model, Solver
from datetime import datetime

now = datetime.now()
def main():
    mpsp = Model("folderza\mspsp.mzn")
    mpsp.add_file("folderza\instances\set-a\inst_set1a_sf0.5_nc1.8_n20_m13_02.dzn")
    gecode = Solver.lookup("chuffed")
    instance = Instance(gecode, mpsp)
    instance["full_output"] = 1
    result = instance.solve()
    print(result)


if __name__ == "__main__":
    main()

now2= datetime.now()
print(now2 - now)
