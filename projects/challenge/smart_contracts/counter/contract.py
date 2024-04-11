# pyright: reportMissingModuleSource=false
from algopy import ARC4Contract, LocalState, GlobalState, UInt64, Txn, arc4, Global


class Counter(ARC4Contract):

    count: LocalState[UInt64]
    counters: GlobalState[UInt64]
    
    # Initilising our LocalState 
    def __init__(self) -> None:
        self.count = LocalState(UInt64) # initilising count as localstate with UInt64
        self.counters = GlobalState(UInt64(1)) # initilising counters as globalstate with UInt64

    @arc4.baremethod(allow_actions=["OptIn"])
    def opt_in(self) -> None:
        self.count[Txn.sender] = UInt64(0)
        self.counters.value += 1

    @arc4.abimethod()
    def increment(self) -> arc4.UInt64:
        assert Txn.sender.is_opted_in(
            Global.current_application_id
        ), "Sender must opt-in to the contract"
        self.count[Txn.sender] += 1
        return arc4.UInt64(self.count[Txn.sender])
    
