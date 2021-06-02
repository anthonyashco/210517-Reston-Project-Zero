from services.banking import BankingService
from daos.account_dao import AccountDAO
from daos.transaction_dao import TransactionDAO
from daos.user_account_dao import UserAccountDAO
from daos.user_dao import UserDAO
from entities.account import Account

s = BankingService(AccountDAO, TransactionDAO, UserAccountDAO, UserDAO)

user = None
account = None


def test_create_user_inline():
    global user
    user = s.create_user_inline("pytest@email.com", "password", "Py", "Test",
                                "active")
    assert user.id != 0


def test_create_account():
    global account
    account = Account(None, "debit", 0.00)
    account = s.create_account(user, account)
    assert account.id is not None


def test_get_user_specific_account():
    get = s.get_user_specific_account(user.id, account.id)
    assert type(get) == Account


def test_update_user_specific_account():
    account.type = "credit"
    update = s.update_user_specific_account(user, account)
    assert update.type == "credit"


def test_deposit():
    tran = s.deposit(user, account, 10.00)
    s.delete_transaction(tran)
    assert tran.transfer_amount == 10.00


def test_withdraw():
    tran = s.withdraw(user, account, 10.00)
    s.delete_transaction(tran)
    assert tran.transfer_amount == -10.00


def test_delete_user_specific_account():
    delete = s.delete_user_specific_account(user, account)
    assert delete is True


def test_delete_user():
    delete_user = s.delete_user(user)
    assert delete_user is True
