from pyteal import *

# 3 vulnerabilities
def logic_signature():
    recv_cond = Txn.receiver() ==  Addr("B6Q6ZZOH5IOCG5PJ366WJU26L5Y2EASQK6ZIC7K6H3V62PZTG7HOW4FKAA")
    amount_cond = Txn.amount() == Int(2_000_000)

    program = And(recv_cond, amount_cond)

    return compileTeal(program, Mode.Signature, version=4)


if __name__ == "__main__":
    print(logic_signature())