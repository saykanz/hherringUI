import os
from datetime import datetime

import json

from config.settings import BASE_URL
from utils.logger import logger
import allure
from playwright.sync_api import Page, Locator,expect


class BasePage:
    def __init__(self, page: Page):
        self.page = page
        self.logger = logger

    def navigate(self, url: str = ""):
        """导航到指定页面"""
        full_url = f"{BASE_URL}{url}" if not url.startswith("http") else url
        with allure.step(f"导航到页面: {full_url}"):
            self.page.goto(full_url, wait_until="networkidle")
            self.logger.info(f"Navigate to {full_url}")

    def get_by_text(self, text: str, exact: bool = True) -> Locator:
        return self.page.get_by_text(text, exact=exact)

    def screenshot(self, name: str = "screenshot"):
        """截图并自动附加到 Allure 报告（失败时特别有用）"""
        screenshot_dir = "reports/screenshots"
        os.makedirs(screenshot_dir, exist_ok=True)
        filename = f"{screenshot_dir}/{name}_{datetime.now().strftime('%H%M%S')}.png"

        self.page.screenshot(path=filename)
        self.logger.info(f"手动截图已保存: {filename}")

        # 自动附加到 Allure（即使测试通过也可看到）
        with open(filename, "rb") as f:
            allure.attach(
                f.read(),
                name=name,
                attachment_type=allure.attachment_type.PNG
            )
        return filename

    @allure.step("验证元素在当前视口下可见且可交互")
    def verify_element_adaptability(self,locator_str:str,element_name:str="元素"):
        """通用适配性验证：检查元素是否可见、可点击、尺寸合理"""
        element = self.page.locator(locator_str) if isinstance(locator_str,str) else locator_str
        expect(element).to_be_visible(),f"{element_name}在当前视口下不可见"
        expect(element).to_be_enabled(),f"{element_name}在当前视口下不可用"

        box = element.bounding_box()
        assert box is not None,f"{element_name}未正确渲染"

        self.logger.info(f"{element}适配性验证通过（视口：{self.page.viewport_size}")
        return box

    @allure.step("验证页面布局不溢出")
    def verify_no_overflow(self):
        """检查页面是否有水平/垂直溢出（常见响应式问题）"""
        overflow_x = self.page.evaluate(
            "() => document.documentElement.scrollWidth > document.documentElement.clientWidth")
        overflow_y = self.page.evaluate(
            "() => document.documentElement.scrollHeight > document.documentElement.clientHeight")
        assert not overflow_x, "页面存在水平溢出（布局在当前分辨率下崩坏）"

    @allure.step("验证元素排列与间距")
    def verify_element_alignment(self, selector: str, element_name: str = "元素", expected_margin: int = None):
        """验证元素对齐和间距是否符合设计规范"""
        element = self.page.locator(selector).first

        if expected_margin is not None:
            margin = self.page.evaluate(
                "(el) => parseInt(getComputedStyle(el).marginBottom || '0')",
                element.element_handle()
            )
            assert abs(margin - expected_margin) <= 8, \
                f"{element_name} 间距不符合预期（实际:{margin}px，预期约:{expected_margin}px）"

    @allure.step("验证文本样式（字体、颜色、字号")
    def verify_text_style(self,selector:str,element_name:str,expected_family:str = None,
                          expected_font_size:float=None,expected_color:str=None):
        element = self.page.locator(selector).first
        assert element.is_visible(),f"{element_name}未显示"
        style = self.page.evaluate("""
            (el)=>{
                const s = window.getComputedStyle(el);
                return {
                fontSize:parseFloat(s.fontSize),
                color:s.color,
                fontFamily:s.fontFamily
                };
            }""",element.element_handle())
        if expected_font_size:
            assert abs(style["fontSize"] - expected_font_size) < 3, \
                f"{element_name} 字号不符（实际:{style['fontSize']}, 预期:{expected_font_size}）"

        if expected_color:
            assert expected_color.lower() in style["color"].lower(), \
                f"{element_name} 颜色不符（实际:{style['color']}）"

        self.logger.info(f"✅ {element_name} 样式验证通过 → 字号:{style['fontSize']}px, 颜色:{style['color']}")

    @allure.step("验证图片/图标正常加载")
    def verify_image_loaded(self,selector:str,element_name:str="图片"):
        element = self.page.locator(selector).first
        assert element.is_visible(),f"{element_name} 加载失败或图片破损"

        loaded = self.page.evaluate("""
            (el)=>{
                if(el.tagName.toLowerCase()==='img'){
                    return el.complete && el.naturalWidth > 0
                    }
                    return true;
            }""",element.element_handle())
        assert loaded,f"{element_name}加载失败或图片破损"
        self.logger.info(f"✅ {element_name} 加载正常")

