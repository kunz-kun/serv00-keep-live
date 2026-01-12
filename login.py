# login.py
import os
from playwright.sync_api import sync_playwright

def run():
    # 从 GitHub Secrets 获取环境变量
    url = os.environ.get("SERV00_URL")
    username = os.environ.get("SERV00_USER")
    password = os.environ.get("SERV00_PASS")

    if not url or not username or not password:
        print("错误：缺少必要的环境变量！")
        exit(1)

    print(f"正在尝试登录: {url}")

    with sync_playwright() as p:
        # 启动浏览器 (headless=True 表示不显示界面，在后台运行)
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # 1. 打开登录页面
        page.goto(url)
        
        # 2. 等待页面加载
        page.wait_for_load_state("networkidle")

        # 3. 填写表单 (Serv00 的输入框 name 通常是 username 和 password)
        # 如果报错找不到元素，可能是网页改版，需要检查 HTML
        print("正在输入账号密码...")
        page.fill('input[name="username"]', username)
        page.fill('input[name="password"]', password)

        # 4. 点击登录按钮
        # 尝试点击类型为 submit 的按钮
        page.click('button[type="submit"]')
        
        # 5. 等待登录结果
        # 通常登录成功后 URL 会变，或者出现 Logout 按钮
        try:
            # 等待 URL 发生变化或者出现特定元素
            page.wait_for_timeout(5000) # 等待5秒让页面跳转
            
            title = page.title()
            print(f"当前页面标题: {title}")
            
            if "Login" not in title and "DevilWEB" in title: 
                 print("✅ 登录成功！检测到进入了 Dashboard。")
            else:
                 # 截图保存以便调试 (GitHub Actions 里可以在 Artifacts 下载查看)
                 page.screenshot(path="error.png")
                 print("⚠️ 可能登录失败，已截图。请检查日志。")

        except Exception as e:
            print(f"发生错误: {e}")

        browser.close()

if __name__ == "__main__":
    run()
