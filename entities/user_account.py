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
