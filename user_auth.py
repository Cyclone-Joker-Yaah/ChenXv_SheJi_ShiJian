import sqlite3
import getpass

# --- 配置 ---
DB_FILE = 'users.db'

# --- 数据库工具函数 ---

def init_db():
    """初始化数据库，创建 users 表（如果不存在）"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # 创建用户表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
    ''')
    
    conn.commit()
    conn.close()

# --- 核心功能函数 ---

def register():
    """用户注册功能"""
    username = input("请输入用户名: ").strip()
    if not username:
        print("用户名不能为空！")
        return

    password = getpass.getpass("请输入密码: ")
    confirm_password = getpass.getpass("请确认密码: ")
    
    if password != confirm_password:
        print("两次输入的密码不一致！")
        return

    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        # 检查用户名是否已存在
        cursor.execute("SELECT username FROM users WHERE username = ?", (username,))
        if cursor.fetchone():
            print(f"错误：用户名 '{username}' 已被注册。")
            return

        # 插入密码
        cursor.execute('''
        INSERT INTO users (username, password)
        VALUES (?, ?)
        ''', (username, password))

        conn.commit()
        print(f"注册成功！欢迎你，{username}！")

    except sqlite3.Error as e:
        print(f"数据库错误：{e}")
    finally:
        if conn:
            conn.close()

def login():
    """用户登录功能"""
    username = input("请输入用户名: ").strip()
    password = getpass.getpass("请输入密码: ")

    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        # 根据用户名查询用户信息
        cursor.execute('''
        SELECT password FROM users WHERE username = ?
        ''', (username,))
        
        user_data = cursor.fetchone()

        if not user_data:
            print("错误：用户名或密码不正确。")
            return False

        stored_password = user_data[0]

        # 直接比较明文密码
        if password == stored_password:
            print(f"登录成功！欢迎回来，{username}！")
            return True
        else:
            print("错误：用户名或密码不正确。")
            return False

    except sqlite3.Error as e:
        print(f"数据库错误：{e}")
        return False
    finally:
        if conn:
            conn.close()

# --- 主程序入口 ---

def main():
    """程序主菜单"""
    init_db() # 确保数据库和表已创建
    
    while True:
        print("\n===== 用户认证系统 =====")
        print("1. 注册新用户")
        print("2. 用户登录")
        print("3. 退出程序")
        
        choice = input("请选择操作: ").strip()
        
        if choice == "1":
            register()
        elif choice == "2":
            if login():
                print("\n你已成功进入系统。")
                break # 登录成功后退出循环
        elif choice == "3":
            print("感谢使用，再见！")
            break
        else:
            print("无效的选择。")

if __name__ == "__main__":
    main()