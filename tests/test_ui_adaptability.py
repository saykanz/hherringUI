import pytest
import allure
from utils.logger import logger

@allure.feature("UI界面测试")
class TestUILayoutAndStyle:

    # ==================== 1. 跨浏览器兼容性 ====================
    @allure.story("跨浏览器兼容性")
    def test_cross_browser_compatibility(self, puzzle_page, browser_name):
        """验证同一套代码在不同浏览器下表现一致"""
        with allure.step(f"【{browser_name.upper()}】浏览器 - 验证首页核心元素"):
            puzzle_page.load_home()
            puzzle_page.verify_element_adaptability(
                puzzle_page.get_puzzle_card("看图推‘树’1"), "谜题卡片"
            )
            assert puzzle_page.get_by_text("立即挑战").first.is_visible()
            puzzle_page.screenshot(f"cross_browser_{browser_name}")


    # ==================== 2. 响应式设计 + 分辨率适配 ====================
    @allure.story("响应式设计与分辨率适配")
    @pytest.mark.parametrize("viewport_config", [
        {"name": "Desktop_1920", "width": 1920, "height": 1080},
        {"name": "Tablet", "width": 768, "height": 1024},
        {"name": "Mobile", "width": 375, "height": 667},
    ], ids=lambda x: x["name"])
    def test_responsive_design(self, puzzle_page, responsive_page, viewport_config):
        """不同屏幕尺寸下的布局适配验证"""
        with allure.step(f"视口 {viewport_config['name']} ({viewport_config['width']}×{viewport_config['height']})"):
            puzzle_page.load_home()

            card = puzzle_page.get_puzzle_card("五脏：民以食为天")
            puzzle_page.verify_element_adaptability(card, "谜题卡片")

            # 移动端特殊检查
            if viewport_config["width"] < 768:
                with allure.step("移动端布局检查"):
                    assert puzzle_page.page.get_by_text("立即挑战").count() > 0

            puzzle_page.screenshot(f"responsive_{viewport_config['name']}")


    # ==================== 3. 界面布局和样式测试 ====================
    @allure.story("元素排列与间距验证")
    def test_element_alignment(self, puzzle_page):
        """验证按钮、卡片等元素的排列和间距是否规范"""
        puzzle_page.load_home()
        puzzle_page.verify_element_alignment("text=立即挑战", "立即挑战按钮", expected_margin=0)


    @allure.story("字体、字号和颜色验证")
    def test_text_style(self, puzzle_page):
        """验证关键文本的样式是否符合设计要求"""
        puzzle_page.load_home()

        puzzle_page.verify_text_style(
            "text=今日挑战等你来解",
            "首页标题",
            expected_font_size=14.0
        )

        puzzle_page.verify_text_style(
            "text=看图推‘树’1",
            "谜题名称",
            expected_font_size=0
        )


    @allure.story("图标和图片加载验证")
    def test_images_and_icons(self, puzzle_page):
        """验证图片和图标是否正常显示无破损"""
        puzzle_page.load_home()
        puzzle_page.verify_image_loaded("text=立即挑战", "挑战按钮区域")

        # 检查破损图片数量
        broken_count = puzzle_page.page.locator("img").evaluate_all(
            """imgs => imgs.filter(img => img.complete === false || img.naturalWidth === 0).length"""
        )
        assert broken_count == 0, f"发现 {broken_count} 张破损图片"


    @allure.story("CSS样式表加载验证")
    def test_css_loading(self, puzzle_page):
        """验证页面样式是否正确加载"""
        puzzle_page.load_home()

        font_family = puzzle_page.page.evaluate("() => getComputedStyle(document.body).fontFamily")
        assert any(x in font_family for x in ["sans-serif", "微软雅黑", "Arial", "Helvetica"]), \
            "页面字体样式未正确加载"

        puzzle_page.screenshot("css_style_verification")