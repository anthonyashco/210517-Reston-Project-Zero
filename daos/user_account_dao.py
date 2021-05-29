from entities.account import Account
from entities.user import User
from entities.user_account import UserAccount
from typing import List
from utils.connect import Connection

conn = Connection.conn


class UserAccountDAO():

    @staticmethod
    def create(ua: UserAccount) -> UserAccount:
        smt = """
            insert into
                piggybank.user_account
            values
                (default, %s, %s)
            returning
                id
        """
        cursor = conn.cursor()
        cursor.execute(smt, [ua.user_id, ua.account_id])
        conn.commit()
        ua.id = cursor.fetchone()[0]

        return ua

    @staticmethod
    def get(ua_id: int) -> UserAccount:
        smt = "select * from piggybank.user_account where id = %s"
        cursor = conn.cursor()
        cursor.execute(smt, [ua_id])
        records = cursor.fetchall()

        uas = [UserAccount(*record) for record in records]
        return uas[0]

    @staticmethod
    def get_from_user(user: User) -> List[UserAccount]:
        smt = """
            select
                ua.id, user_id, account_id
            from
                piggybank.user u
                inner join piggybank.user_account ua on u.id = user_id
            where
                u.id = %s
        """
        cursor = conn.cursor()
        cursor.execute(smt, [user.id])
        records = cursor.fetchall()

        uas = [UserAccount(*record) for record in records]
        return uas

    @staticmethod
    def get_from_account(account: Account) -> List[UserAccount]:
        smt = """
            select
                ua.id, user_id, account_id
            from
                piggybank.account a
                inner join piggybank.user_account ua on a.id = user_id
            where
                a.id = %s
        """
        cursor = conn.cursor()
        cursor.execute(smt, [account.id])
        records = cursor.fetchall()

        uas = [UserAccount(*record) for record in records]
        return uas

    @staticmethod
    def get_from_id_pair(u_id: int, a_id: int) -> List[UserAccount]:
        smt = """
            select
                id, user_id, account_id
            from
                piggybank.user_account
            where
                (user_id = %s and account_id = %s)
        """
        cursor = conn.cursor()
        cursor.execute(smt, [u_id, a_id])
        records = cursor.fetchall()

        uas = [UserAccount(*record) for record in records]
        return uas

    @staticmethod
    def get_all() -> List[UserAccount]:
        smt = "select * from piggybank.user_account"
        cursor = conn.cursor()
        cursor.execute(smt)
        records = cursor.fetchall()

        uas = [UserAccount(*record) for record in records]
        return uas

    @staticmethod
    def update(ua: UserAccount) -> UserAccount:
        smt = ("""
            update
                piggybank.user_account
            set
                user_id = %s,
                account_id = %s,
            where
                id=%s
        """)
        cursor = conn.cursor()
        cursor.execute(smt, [ua.user_id, ua.account_id])
        conn.commit()

        return ua

    @staticmethod
    def delete(ua: UserAccount) -> bool:
        smt = "delete from piggybank.transactions where id = %s"
        cursor = conn.cursor()
        cursor.execute(smt, [ua.id])
        conn.commit()

        return True
