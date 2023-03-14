from pyteal import *

var_owner = Bytes("owner")
var_counter = Bytes("counter")

def buggy_program():
    """
    This is a stateful smart contract with a purposeful bug.
    It is used to demonstrate using the debugger to uncover the bug.
    """
    init_contract = Seq([
        App.globalPut(var_owner, Txn.sender()),
        App.globalPut(var_counter, Int(0)),
        Return(Int(1))
    ])

    is_owner = Txn.sender() == App.globalGet(var_owner)

    # Assign the transactions to variables
    payment_txn = Gtxn[0]
    app_txn = Txn # This transaction is at index 1

    payment_check = payment_txn.type_enum() == TxnType.Payment
    payment_receiver_check = payment_txn.receiver() == App.globalGet(var_owner)
    app_check = app_txn.type_enum() == TxnType.ApplicationCall

    group_checks = And(
        payment_check,
        payment_receiver_check,
        app_check,
    )

    counter = App.globalGet(var_counter)
    increment_counter  = Seq([
        Assert(group_checks),
        # Increment the counter if the sender sends the owner more than 10 Algos.
        # Otherwise decrement the counter
        If(payment_txn.amount() >= Int(10 * 1000000),
            App.globalPut(var_counter, counter + Int(1)),
            If(counter > Int(0),
                App.globalPut(var_counter, counter - Int(1)),
            ),
        ),

        Return(Int(1))
    ])

    program = Cond(
        [Txn.application_id() == Int(0), init_contract],
        [Txn.on_completion() == OnComplete.DeleteApplication, Return(is_owner)],
        [Txn.on_completion() == OnComplete.UpdateApplication, Return(is_owner)],
        [Txn.on_completion() == OnComplete.OptIn, Return(Int(1))],
        [Txn.on_completion() == OnComplete.CloseOut, Return(Int(1))],
        [Txn.on_completion() == OnComplete.NoOp, increment_counter],
    )

    return program

if __name__ == "__main__":
    print(compileTeal(buggy_program(), Mode.Application, version=4))