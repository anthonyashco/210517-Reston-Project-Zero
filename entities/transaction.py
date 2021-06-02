from __future__ import annotations
from datetime import datetime


class Transaction():

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
        self.destination_account_id = int(destination_account_id)
        self.transfer_amount = float(transfer_amount)
        self.transaction_time = transaction_time

    def __str__(self) -> str:
        return "Transaction {}: {} ({}) transferred {:.2f} to {} at {}.".format(
            self.id, self.source_account_id, self.source_user_id,
            self.transfer_amount, self.destination_account_id,
            self.transaction_time)

    def to_json(self) -> dict:
        return {
            "id":
                self.id,
            "source_account_id":
                self.source_account_id,
            "source_user_id":
                self.source_user_id,
            "transfer_amount":
                f"{self.transfer_amount:.2f}",
            "destination_account_id":
                self.destination_account_id,
            "transaction_time":
                self.transaction_time.strftime("%Y.%m.%d, %H:%M:%S")
        }

    @staticmethod
    def from_json(json: dict) -> Transaction:
        return Transaction(json["id"], json["source_account_id"],
                           json["source_user_id"],
                           json["destination_account_id"],
                           json["transfer_amount"], json["transaction_time"])
