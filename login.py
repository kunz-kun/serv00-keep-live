# login.py (修复版)
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
        # 启动浏览器
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        try:
            # 1. 打开登录页面
            page.goto(url)
            
            # 2. 等待页面加载
            page.wait_for_load_state("networkidle")

            # 3. 填写表单
            print("正在输入账号密码...")
            page.fill('input[name="username"]', username)
            page.fill('input[name="password"]', password)

            # 4. 点击登录按钮 (修复点：增加 :visible 过滤器)
            # 原来的代码找到了两个按钮，其中一个是隐藏的。
            # 这里强制只点击可见的那个提交按钮。
            print("正在点击登录按钮...")
            page.click('button[type="submit"]:visible')
            
            # 5. 等待登录结果
            page.wait_for_timeout(5000) # 等待5秒让页面跳转
            
            title = page.title()
            print(f"当前页面标题: {title}")
            
            # 判断逻辑：只要不是 Login 页面，通常就是进去了
            if "Login" not in title: 
                 print("✅ 登录成功！")
            else:
                 print("⚠️ 标题未变，尝试截图保存...")
                 page.screenshot(path="error.png")

        except Exception as e:
            print(f"发生错误: {e}")
            # 出错时截图，方便在 Artifacts 里查看
            try:
                page.screenshot(path="debug_error.png")
            except:
                pass

        browser.close()

if __name__ == "__main__":
    run()
