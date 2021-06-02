from exceptions.resource_not_found import ResourceNotFound
from entities.user_account import UserAccount
from daos.account_dao import AccountDAO
from daos.transaction_dao import TransactionDAO
from daos.user_account_dao import UserAccountDAO
from daos.user_dao import UserDAO
from entities.account import Account
from entities.transaction import Transaction
from entities.user import User
from security.password import Password
from services.banking_int import BankingInterface
from typing import List


class BankingService(BankingInterface):

    def __init__(self, account_dao: AccountDAO, transaction_dao: TransactionDAO,
                 user_account_dao: UserAccountDAO, user_dao: UserDAO):
        self.a = account_dao
        self.t = transaction_dao
        self.ua = user_account_dao
        self.u = user_dao

    def login(self, email: str, password: str):
        user = self.u.get_from_email(email)
        return Password.check_pass(password, user.pass_hash, user.pass_salt)

    def create_user_inline(self, email: str, password: str, first_name: str,
                           last_name: str, status: str) -> User:
        pass_hash, pass_salt = Password.hash_griddle(password)
        return self.u.create(
            User(0, email, pass_hash, pass_salt, first_name, last_name, status))

    def create_user(self, user: User) -> User:
        return self.u.create(user)

    def get_user(self, user_id: int) -> User:
        return self.u.get(user_id)

    def get_users_from_account(self, account: Account) -> List[User]:
        return self.u.get_from_account(account)

    def get_users_from_account_id(self, account_id: int) -> List[User]:
        account = self.a.get(account_id)
        return self.u.get_from_account(account)

    def get_users(self) -> List[User]:
        return self.u.get_all()

    def get_user_from_email(self, email: str) -> User:
        return self.u.get_from_email(email)

    def update_user(self, user: User) -> User:
        return self.u.update(user)

    def delete_user(self, user: User) -> bool:
        return self.u.delete(user)

    def delete_user_from_id(self, user_id: int) -> bool:
        user = self.u.get(user_id)
        return self.u.delete(user)

    def create_account(self, user: User, account: Account) -> Account:
        account = self.a.create(account)
        join = UserAccount("default", user.id, account.id)
        self.ua.create(join)
        return account

    def get_account_from_id(self, account_id: int):
        return self.a.get(account_id)

    def get_accounts_from_user(self, user: User) -> List[Account]:
        return self.a.get_from_user(user)

    def get_accounts_from_range(self, above: int, below: int) -> List[Account]:
        accounts = self.a.get_all()
        return [
            account for account in accounts
            if account.id >= above and account.id <= below
        ]

    def get_user_specific_account(self, u_id: int, a_id: int) -> Account:
        joins = self.ua.get_from_id_pair(u_id, a_id)
        if len(joins) == 0:
            raise ResourceNotFound(
                "This user / account pairing does not exist.")
        else:
            return self.a.get(joins[0].account_id)

    def update_user_specific_account(self, user: User,
                                     account: Account) -> Account:
        joins = self.ua.get_from_id_pair(user.id, account.id)
        if len(joins) == 0:
            raise ResourceNotFound(
                "This user / account pairing does not exist.")
        else:
            return self.a.update(account)

    def delete_user_specific_account(self, user: User,
                                     account: Account) -> bool:
        joins = self.ua.get_from_id_pair(user.id, account.id)
        if len(joins) == 0:
            raise ResourceNotFound(
                "This user / account pairing does not exist.")
        else:
            self.ua.delete(joins[0])
            return self.a.delete(account)

    def delete_transaction(self, tran: Transaction) -> bool:
        return self.t.delete(tran)

    def deposit(self, user: User, account: Account,
                amount: float) -> Transaction:
        if amount <= 0:
            raise ValueError("Amount must be positive!")
        tran = Transaction("default", account.id, user.id, account.id, amount,
                           "default")
        tran = self.t.create(tran)
        account.balance += amount
        self.a.update(account)
        return tran

    def withdraw(self, user: User, account: Account,
                 amount: float) -> Transaction:
        if amount <= 0:
            raise ValueError("Amount must be positive!")
        tran = Transaction("default", account.id, user.id, account.id, -amount,
                           "default")
        tran = self.t.create(tran)
        account.balance -= amount
        self.a.update(account)
        return tran

    def transfer(self, user: User, account: Account, recipient: Account,
                 amount: float) -> Transaction:
        if amount <= 0:
            raise ValueError("Amount must be positive!")
        tran = Transaction("default", account.id, user.id, recipient.id, amount,
                           "default")
        tran = self.t.create(tran)
        account.balance -= amount
        recipient.balance += amount
        self.a.update(account)
        self.a.update(recipient)
        return tran

    def get_transactions_from_user(self, user: User) -> List[Transaction]:
        return self.t.get_from_user(user)
