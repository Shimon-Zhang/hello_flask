# -*- coding: utf-8 -*-
"""
@Author : Shimon.Zhang
@Date   : 2020/6/3 15:33
@Desc   : 初始化工厂模式
"""
import os

from flask import Flask


def create_app(test_config=None):
    # 创建并且配置应用
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # 加载配置实例
        app.config.from_pyfile('config.py', silent=True)
    else:
        # 加载测试实例
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # 绑定一个简单的路由
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    # 将db操作注册到app当中
    from . import db
    db.init_app(app)

    # 导入认证模块
    from . import auth
    app.register_blueprint(auth.bp)

    return app
