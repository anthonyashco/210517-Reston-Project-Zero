from typing import List
from entities.account import Account
from entities.user import User
from utils.connect import Connection

conn = Connection.conn


class UserDAO():

    def create(user: User) -> User:
        smt = ("INSERT INTO piggybank.users VALUES " +
               "(DEFAULT, %s, %s, %s, %s, %s, %s) RETURNING id")
        cursor = conn.cursor()
        cursor.execute(smt, [
            user.email, user.pass_hash, user.pass_salt, user.first_name,
            user.last_name, user.status
        ])
        user.id = cursor.fetchone()[0]

        return user

    def get(user_id: int) -> User:
        smt = "SELECT * FROM piggybank.users WHERE id = %s"
        cursor = conn.cursor()
        cursor.execute(smt, [user_id])
        records = cursor.fetchall()

        users = []
        for user in records:
            user = User(user[0], user[1], user[2], user[3], user[4], user[5],
                        user[6])
            users.append(user)

        return users[0]

    def get_from_account(account: Account) -> List[User]:
        join_smt = "SELECT user_id FROM piggybank.user_accounts WHERE account_id=%s"
        cursor = conn.cursor()
        cursor.execute(join_smt, [account.id])
        records = cursor.fetchall()

        user_ids = [user_id for user_id in records]
        users = []
        usr_smt = "SELECT * FROM piggybank.users WHERE id = %s"

        for user_id in user_ids:
            cursor.execute(usr_smt, [user_id])
            record = cursor.fetchone()
            user = User(record[0], record[1], record[2], record[3], record[4],
                        record[5], record[6])
            users.append(user)

        return users

    def get_all() -> List[User]:
        smt = "SELECT * FROM piggybank.users"
        cursor = conn.cursor()
        cursor.execute(smt)
        records = cursor.fetchall()

        users = []
        for user in records:
            user = User(user[0], user[1], user[2], user[3], user[4], user[5],
                        user[6])
            users.append(user)

        return users

    def update(user: User) -> User:
        smt = (
            "UPDATE piggybank.users SET email=%s, pass_hash=%s, pass_salt=%s, "
            + "first_name=%s, last_name=%s, status=%s WHERE id=%s")
        cursor = conn.cursor()
        cursor.execute(smt, [
            user.email, user.pass_hash, user.pass_salt, user.first_name,
            user.last_name, user.status, user.id
        ])

        return user

    def delete(user: User) -> bool:
        smt = "DELETE FROM piggybank.users WHERE id=%s"
        cursor = conn.cursor()
        cursor.execute(smt, [user.id])

        return True
