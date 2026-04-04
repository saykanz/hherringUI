from page_objects.base_page import BasePage
from playwright.sync_api import expect
import allure


class LatestContent(BasePage):
    def __init__(self,page):
        super().__init__(page)

    @allure.step("加载首页")
    def load_home(self):
        self.navigate()

    def tab_switch(self, tab_name):
        tab = self.page.get_by_text(tab_name).first
        tab.click()
        expect(tab).to_have_class("active")

    def get_card(self, title):
        return self.page.locator(".content-card").filter(has_text=title)

    def click_card(self, title):
        card = self.get_card(title)
        expect(card).to_be_visible()
        card.click()
