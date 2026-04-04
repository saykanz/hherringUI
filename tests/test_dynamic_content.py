import pytest
import allure
from utils.logger import logger


@allure.feature("动态内容和 Ajax 测试")
class TestDynamicContentAndAjax:

    @allure.story("动态数据加载验证")
    def test_dynamic_data_loading(self, puzzle_page):
        """验证页面能正确加载服务器返回的动态数据（如谜题列表、推荐内容等）"""
        with allure.step("加载首页并等待动态内容"):
            puzzle_page.load_home()

            # 等待谜题卡片等动态内容加载完成
            puzzle_page.verify_loading_state(
                loading_selector="[data-loading='true'], .loading, .skeleton",  # 根据实际页面调整
                content_selector="text=立即挑战",
                timeout=12000
            )

            # 验证动态加载的内容是否正确显示
            cards = puzzle_page.page.locator("text=立即挑战").all()
            assert len(cards) >= 3, f"动态加载的谜题卡片数量不足，实际只有 {len(cards)} 个"

            puzzle_page.screenshot("dynamic_content_loaded")

    @allure.story("AJAX 请求验证")
    def test_ajax_requests(self, puzzle_page):
        """验证异步请求是否成功发出并返回正确数据"""
        puzzle_page.load_home()

        # 根据 hherring.cn 实际接口特征调整 pattern（常见如 api、graphql、challenge 等）
        response_data = puzzle_page.wait_for_dynamic_content(
            url_pattern="api|challenge|list|content",  # 关键词匹配，根据实际接口修改
            timeout=8000
        )

        # 如果能拿到 JSON 数据，可做更深入断言
        if response_data and isinstance(response_data, dict):
            assert "data" in response_data or "list" in response_data or len(response_data) > 0, \
                "AJAX 返回数据结构不符合预期"

    @allure.story("加载状态与进度条验证")
    def test_loading_indicator(self, puzzle_page):
        """重点验证加载中 → 加载完成 的用户体验流程"""
        puzzle_page.load_home()

        # 验证加载指示器出现和消失的完整过程
        puzzle_page.verify_loading_state(
            loading_selector=".loading-spinner, .ant-spin, [role='status']",  # 适配常见 loading 元素
            content_selector="text=今日挑战等你来解",
            timeout=10000
        )

        # 额外验证：加载完成后，loading 元素不应再可见
        loading_elements = puzzle_page.page.locator(".loading, .skeleton, .spin").all()
        visible_loadings = [el for el in loading_elements if el.is_visible()]
        assert len(visible_loadings) == 0, f"加载完成后仍有 {len(visible_loadings)} 个 loading 元素未隐藏"

    @allure.story("网络请求监控（调试辅助）")
    def test_network_monitor(self, puzzle_page):
        """监控页面发出的所有网络请求，便于排查问题"""
        puzzle_page.load_home()

        # 监听包含特定关键词的请求
        requests = puzzle_page.monitor_network_requests(["api", "challenge", "static"])

        # 等待页面加载完成
        self.page.wait_for_load_state("networkidle")

        assert len(requests) > 0, "页面未发出任何网络请求"
        self.logger.info(f"页面共发出 {len(requests)} 个被监控的网络请求")