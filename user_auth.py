# user_auth.py
import sqlite3
import getpass

DB_FILE = 'users.db'

# 数据库初始化
def init_db():
    """初始化数据库，创建 users 表（如果不存在）"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
    ''')
    conn.commit()
    conn.close()

# 注册功能（仅业务逻辑，无菜单）
def register():
    username = input("请输入用户名: ").strip()
    if not username:
        print("用户名不能为空！")
        return False

    password = getpass.getpass("请输入密码: ")
    confirm_password = getpass.getpass("请确认密码: ")
    
    if password != confirm_password:
        print("两次输入的密码不一致！")
        return False

    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT username FROM users WHERE username = ?", (username,))
        if cursor.fetchone():
            print(f"错误：用户名 '{username}' 已被注册。")
            return False

        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        conn.commit()
        print(f"注册成功！欢迎你，{username}！")
        return True
    except sqlite3.Error as e:
        print(f"数据库错误：{e}")
        return False
    finally:
        if conn:
            conn.close()

# 登录功能（仅业务逻辑，返回用户名便于后续使用）
def login():
    username = input("请输入用户名: ").strip()
    password = getpass.getpass("请输入密码: ")

    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('SELECT password FROM users WHERE username = ?', (username,))
        user_data = cursor.fetchone()

        if not user_data:
            print("错误：用户名或密码不正确。")
            return None

        stored_password = user_data[0]
        if password == stored_password:
            print(f"登录成功！欢迎回来，{username}！")
            return username  # 登录成功返回用户名，用于后续交互
        else:
            print("错误：用户名或密码不正确。")
            return None
    except sqlite3.Error as e:
        print(f"数据库错误：{e}")
        return None
    finally:
        if conn:
            conn.close()