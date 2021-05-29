from abc import ABC, abstractmethod
from typing import List
from entities.account import Account
from entities.transaction import Transaction
from entities.user import User


class BankingInterface(ABC):

    @abstractmethod
    def create_user(self, user: User) -> User:
        pass

    @abstractmethod
    def get_user(self, user_id: int) -> User:
        pass

    @abstractmethod
    def get_users_from_account(self, account: Account) -> List[User]:
        pass

    @abstractmethod
    def get_users(self) -> List[User]:
        pass

    @abstractmethod
    def update_user(self, user: User) -> User:
        pass

    @abstractmethod
    def delete_user(self, user: User) -> bool:
        pass

    @abstractmethod
    def create_account(self, user: User, account: Account):
        pass

    @abstractmethod
    def get_accounts_from_user(self, user: User) -> List[Account]:
        pass

    @abstractmethod
    def get_accounts_from_range(self, above: int, below: int) -> List[Account]:
        pass

    @abstractmethod
    def get_user_specific_account(self, u_id: int, a_id: int) -> Account:
        pass

    @abstractmethod
    def update_user_specific_account(self, user: User,
                                     account: Account) -> Account:
        pass

    @abstractmethod
    def delete_user_specific_account(self, user: User,
                                     account: Account) -> bool:
        pass

    @abstractmethod
    def deposit(self, user: User, account: Account,
                tran: Transaction) -> Transaction:
        pass

    @abstractmethod
    def withdraw(self, user: User, account: Account,
                 tran: Transaction) -> Transaction:
        pass

    @abstractmethod
    def transfer(self, user: User, account: Account, recipient: Account,
                 tran: Transaction) -> Transaction:
        pass
