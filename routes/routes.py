from exceptions.resource_not_found import ResourceNotFound
from daos.account_dao import AccountDAO
from daos.transaction_dao import TransactionDAO
from daos.user_account_dao import UserAccountDAO
from daos.user_dao import UserDAO
from entities.account import Account
from entities.user import User
from flask import Flask, request, jsonify
from psycopg2.errors import CheckViolation, ForeignKeyViolation
from services.banking import BankingService

s = BankingService(AccountDAO, TransactionDAO, UserAccountDAO, UserDAO)


def create_routes(app: Flask):

    @app.route("/")
    def hello():
        return "Hello world!", 200

    @app.route("/user", methods=["POST"])
    def create_user():
        """
        email: str,
        password: str,
        first_name: str,
        last_name: str,
        status: str
        """
        try:
            return s.create_user_inline(**request.json).to_json(), 201
        except Exception as e:
            print(e)
            return "This email is in use.", 200

    @app.route("/user", methods=["GET"])
    def get_users():
        user_id = request.args.get("id")
        email = request.args.get("email")
        account_id = request.args.get("account")
        try:
            if user_id is not None:
                return s.get_user(user_id).to_json(), 200
            elif email is not None:
                return s.get_user_from_email(email).to_json(), 200
            elif account_id is not None:
                return jsonify([
                    user.to_json()
                    for user in s.get_users_from_account_id(account_id)
                ]), 200
            else:
                return jsonify([user.to_json() for user in s.get_users()]), 200
        except ResourceNotFound as e:
            return str(e), 404

    @app.route("/user", methods=["PATCH"])
    def update_user():
        user = User.from_json(request.json)
        try:
            return s.update_user(user).to_json(), 200
        except ResourceNotFound as e:
            return str(e), 404
        except CheckViolation as e:
            return str(e), 422

    @app.route("/user", methods=["DELETE"])
    def delete_user():
        user = User.from_json(request.json)
        try:
            status = s.delete_user(user)
        except ForeignKeyViolation:
            return f"User {user.id} cannot be deleted.", 422
        if status:
            return f"User {user.id} deleted.", 205
        else:
            return f"User {user.id} not found.", 404

    @app.route("/user/<user_id>/account/<account_id>", methods=["GET"])
    def get_user_specific_account(user_id: str, account_id: str):
        return s.get_user_specific_account(int(user_id),
                                           int(account_id)).to_json(), 200

    @app.route("/user/<user_id>/account/<account_id>", methods=["PATCH"])
    def update_user_specific_account(user_id: str, account_id: str):
        body = request.json
        user = s.get_user(user_id)
        account = Account(**body)
        account.id = int(account_id)
        return s.update_user_specific_account(user, account).to_json(), 200

    @app.route("/user/<user_id>/account/<account_id>", methods=["DELETE"])
    def delete_user_specific_account(user_id: str, account_id: str):
        user = s.get_user(user_id)
        account = s.get_account_from_id(account_id)
        return s.delete_user_specific_account(user, account), 200

    @app.route("/user/<user_id>/account", methods=["GET"])
    def get_accounts_from_user(user_id: str):
        user = s.get_user(int(user_id))
        return jsonify([
            account.to_json() for account in s.get_accounts_from_user(user)
        ]), 200

    @app.route("/account", methods=["GET"])
    def get_accounts():
        account_id = request.args.get("id")
        above = request.args.get("above")
        below = request.args.get("below")

        if account_id is not None:
            return s.get_account_from_id(int(account_id)).to_json(), 200
        elif above is not None and below is not None:
            return jsonify([
                account.to_json() for account in s.get_accounts_from_range(
                    int(above), int(below))
            ]), 200

    @app.route("/account", methods=["POST"])
    def create_account():
        user_id = request.args.get("user")
        account_type = request.args.get("type")
        user = s.get_user(user_id)
        account = Account(None, account_type, 0.00)
        return s.create_account(user, account).to_json(), 201

    @app.route("/transaction", methods=["PATCH"])
    def transaction():
        body = request.json
        try:
            user = s.get_user(int(body["user"]))
            account = s.get_account_from_id(int(body["account"]))
        except ResourceNotFound as e:
            return str(e), 404
        if body["amount"] <= 0:
            return "Transfer amount must be positive.", 400
        try:
            if body["transaction"] == "deposit":
                return s.deposit(user, account,
                                 float(body["amount"])).to_json(), 200
            elif body["transaction"] == "withdraw":
                return s.withdraw(user, account,
                                  float(body["amount"])).to_json(), 200
            elif body["transaction"] == "transfer":
                recipient = s.get_account_from_id(int(body["recipient"]))
                return s.transfer(user, account, recipient,
                                  float(body["amount"])).to_json(), 200
        except CheckViolation:
            return f"Debit account {account.id} has insufficient funds.", 422
