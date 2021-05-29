from __future__ import annotations


class Account():

    def __init__(self,
                 account_id: int = 0,
                 account_type: str = None,
                 balance: float = None) -> None:
        self.id = account_id
        self.type = account_type
        self.balance = balance

    def __str__(self) -> str:
        return f"Account {self.id} ({self.type}): {self.balance:.2f}"

    def to_json(self) -> dict:
        return {
            "id": self.id,
            "account_type": self.type,
            "balance": self.balance
        }

    @staticmethod
    def from_json(json: dict) -> Account:
        return Account(json["id"], json["account_type"], json["balance"])
