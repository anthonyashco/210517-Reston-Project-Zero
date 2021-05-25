from datetime import datetime


class Transaction():
    count = 0

    def __init__(self,
                 transaction_id: int = 0,
                 source_account_id: int = None,
                 source_user_id: int = None,
                 destination_account_id: int = None,
                 transfer_amount: float = None,
                 transaction_time: datetime = None) -> None:
        self.id = transaction_id
        self.source_account_id = source_account_id
        self.source_user_id = source_user_id
        self.destination_account_id = destination_account_id
        self.transfer_amount = transfer_amount
        self.transaction_time = transaction_time
        Transaction.count += 1

    def __str__(self) -> str:
        return "Transaction {}: {} ({}) transferred {:.2f} to {} at {}.".format(
            self.id, self.source_account_id, self.source_user_id,
            self.transfer_amount, self.destination_account_id,
            self.transaction_time)
