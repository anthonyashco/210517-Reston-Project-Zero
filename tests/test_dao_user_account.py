from daos.user_account_dao import UserAccountDAO as ua
from entities.user_account import UserAccount

join = UserAccount(0, 2, 2)


def test_create():
    global join
    count_1 = len(ua.get_all())
    join = ua.create(join)
    count_2 = len(ua.get_all())
    assert count_2 == count_1 + 1


def test_delete():
    global join
    count_1 = len(ua.get_all())
    ua.delete(join)
    count_2 = len(ua.get_all())
    assert count_2 == count_1 - 1


def test_get_all():
    joins = ua.get_all()
    assert type(joins[0]) == UserAccount
