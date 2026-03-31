from .base_page import BasePage

class LoginPage(BasePage):
    def click_qq_login(self):
        self.page.get_by_text("QQ登录").click()

    # 如有普通账号登录可继续扩展