class Account():
    count = 0

    def __init__(self,
                 account_id: int = 0,
                 account_type: str = None,
                 balance: float = None) -> None:
        self.id = account_id
        self.type = account_type
        self.balance = balance
        Account.count += 1

    def __str__(self) -> str:
        return f"Account {self.id} ({self.type}): {self.balance:.2f}"
