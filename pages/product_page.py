from .base_page import BasePage


class ProductPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.product_detail = page.locator(".inventory_details_container")
        self.add_to_cart_button = page.locator(
            "button.btn_primary.btn_inventory, button[data-test^='add-to-cart']"
        )
        self.cart_badge = page.locator(".shopping_cart_badge")

    async def wait_until_loaded(self):
        await self.product_detail.wait_for(timeout=10000)

    async def add_to_cart(self):
        await self.add_to_cart_button.click()
        await self.cart_badge.wait_for(timeout=5000)
