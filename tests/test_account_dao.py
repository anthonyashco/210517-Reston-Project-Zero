from daos.account_dao import AccountDAO as a
from daos.user_dao import UserDAO as u
from entities.account import Account

account = Account(0, "debit", 0.00)


def test_create():
    global account
    count_1 = len(a.get_all())
    account = a.create(account)
    count_2 = len(a.get_all())
    assert count_2 == count_1 + 1


def test_update():
    global account
    account.balance += 10.50
    a.update(account)
    account_2 = a.get(account.id)
    assert account_2.balance == 10.50


def test_delete():
    global account
    count_1 = len(a.get_all())
    a.delete(account)
    count_2 = len(a.get_all())
    assert count_2 == count_1 - 1


def test_from_user():
    user = u.get(3)
    accounts = a.get_from_user(user)
    assert type(accounts[0]) == Account
