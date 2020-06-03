# -*- coding: utf-8 -*-
"""
@Author : Shimon.Zhang
@Date   : 2020/6/3 16:03
@Desc   : 创建数据库实例
"""
import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    # 用于每次创建数据库操作对象
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    # 用于关闭数据库操作对象
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()
    # 打开sql文件执行里面的sql语句
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
@with_appcontext
def init_db_command():
    """清空存在的表，创建新表操作"""
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    # app执行完毕任务之后，关闭db对象
    app.teardown_appcontext(close_db)
    # 吧init-db命令注册到app当中
    app.cli.add_command(init_db_command)
