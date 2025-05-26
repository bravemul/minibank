"""
接口路由模块。
负责将 HTTP 请求路由到对应的业务处理函数，实现 RESTful API。
"""

from flask import Blueprint, request, jsonify
from .services import (
    register_user, get_account_info, deposit, withdraw, transfer, 
    get_transactions, reconcile_account
)

# 创建一个 Blueprint 对象，方便模块化管理路由
bp = Blueprint('api', __name__)

@bp.route('/accounts/register', methods=['POST'])
def register():
    """
    注册新用户并开户。
    请求体需包含 username 和 password 字段。
    """
    data = request.json
    return register_user(data)

@bp.route('/accounts/<int:account_id>', methods=['GET'])
def account_info(account_id):
    """
    查询指定账户的基本信息。
    """
    return get_account_info(account_id)

@bp.route('/accounts/<int:account_id>/deposit', methods=['POST'])
def deposit_route(account_id):
    """
    向指定账户存款。
    请求体需包含 amount 字段。
    """
    data = request.json
    return deposit(account_id, data)

@bp.route('/accounts/<int:account_id>/withdraw', methods=['POST'])
def withdraw_route(account_id):
    """
    从指定账户取款。
    请求体需包含 amount 字段。
    """
    data = request.json
    return withdraw(account_id, data)

@bp.route('/accounts/transfer', methods=['POST'])
def transfer_route():
    """
    账户间转账。
    请求体需包含 from_account、to_account、amount 字段。
    """
    data = request.json
    return transfer(data)

@bp.route('/accounts/<int:account_id>/transactions', methods=['GET'])
def transactions_route(account_id):
    """
    查询指定账户的所有交易流水。
    """
    return get_transactions(account_id)

@bp.route('/accounts/<int:account_id>/reconcile', methods=['GET'])
def reconcile_route(account_id):
    """
    对账户进行对账检查。
    """
    return reconcile_account(account_id)
@bp.route('/', methods=['GET'])
def welcome():
    return "Welcome to MiniBank API! Visit /api/ for API endpoints."