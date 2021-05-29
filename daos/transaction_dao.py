from entities.account import Account
from entities.transaction import Transaction
from entities.user import User
from typing import List
from utils.connect import Connection

conn = Connection.conn


class TransactionDAO():

    @staticmethod
    def create(tran: Transaction) -> Transaction:
        smt = """
            insert into
                piggybank.transaction
            values
                (default, %s, %s, %s, %s, default)
            returning
                id, transaction_time
        """
        cursor = conn.cursor()
        cursor.execute(smt, [
            tran.source_account_id, tran.source_user_id, tran.transfer_amount,
            tran.destination_account_id
        ])
        conn.commit()
        result = cursor.fetchone()
        tran.id = result[0]
        tran.transaction_time = result[1]

        return tran

    @staticmethod
    def get(tran_id: int) -> Transaction:
        smt = "select * from piggybank.transaction where id = %s"
        cursor = conn.cursor()
        cursor.execute(smt, [tran_id])
        records = cursor.fetchall()

        trans = [Transaction(*record) for record in records]
        return trans[0]

    @staticmethod
    def get_from_user(user: User) -> List[Transaction]:
        smt = """
            select
                t.id, source_account_id, source_user_id, transfer_amount,
                destination_account_id, transaction_time
            from
                piggybank.user u
                inner join piggybank.transaction t on u.id = source_user_id
            where
                u.id = %s"""
        cursor = conn.cursor()
        cursor.execute(smt, [user.id])
        records = cursor.fetchall()

        trans = [Transaction(*record) for record in records]
        return trans

    @staticmethod
    def get_from_account(account: Account) -> List[Transaction]:
        smt = """
            select
                t.id, source_account_id, source_user_id, transfer_amount,
                destination_account_id, transaction_time
            from
                piggybank.account a
                inner join piggybank.transaction t on a.id = source_account_id
            where
                a.id = %s"""
        cursor = conn.cursor()
        cursor.execute(smt, [account.id])
        records = cursor.fetchall()

        trans = [Transaction(*record) for record in records]
        return trans

    @staticmethod
    def get_all() -> List[Transaction]:
        smt = "select * from piggybank.transaction"
        cursor = conn.cursor()
        cursor.execute(smt)
        records = cursor.fetchall()

        trans = [Transaction(*record) for record in records]
        return trans

    @staticmethod
    def update(tran: Transaction) -> Transaction:
        smt = ("""
            update
                piggybank.transaction
            set
                source_account_id = %s,
                source_user_id = %s,
                transfer_amount = %s,
                destination_account_id = %s,
                transaction_time = %s
            where
                id = %s
        """)
        cursor = conn.cursor()
        cursor.execute(smt, [
            tran.source_account_id, tran.source_user_id, tran.transfer_amount,
            tran.destination_account_id, tran.transaction_time
        ])
        conn.commit()

        return tran

    @staticmethod
    def delete(tran: Transaction) -> bool:
        smt = "delete from piggybank.transaction where id = %s"
        cursor = conn.cursor()
        cursor.execute(smt, [tran.id])
        conn.commit()

        return True
