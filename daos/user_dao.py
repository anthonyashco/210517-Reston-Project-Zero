from entities.account import Account
from entities.user import User
from typing import List
from utils.connect import Connection

conn = Connection.conn


class UserDAO():

    @staticmethod
    def create(user: User) -> User:
        smt = """
            insert into
                piggybank.user
            values
                (default, %s, %s, %s, %s, %s, %s)
            returning
                id
        """
        cursor = conn.cursor()
        cursor.execute(smt, [
            user.email, user.pass_hash, user.pass_salt, user.first_name,
            user.last_name, user.status
        ])
        conn.commit()
        user.id = cursor.fetchone()[0]

        return user

    @staticmethod
    def get(user_id: int) -> User:
        smt = "select * from piggybank.user where id = %s"
        cursor = conn.cursor()
        cursor.execute(smt, [user_id])
        records = cursor.fetchall()

        users = [User(*record) for record in records]
        return users[0]

    @staticmethod
    def get_from_email(email: str) -> User:
        smt = "select * from piggybank.user where email = %s"
        cursor = conn.cursor()
        cursor.execute(smt, [email])
        records = cursor.fetchall()

        users = [User(*record) for record in records]
        return users[0]

    @staticmethod
    def get_from_account(account: Account) -> List[User]:
        smt = """
            select
                u.id, email, pass_hash, pass_salt, first_name, last_name, status
            from
                piggybank.account a
                inner join piggybank.user_account ua on a.id = ua.account_id
                left join piggybank.user u on ua.user_id = u.id
            where
                a.id = %s
        """
        cursor = conn.cursor()
        cursor.execute(smt, [account.id])
        records = cursor.fetchall()

        users = [User(*record) for record in records]
        return users

    @staticmethod
    def get_all() -> List[User]:
        smt = "select * from piggybank.user"
        cursor = conn.cursor()
        cursor.execute(smt)
        records = cursor.fetchall()

        users = [User(*record) for record in records]
        return users

    @staticmethod
    def update(user: User) -> User:
        smt = """
            update
                piggybank.user
            set
                email = %s, pass_hash = %s, pass_salt = %s,
                first_name = %s, last_name = %s, status = %s
            where
                id = %s
        """
        cursor = conn.cursor()
        cursor.execute(smt, [
            user.email, user.pass_hash, user.pass_salt, user.first_name,
            user.last_name, user.status, user.id
        ])
        conn.commit()

        return user

    @staticmethod
    def delete(user: User) -> bool:
        smt = "delete from piggybank.user where id = %s"
        cursor = conn.cursor()
        cursor.execute(smt, [user.id])
        conn.commit()

        return True
