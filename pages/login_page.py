from config.settings import BASE_URL
from .base_page import BasePage


class LoginPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.username_input = page.locator("#user-name")
        self.password_input = page.locator("#password")
        self.login_button = page.locator("#login-button")
        self.error_box = page.locator("[data-test='error']")

    async def open(self):
        await self.page.goto(BASE_URL, wait_until="domcontentloaded")
        await self.username_input.wait_for(timeout=10000)

    async def fill_credentials(self, username, password):
        await self.username_input.fill(username)
        await self.password_input.fill(password)

    async def submit(self):
        await self.login_button.click()

    async def wait_for_success(self):
        await self.page.wait_for_url("**/inventory.html", timeout=15000)

    async def get_error_text(self):
        if await self.error_box.is_visible():
            return await self.error_box.text_content()
        return None
