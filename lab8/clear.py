from pyteal import *

def clear():
    return Int(1)

if __name__ == "__main__":
    print(compileTeal(clear(), Mode.Application, version=4))
