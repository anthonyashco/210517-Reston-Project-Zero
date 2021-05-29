from exceptions.resource_not_found import ResourceNotFound
from entities.user_account import UserAccount
from daos.account_dao import AccountDAO
from daos.transaction_dao import TransactionDAO
from daos.user_account_dao import UserAccountDAO
from daos.user_dao import UserDAO
from entities.account import Account
from entities.transaction import Transaction
from entities.user import User
from services.banking_int import BankingInterface
from typing import List


class BankingService(BankingInterface):

    def __init__(self, account_dao: AccountDAO, transaction_dao: TransactionDAO,
                 user_account_dao: UserAccountDAO, user_dao: UserDAO):
        self.a = account_dao
        self.t = transaction_dao
        self.ua = user_account_dao
        self.u = user_dao

    def create_user(self, user: User) -> User:
        return self.u.create(user)

    def get_user(self, user_id: int) -> User:
        return self.u.get(user_id)

    def get_users_from_account(self, account: Account) -> List[User]:
        return self.u.get_from_account(account)

    def get_users(self) -> List[User]:
        return self.u.get_all()

    def update_user(self, user: User) -> User:
        return self.u.update(user)

    def delete_user(self, user: User) -> bool:
        return self.u.delete(user)

    def create_account(self, user: User, account: Account) -> Account:
        # TODO: Test
        account = self.a.create(account)
        join = UserAccount("default", user.id, account.id)
        self.ua.create(join)
        return account

    def get_accounts_from_user(self, user: User) -> List[Account]:
        return self.a.get_from_user(user)

    def get_accounts_from_range(self, above: int, below: int) -> List[Account]:
        # TODO: Test
        accounts = self.a.get_all()
        return [
            account for account in accounts
            if account.id >= above and account.id <= below
        ]

    def get_user_specific_account(self, u_id: int, a_id: int) -> Account:
        # TODO: Test
        joins = self.ua.get_from_id_pair(u_id, a_id)
        if len(joins) == 0:
            raise ResourceNotFound(
                "This user / account pairing does not exist.")
        else:
            return self.a.get(joins[0].id)

    def update_user_specific_account(self, user: User,
                                     account: Account) -> Account:
        # TODO: Test
        joins = self.ua.get_from_id_pair(user.id, account.id)
        if len(joins) == 0:
            raise ResourceNotFound(
                "This user / account pairing does not exist.")
        else:
            return self.a.update(account)

    def delete_user_specific_account(self, user: User,
                                     account: Account) -> bool:
        # TODO: Test
        joins = self.ua.get_from_id_pair(user.id, account.id)
        if len(joins) == 0:
            raise ResourceNotFound(
                "This user / account pairing does not exist.")
        else:
            return self.a.delete(account)

    def deposit(self, user: User, account: Account,
                amount: float) -> Transaction:
        # TODO: Test
        # ! Check for invalid input
        tran = Transaction("default", account.id, user.id, account.id, amount,
                           "default")
        tran = self.t.create(tran)
        account.balance += amount
        self.a.update(account)
        return tran

    def withdraw(self, user: User, account: Account,
                 amount: float) -> Transaction:
        # TODO: Test
        # ! Check for invalid input
        tran = Transaction("default", account.id, user.id, account.id, -amount,
                           "default")
        tran = self.t.create(tran)
        account.balance -= amount
        self.a.update(account)
        return tran

    def transfer(self, user: User, account: Account, recipient: Account,
                 amount: float) -> Transaction:
        # TODO: Test
        # ! Check for invalid input
        tran = Transaction("default", account.id, user.id, recipient.id, amount,
                           "default")
        tran = self.t.create(tran)
        account.balance -= amount
        recipient.balance += amount
        self.a.update(account)
        self.a.update(recipient)
        return tran
