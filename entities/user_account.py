from __future__ import annotations


class UserAccount():
    count = 0

    def __init__(self,
                 join_id: int = 0,
                 user_id: int = None,
                 account_id: int = None) -> None:
        self.id = join_id
        self.user_id = user_id
        self.account_id = account_id
        UserAccount.count += 0

    def __str__(self) -> str:
        return f"Join {self.id}: user {self.user_id}, account {self.account_id}"

    def to_json(self) -> dict:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "account_id": self.account_id
        }

    @staticmethod
    def from_json(json: dict) -> UserAccount:
        return UserAccount(json["id"], json["user_id"], json["account_id"])
