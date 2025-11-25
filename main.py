# main.py
import user_auth

def main():
    # 初始化数据库（程序启动时执行一次）
    user_auth.init_db()
    
    current_user = None  # 记录当前登录用户

    while True:
        print("\n===== 电商平台客服系统 =====")
        if current_user is None:
            # 未登录状态：显示注册/登录选项
            print("1. 注册新用户")
            print("2. 用户登录")
            print("3. 退出程序")
        else:
            # 已登录状态：显示后续功能（如客服机器人交互）
            print(f"当前用户：{current_user}")
            print("1. 与客服机器人交流")
            print("2. 退出登录")
            print("3. 退出程序")

        choice = input("请选择操作: ").strip()

        # 未登录状态处理
        if current_user is None:
            if choice == "1":
                user_auth.register()
            elif choice == "2":
                current_user = user_auth.login()  # 登录成功后记录用户名
            elif choice == "3":
                print("感谢使用，再见！")
                break
            else:
                print("无效的选择，请重新输入。")
        # 已登录状态处理
        else:
            if choice == "1":
                # 调用客服机器人交互逻辑（后续可扩展）
                print("\n===== 客服机器人 =====")
                print(f"客服机器人：欢迎你，{current_user}！有什么可以帮你的吗？")
                # 此处可添加更多对话逻辑
            elif choice == "2":
                current_user = None
                print("已退出登录。")
            elif choice == "3":
                print("感谢使用，再见！")
                break
            else:
                print("无效的选择，请重新输入。")

if __name__ == "__main__":
    main()