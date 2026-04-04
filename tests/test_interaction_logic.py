import pytest
import allure
from utils.logger import logger

@allure.feature("交互逻辑测试")
class TestInteractionLogic:

    @allure.story("鼠标事件验证（Hover、Click 等）")
    def test_mouse_interactions(self, puzzle_page):
        """验证鼠标悬停、点击等事件"""
        puzzle_page.load_home()

        with allure.step("验证谜题卡片鼠标悬停效果"):
            puzzle_page.verify_hover_effect("text=立即挑战", "挑战按钮")

        with allure.step("验证点击『立即挑战』按钮"):
            btn = puzzle_page.get_by_text("立即挑战", exact=True).first
            btn.click()
            # 根据实际页面添加断言，例如跳转或弹窗出现
            puzzle_page.screenshot("mouse_click")


    @allure.story("键盘事件验证（可访问性重点）")
    def test_keyboard_interactions(self, puzzle_page):
        """验证 Tab 导航、Enter、Esc 等键盘操作"""
        puzzle_page.load_home()

        with allure.step("Tab 键导航测试"):
            # 模拟 Tab 键多次，按需调整次数
            for _ in range(5):
                puzzle_page.page.keyboard.press("Tab")
            # 验证焦点是否正确（示例：最后一个可聚焦元素）
            puzzle_page.verify_keyboard_interaction("text=立即挑战", "Tab", "焦点移动")

        with allure.step("Enter 键触发操作"):
            puzzle_page.verify_keyboard_interaction("text=立即挑战", "Enter", "触发挑战")

        with allure.step("Esc 键关闭/取消（如果页面有弹窗）"):
            # 如果首页无弹窗，可在其他测试中验证
            puzzle_page.page.keyboard.press("Escape")


    @allure.story("拖放功能验证")
    def test_drag_and_drop(self, puzzle_page):
        """验证页面是否支持拖放操作（如果 hherring.cn 有排序/上传等功能）"""
        puzzle_page.load_home()

        # 注意：hherring.cn 当前可能没有明显拖放功能，可根据实际元素调整 selector
        # 示例（如果存在可拖拽的谜题卡片或文件上传区）：
        # puzzle_page.verify_drag_and_drop(
        #     source_selector="text=看图推‘树’1",
        #     target_selector=".drop-zone 或其他目标",
        #     element_name="谜题卡片拖放"
        # )

        # 如果当前页面无拖放，可标记为 skip 或仅验证相关区域
        pytest.skip("hherring.cn 当前页面暂无明显拖放功能，待功能上线后补充具体测试")


    @allure.story("滚动条与长页面滚动验证")
    def test_scroll_behavior(self, puzzle_page):
        """验证页面是否能正常滚动（尤其是长列表/文章页）"""
        puzzle_page.load_home()

        # 滚动测试
        puzzle_page.verify_scroll_behavior()

        # 可滚动到特定元素（例如页面底部的“查看更多”）
        puzzle_page.verify_scroll_behavior(scroll_target_selector="text=查看更多")