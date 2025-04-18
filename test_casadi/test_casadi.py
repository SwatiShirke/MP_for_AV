import casadi as ca


def main():
    A = ca.SX.sym("A",3,3)
    print(A)
    A_reshaped = ca.reshape(A, -1, 1)
    print(A_reshaped)
    
    

if __name__ == "__main__":
    main()

