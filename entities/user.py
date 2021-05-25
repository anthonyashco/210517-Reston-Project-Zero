class User():
    count = 0

    def __init__(self,
                 user_id: int = 0,
                 email: str = None,
                 pass_hash: str = None,
                 pass_salt: str = None,
                 first_name: str = None,
                 last_name: str = None,
                 status: str = None) -> None:
        self.id = user_id
        self.email = email
        self.pass_hash = pass_hash
        self.pass_salt = pass_salt
        self.first_name = first_name
        self.last_name = last_name
        self.status = status
        User.count += 1

    def __str__(self) -> str:
        return f"User {self.user_id} ({self.email}). Status: {self.status}"
