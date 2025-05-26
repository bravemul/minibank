"""
应用主入口。
用于启动 Flask 应用服务器。
"""

from app import create_app

# 创建 Flask app 实例
app = create_app()

if __name__ == "__main__":
    # 启动开发服务器，debug 模式方便调试
    app.run(debug=True)