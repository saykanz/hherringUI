import pytest
import allure
import json
from utils.logger import logger

@allure.feature("性能测试（企业推荐方案）")
class TestPerformance:

    @allure.story("页面加载速度 & Web Vitals")
    @pytest.mark.performance
    def test_page_load_performance(self, puzzle_page):
        """企业最常用：测量加载时间 + Web Vitals（FCP / LCP）"""
        with allure.step("导航到首页并测量性能"):
            puzzle_page.load_home()
            metrics = puzzle_page.measure_page_performance(max_load_time_ms=6000)  # 根据 hherring.cn 实际情况调整

        # 可设置性能预算断言
        assert metrics["firstContentfulPaint"] < 2000, "FCP 超过 2 秒，影响用户感知"


    @allure.story("资源加载性能验证")
    @pytest.mark.performance
    def test_resource_loading(self, puzzle_page):
        """验证多媒体资源加载是否正常且快速"""
        puzzle_page.load_home()
        resources = puzzle_page.verify_resource_performance()

        # 可重点检查图片加载
        images = [r for r in resources if r["type"] == "img"]
        assert len(images) >= 2, "首页图片资源过少"


    @allure.story("轻量级并发访问模拟（企业常用）")
    @pytest.mark.parametrize("user_count", [3, 5])
    def test_concurrent_users(self, user_count, puzzle_page):
        """模拟多个用户同时访问，验证页面稳定性（非重度负载）"""
        with allure.step(f"模拟 {user_count} 个并发用户访问"):
            contexts = []
            try:
                for i in range(user_count):
                    context = puzzle_page.page.context.browser.new_context()
                    page = context.new_page()
                    page.goto(puzzle_page.page.url, wait_until="load")
                    assert page.locator("text=立即挑战").is_visible(timeout=8000), \
                        f"用户 {i+1} 未正常加载挑战按钮"
                    contexts.append(context)
                    logger.info(f"并发用户 {i+1} 访问成功")
            finally:
                for ctx in contexts:
                    ctx.close()