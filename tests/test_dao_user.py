from daos.account_dao import AccountDAO as a
from daos.user_dao import UserDAO as u
from entities.user import User

user = User(0, "test@fake.email", "153417bd132637ba71cf236c323a55bd",
            "71a8b28bf9986f51ab5e31c1c20993f3", "Testy", "McTestFace", "active")


def test_create():
    global user
    count_1 = len(u.get_all())
    user = u.create(user)
    count_2 = len(u.get_all())
    assert count_2 == count_1 + 1


def test_update():
    global user
    user.status = "closed"
    u.update(user)
    account_2 = u.get(user.id)
    assert account_2.status == "closed"


def test_delete():
    global user
    count_1 = len(u.get_all())
    u.delete(user)
    count_2 = len(u.get_all())
    assert count_2 == count_1 - 1


def test_from_account():
    account = a.get(1)
    users = u.get_from_account(account)
    assert type(users[0]) == User
