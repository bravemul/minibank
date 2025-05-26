
"""
数据模型定义模块。
定义 User（用户）、Account（账户）、Transaction（交易流水）三大数据表结构。
"""

from .db import db
from datetime import datetime

class User(db.Model):
    """
    用户表模型。
    字段说明：
        - id: 用户唯一ID
        - username: 用户名（唯一）
        - password_hash: 加密后的密码
        - created_at: 注册时间
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Account(db.Model):
    """
    账户表模型。
    字段说明：
        - id: 账户唯一ID
        - user_id: 所属用户ID
        - balance: 账户余额
        - created_at: 开户时间
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    balance = db.Column(db.Float, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Transaction(db.Model):
    """
    交易流水表模型。
    字段说明：
        - id: 流水唯一ID
        - from_account: 转出账户ID（存款时为None）
        - to_account: 转入账户ID（取款时为None）
        - amount: 交易金额
        - type: 交易类型（deposit/withdraw/transfer）
        - timestamp: 交易时间
        - description: 交易描述
    """
    id = db.Column(db.Integer, primary_key=True)
    from_account = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=True)
    to_account = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=True)
    amount = db.Column(db.Float, nullable=False)
    type = db.Column(db.String(16))  # deposit, withdraw, transfer
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    description = db.Column(db.String(128), nullable=True)