from typing import List
from entities.account import Account
from entities.user import User
from utils.connect import Connection

conn = Connection.conn


class AccountDAO():

    def create(account: Account) -> Account:
        smt = "INSERT INTO piggybank.accounts VALUES (DEFAULT, %s, %s) RETURNING id"
        cursor = conn.cursor()
        cursor.execute(smt, [account.type, account.balance])
        account.id = cursor.fetchone()[0]

        return account

    def get(account_id: int) -> Account:
        smt = "SELECT * FROM piggybank.accounts WHERE id = %s"
        cursor = conn.cursor()
        cursor.execute(smt, [account_id])
        records = cursor.fetchall()

        accounts = []
        for account in records:
            account = Account(account[0], account[1], account[2])
            accounts.append(account)

        return accounts[0]

    def get_from_user(user: User) -> List[Account]:
        join_smt = "SELECT account_id FROM piggybank.user_accounts WHERE user_id=%s"
        cursor = conn.cursor()
        cursor.execute(join_smt, [user.id])
        records = cursor.fetchall()

        account_ids = [account_id for account_id in records]
        accounts = []
        acc_smt = "SELECT * FROM piggybank.accounts WHERE id = %s"

        for account_id in account_ids:
            cursor.execute(acc_smt, [account_id])
            record = cursor.fetchone()
            account = Account(record[0], record[1], record[2])
            accounts.append(account)

        return accounts

    def get_all() -> List[Account]:
        smt = "SELECT * FROM piggybank.accounts"
        cursor = conn.cursor()
        cursor.execute(smt)
        records = cursor.fetchall()

        accounts = []
        for account in records:
            account = Account(account[0], account[1], account[2])
            accounts.append(account)

        return accounts

    def update(account: Account) -> Account:
        smt = "UPDATE piggybank.accounts SET account_type=%s, balance=%s WHERE id=%s"
        cursor = conn.cursor()
        cursor.execute(smt, [account.type, account.balance, account.id])

        return account

    def delete(account: Account) -> bool:
        smt = "DELETE FROM piggybank.accounts WHERE id=%s"
        cursor = conn.cursor()
        cursor.execute(smt, [account.id])

        return True
