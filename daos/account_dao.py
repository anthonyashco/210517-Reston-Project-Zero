from entities.account import Account
from entities.user import User
from typing import List
from utils.connect import Connection

conn = Connection.conn


class AccountDAO():

    @staticmethod
    def create(account: Account) -> Account:
        smt = "insert into piggybank.account values (default, %s, %s) returning id"
        cursor = conn.cursor()
        cursor.execute(smt, [account.type, account.balance])
        conn.commit()
        account.id = cursor.fetchone()[0]

        return account

    @staticmethod
    def get(account_id: int) -> Account:
        smt = "select * from piggybank.account where id = %s"
        cursor = conn.cursor()
        cursor.execute(smt, [account_id])
        records = cursor.fetchall()

        accounts = [Account(*record) for record in records]
        return accounts[0]

    @staticmethod
    def get_from_user(user: User) -> List[Account]:
        smt = """
            select
                a.id, account_type, balance
            from
                piggybank.user u
                inner join piggybank.user_account ua on u.id = ua.user_id
                left join piggybank.account a on ua.account_id = a.id
            where
                u.id = %s
        """
        cursor = conn.cursor()
        cursor.execute(smt, [user.id])
        records = cursor.fetchall()

        accounts = [Account(*record) for record in records]
        return accounts

    @staticmethod
    def get_all() -> List[Account]:
        smt = "select * from piggybank.account"
        cursor = conn.cursor()
        cursor.execute(smt)
        records = cursor.fetchall()

        accounts = [Account(*record) for record in records]
        return accounts

    @staticmethod
    def update(account: Account) -> Account:
        smt = """
            update
                piggybank.account
            set
                account_type = %s, balance = %s
            where
                id = %s
        """
        cursor = conn.cursor()
        cursor.execute(smt, [account.type, account.balance, account.id])
        conn.commit()

        return account

    @staticmethod
    def delete(account: Account) -> bool:
        smt = "delete from piggybank.account where id = %s"
        cursor = conn.cursor()
        cursor.execute(smt, [account.id])
        conn.commit()

        return True
