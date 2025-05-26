"""
数据库初始化模块。
负责初始化 SQLAlchemy 数据库对象和与 Flask 应用的集成。
"""

from flask_sqlalchemy import SQLAlchemy

# 创建全局 SQLAlchemy 数据库实例
db = SQLAlchemy()

def init_db(app):
    """
    初始化数据库，将 db 与 Flask app 绑定，并创建所有表。

    Args:
        app (Flask): Flask app 实例
    """
    db.init_app(app)
    with app.app_context():
        db.create_all()