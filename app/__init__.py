"""
应用初始化模块。
负责创建 Flask 应用对象，注册数据库和 API 路由蓝图。
"""

from flask import Flask
from .db import init_db
from .routes import bp as api_bp

def create_app():
    """
    创建 Flask app 并完成配置与初始化。

    Returns:
        Flask app 实例
    """
    app = Flask(__name__)
    # 配置密钥和数据库 URI
    app.config['SECRET_KEY'] = 'replace_this_with_a_random_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///minibank.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # 初始化数据库
    init_db(app)
    # 注册 API 路由蓝图，所有接口前缀为 /api
    app.register_blueprint(api_bp, url_prefix='/api')
    return app