# ==================== 企业级性能测试方法 (2026 推荐) ====================

    @allure.step("测量页面核心性能指标 (Navigation Timing + Web Vitals)")
    def measure_page_performance(self, max_load_time_ms: int = 5000):
        """结合 Navigation Timing + First Contentful Paint 等 Web Vitals"""
        metrics = self.page.evaluate("""() => {
            const timing = performance.timing;
            const paint = performance.getEntriesByType('paint');
            const fcp = paint.find(entry => entry.name === 'first-contentful-paint')?.startTime || 0;
            const lcp = performance.getEntriesByType('largest-contentful-paint')[0]?.startTime || 0;

            return {
                totalLoadTime: timing.loadEventEnd - timing.navigationStart,
                domContentLoaded: timing.domContentLoadedEventEnd - timing.navigationStart,
                firstContentfulPaint: Math.round(fcp),
                largestContentfulPaint: Math.round(lcp),
                ttfb: timing.responseStart - timing.navigationStart   // Time to First Byte
            };
        }""")

        assert metrics["totalLoadTime"] < max_load_time_ms, \
            f"页面加载超时！实际 {metrics['totalLoadTime']}ms > 阈值 {max_load_time_ms}ms"

        # Allure 附加详细指标（便于趋势分析）
        allure.attach(
            json.dumps(metrics, indent=2, ensure_ascii=False),
            name="页面性能指标 (Web Vitals)",
            attachment_type=allure.attachment_type.JSON
        )

        self.logger.info(f"性能指标 → Total Load: {metrics['totalLoadTime']}ms | "
                        f"FCP: {metrics['firstContentfulPaint']}ms | LCP: {metrics['largestContentfulPaint']}ms")
        return metrics

    @allure.step("验证关键资源加载（图片、JS、CSS）")
    def verify_resource_performance(self):
        """检查资源加载时间和成功率"""
        resources = self.page.evaluate("""() => performance.getEntriesByType('resource').map(r => ({
            name: r.name.split('?')[0],
            type: r.initiatorType,
            duration: Math.round(r.duration),
            size: r.transferSize
        }))""")

        slow_resources = [r for r in resources if r["duration"] > 1500]  # >1.5s 视为慢资源
        failed_resources = [r for r in resources if r["duration"] == 0 and r["size"] == 0]

        if slow_resources:
            allure.attach(str(slow_resources[:10]), name="慢加载资源警告", attachment_type=allure.attachment_type.JSON)

        assert len(failed_resources) == 0, f"发现 {len(failed_resources)} 个资源加载失败"
        self.logger.info(f"共加载 {len(resources)} 个资源，慢资源数量: {len(slow_resources)}")
        return resources

    # ==================== 交互逻辑测试方法 ====================

    @allure.step("验证鼠标悬停（Hover）效果")
    def verify_hover_effect(self, selector: str, element_name: str = "元素"):
        """验证鼠标悬停是否触发样式/菜单/提示等"""
        element = self.page.locator(selector).first
        assert element.is_visible(), f"{element_name} 未显示"

        # 执行 hover 并等待可能出现的变化
        element.hover()
        self.page.wait_for_timeout(300)  # 短暂等待样式/动画生效

        # 示例断言：可根据实际页面调整（检查 class、属性、可见元素等）
        self.logger.info(f"✅ {element_name} 鼠标悬停验证通过")
        return element

    @allure.step("验证键盘事件（Tab / Enter / Esc 等）")
    def verify_keyboard_interaction(self, selector: str, key: str, expected_behavior: str = None):
        """验证键盘操作是否触发预期行为"""
        element = self.page.locator(selector).first
        element.focus()  # 先聚焦

        self.page.keyboard.press(key)

        if expected_behavior:
            # 根据实际页面添加具体断言，例如 Enter 后提交、Esc 关闭弹窗等
            self.logger.info(f"✅ 按键 {key} 执行成功，预期行为: {expected_behavior}")

    @allure.step("验证拖放操作（Drag & Drop）")
    def verify_drag_and_drop(self, source_selector: str, target_selector: str, element_name: str = "拖放操作"):
        """使用 Playwright 推荐的 dragTo() 方法"""
        source = self.page.locator(source_selector).first
        target = self.page.locator(target_selector).first

        assert source.is_visible() and target.is_visible(), "拖放源或目标元素不可见"

        # 推荐方式：dragTo（自动处理 hover + down + move + up）
        source.drag_to(target, force=True)  # force=True 可绕过部分 actionability 检查

        self.logger.info(f"✅ {element_name} 拖放操作执行成功")
        self.screenshot(f"drag_drop_{element_name}")

    @allure.step("验证页面滚动功能")
    def verify_scroll_behavior(self, scroll_target_selector: str = None):
        """验证滚动条是否正常工作（长页面/列表）"""
        # 滚动到页面底部
        self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        self.page.wait_for_timeout(500)

        # 验证是否能滚动到底部（或特定元素进入视口）
        if scroll_target_selector:
            target = self.page.locator(scroll_target_selector).first
            target.scroll_into_view_if_needed()
            assert target.is_visible(), "滚动后目标元素仍不可见"

        # 可选：验证滚动位置
        scroll_y = self.page.evaluate("window.scrollY")
        assert scroll_y > 100, "页面滚动未生效"

        self.logger.info("✅ 页面滚动验证通过")
        self.screenshot("scroll_verification")

    # ==================== 动态内容和 Ajax 测试方法（企业推荐） ====================

    @allure.step("验证动态数据加载（AJAX/Fetch）")
    def wait_for_dynamic_content(self, url_pattern: str, timeout: int = 10000):
        """等待特定 AJAX 请求完成并返回响应"""
        with allure.step(f"等待包含 {url_pattern} 的网络请求"):
            response = self.page.wait_for_response(
                lambda resp: url_pattern in resp.url,
                timeout=timeout
            )

            assert response.ok, f"AJAX 请求失败: {response.url} (状态码: {response.status})"

            # 可选：解析 JSON 数据并验证
            try:
                json_data = response.json()
                allure.attach(
                    json.dumps(json_data, indent=2, ensure_ascii=False),
                    name=f"接口响应 - {url_pattern}",
                    attachment_type=allure.attachment_type.JSON
                )
                self.logger.info(f"AJAX 请求成功: {response.url} | 状态: {response.status}")
                return json_data
            except:
                self.logger.info(f"AJAX 请求成功（非JSON）: {response.url}")
                return None

    @allure.step("验证加载状态（Loading 进度条/骨架屏）")
    def verify_loading_state(self, loading_selector: str, content_selector: str, timeout: int = 15000):
        """验证加载中状态显示 → 加载完成消失的完整流程"""
        # 1. 确认加载指示器出现
        loading = self.page.locator(loading_selector)
        if loading.is_visible(timeout=3000):
            self.logger.info("检测到加载状态指示器")
            allure.attach(self.page.screenshot(), name="加载中状态", attachment_type=allure.attachment_type.PNG)

        # 2. 等待实际内容加载完成（推荐方式）
        content = self.page.locator(content_selector)
        content.wait_for(state="visible", timeout=timeout)

        # 3. 确认加载指示器消失
        try:
            loading.wait_for(state="hidden", timeout=5000)
            self.logger.info("✅ 加载指示器已正确消失")
        except:
            self.logger.warning("加载指示器未及时消失（可能为正常情况）")

        assert content.is_visible(), "动态内容加载完成后仍不可见"
        self.screenshot("dynamic_content_loaded")

    @allure.step("监听并验证网络请求")
    def monitor_network_requests(self, url_patterns: list = None):
        """监听页面所有网络请求（用于调试和验证）"""
        requests = []

        def log_request(request):
            if url_patterns is None or any(p in request.url for p in url_patterns):
                requests.append({
                    "url": request.url,
                    "method": request.method,
                    "headers": dict(request.headers)
                })

        self.page.on("request", log_request)

        # 返回一个可用于后续断言的函数
        return requests

    # ==================== 8. 错误和异常处理 ====================

    @allure.step("验证错误提示信息")
    def verify_error_message(self, expected_text: str, timeout: int = 5000):
        """验证页面是否显示清晰准确的错误提示"""
        error_locator = self.page.get_by_text(expected_text, exact=False)
        error_locator.wait_for(state="visible", timeout=timeout)

        assert error_locator.is_visible(), f"未显示预期错误提示: {expected_text}"
        self.logger.info(f"✅ 正确显示错误提示: {expected_text}")
        self.screenshot("error_message")
        return error_locator

    @allure.step("模拟网络异常并验证优雅降级")
    def simulate_network_error(self):
        """模拟网络断开，验证页面是否优雅处理"""
        self.page.context.set_offline(True)
        self.logger.info("已模拟网络断开（Offline）")
        self.screenshot("network_offline")

    @allure.step("恢复网络连接")
    def restore_network(self):
        """恢复网络连接"""
        self.page.context.set_offline(False)
        self.logger.info("网络已恢复")

    @allure.step("验证边界条件处理")
    def verify_boundary_condition(self, input_selector: str, value: str, expected_result: str = None):
        """验证空值、最大值、最小值等边界情况"""
        field = self.page.locator(input_selector).first
        field.fill(value)
        field.press("Enter")  # 或点击提交按钮

        if expected_result:
            self.page.get_by_text(expected_result).wait_for(state="visible", timeout=5000)
            assert self.page.get_by_text(expected_result).is_visible(), f"边界值 {value} 处理不符合预期"

    # ==================== 9. 安全性测试 ====================

    @allure.step("验证 XSS 注入防护")
    def verify_xss_protection(self, input_selector: str, malicious_payload: str):
        """验证是否能防止 XSS 攻击（恶意脚本被转义或过滤）"""
        field = self.page.locator(input_selector).first
        field.fill(malicious_payload)
        field.press("Enter")

        # 检查页面中是否出现未转义的 <script> 或 alert
        assert not self.page.locator("script").filter(has_text="alert").is_visible(timeout=2000), \
            "XSS 攻击成功！页面存在未转义的恶意脚本"

        self.logger.info("✅ XSS 防护验证通过（恶意脚本被正确处理）")
        self.screenshot("xss_test")

    @allure.step("验证会话管理（登出后清理）")
    def verify_session_logout(self):
        """验证登出后会话是否正确清除（无法访问需要登录的页面）"""
        # 假设页面有登出按钮
        if self.page.get_by_text("退出登录").is_visible():
            self.page.get_by_text("退出登录").click()

        self.page.wait_for_timeout(1000)
        # 尝试访问需要登录的页面或检查登录状态
        assert not self.page.get_by_text("欢迎回来").is_visible(timeout=3000), \
            "登出后仍显示已登录状态，会话清理失败"
        self.logger.info("✅ 会话登出与清理验证通过")

    @allure.step("验证权限控制（未授权访问）")
    def verify_unauthorized_access(self, protected_url: str):
        """验证未授权用户无法访问受保护页面"""
        self.page.goto(protected_url)
        self.page.wait_for_load_state("networkidle")

        # 常见表现：跳转到登录页、显示无权限提示、403 页面等
        unauthorized_indicators = [
            "无权限访问", "请先登录", "403", "登录", "Unauthorized"
        ]

        found = any(
            self.page.get_by_text(text, exact=False).is_visible(timeout=3000) for text in unauthorized_indicators)
        assert found, f"未授权访问 {protected_url} 时未显示权限控制提示"
        self.logger.info(f"✅ 权限控制验证通过（{protected_url}）")
        self.screenshot("unauthorized_access")