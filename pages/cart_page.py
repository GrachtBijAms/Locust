from .base_page import BasePage


class CartPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.cart_list = page.locator(".cart_list")

    async def wait_until_loaded(self):
        await self.cart_list.wait_for(timeout=10000)
