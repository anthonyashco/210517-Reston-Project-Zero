from daos.transaction_dao import TransactionDAO as t
from entities.transaction import Transaction

tran = Transaction(0, 1, 3, 2, 1.00, None)


def test_create():
    global tran
    count_1 = len(t.get_all())
    tran = t.create(tran)
    count_2 = len(t.get_all())
    assert count_2 == count_1 + 1


def test_delete():
    global tran
    count_1 = len(t.get_all())
    t.delete(tran)
    count_2 = len(t.get_all())
    assert count_2 == count_1 - 1


def test_get_all():
    trans = t.get_all()
    assert type(trans[0]) == Transaction
