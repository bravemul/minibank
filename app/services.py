"""
业务逻辑层模块。
实现所有账户操作、交易处理和对账等核心业务功能。
"""

from flask import jsonify
from .models import db, User, Account, Transaction
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

def register_user(data):
    """
    用户注册和开户逻辑。

    Args:
        data (dict): 包含 'username' 和 'password' 字段

    Returns:
        Flask Response: 注册结果，包含新建的用户ID和账户ID
    """
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'error': '用户名和密码必填'}), 400
    if User.query.filter_by(username=username).first():
        return jsonify({'error': '用户名已存在'}), 400

    # 创建新用户，并使用哈希安全方式保存密码
    user = User(username=username, password_hash=generate_password_hash(password))
    db.session.add(user)
    db.session.commit()
    # 为新用户自动创建一个账户
    account = Account(user_id=user.id, balance=0)
    db.session.add(account)
    db.session.commit()
    return jsonify({'message': '注册成功', 'user_id': user.id, 'account_id': account.id}), 201

def get_account_info(account_id):
    """
    查询账户基本信息。

    Args:
        account_id (int): 账户ID

    Returns:
        Flask Response: 账户信息（账户ID、用户名、余额、开户时间）
    """
    account = Account.query.get(account_id)
    if not account:
        return jsonify({'error': '账户不存在'}), 404
    user = User.query.get(account.user_id)
    return jsonify({
        'account_id': account.id,
        'username': user.username,
        'balance': account.balance,
        'created_at': account.created_at.isoformat()
    })

def deposit(account_id, data):
    """
    存款操作。

    Args:
        account_id (int): 目标账户ID
        data (dict): 包含 'amount' 字段

    Returns:
        Flask Response: 存款结果和当前余额
    """
    amount = data.get('amount')
    if amount is None or amount <= 0:
        return jsonify({'error': '存款金额需大于0'}), 400
    account = Account.query.get(account_id)
    if not account:
        return jsonify({'error': '账户不存在'}), 404

    # 更新账户余额，记录交易流水
    account.balance += amount
    txn = Transaction(
        from_account=None,
        to_account=account_id,
        amount=amount,
        type='deposit',
        description='存款'
    )
    db.session.add(txn)
    db.session.commit()
    return jsonify({'message': '存款成功', 'balance': account.balance})

def withdraw(account_id, data):
    """
    取款操作。

    Args:
        account_id (int): 目标账户ID
        data (dict): 包含 'amount' 字段

    Returns:
        Flask Response: 取款结果和当前余额
    """
    amount = data.get('amount')
    if amount is None or amount <= 0:
        return jsonify({'error': '取款金额需大于0'}), 400
    account = Account.query.get(account_id)
    if not account:
        return jsonify({'error': '账户不存在'}), 404
    if account.balance < amount:
        return jsonify({'error': '余额不足'}), 400

    # 更新账户余额，记录交易流水
    account.balance -= amount
    txn = Transaction(
        from_account=account_id,
        to_account=None,
        amount=amount,
        type='withdraw',
        description='取款'
    )
    db.session.add(txn)
    db.session.commit()
    return jsonify({'message': '取款成功', 'balance': account.balance})

def transfer(data):
    """
    转账操作。

    Args:
        data (dict): 包含 'from_account'、'to_account'、'amount' 字段

    Returns:
        Flask Response: 转账结果、转出与转入账户余额
    """
    from_id = data.get('from_account')
    to_id = data.get('to_account')
    amount = data.get('amount')
    if None in (from_id, to_id, amount):
        return jsonify({'error': '参数不全'}), 400
    if amount <= 0:
        return jsonify({'error': '转账金额需大于0'}), 400
    from_acct = Account.query.get(from_id)
    to_acct = Account.query.get(to_id)
    if not from_acct or not to_acct:
        return jsonify({'error': '账户不存在'}), 404
    if from_acct.balance < amount:
        return jsonify({'error': '余额不足'}), 400

    # 扣减转出账户余额，增加转入账户余额，记录交易流水
    from_acct.balance -= amount
    to_acct.balance += amount
    txn = Transaction(
        from_account=from_id,
        to_account=to_id,
        amount=amount,
        type='transfer',
        description='转账'
    )
    db.session.add(txn)
    db.session.commit()
    return jsonify({'message': '转账成功', 'from_balance': from_acct.balance, 'to_balance': to_acct.balance})

def get_transactions(account_id):
    """
    查询账户所有交易流水，按时间倒序排列。

    Args:
        account_id (int): 账户ID

    Returns:
        Flask Response: 交易流水列表
    """
    txns = Transaction.query.filter(
        ((Transaction.from_account == account_id) | (Transaction.to_account == account_id))
    ).order_by(Transaction.timestamp.desc()).all()
    txn_list = [
        {
            'id': txn.id,
            'type': txn.type,
            'amount': txn.amount,
            'from_account': txn.from_account,
            'to_account': txn.to_account,
            'timestamp': txn.timestamp.isoformat(),
            'description': txn.description
        } for txn in txns
    ]
    return jsonify(txn_list)

def reconcile_account(account_id):
    """
    对账功能：验证账户余额与流水记录的一致性。

    Args:
        account_id (int): 账户ID

    Returns:
        Flask Response: 记录余额、流水计算余额、是否一致
    """
    account = Account.query.get(account_id)
    if not account:
        return jsonify({'error': '账户不存在'}), 404
    txns = Transaction.query.filter(
        ((Transaction.from_account == account_id) | (Transaction.to_account == account_id))
    ).all()
    calculated = 0
    for txn in txns:
        if txn.type == 'deposit' and txn.to_account == account_id:
            calculated += txn.amount
        elif txn.type == 'withdraw' and txn.from_account == account_id:
            calculated -= txn.amount
        elif txn.type == 'transfer':
            if txn.from_account == account_id:
                calculated -= txn.amount
            if txn.to_account == account_id:
                calculated += txn.amount
    is_consistent = abs(account.balance - calculated) < 1e-6
    return jsonify({
        'account_id': account_id,
        'recorded_balance': account.balance,
        'calculated_balance': calculated,
        'is_consistent': is_consistent
    })