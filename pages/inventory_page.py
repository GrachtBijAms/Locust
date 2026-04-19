import random
from .base_page import BasePage


class InventoryPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.inventory_list = page.locator(".inventory_list")
        self.sort_dropdown = page.locator(".product_sort_container")
        self.inventory_items = page.locator(".inventory_item")
        self.item_names = page.locator(".inventory_item_name")
        self.cart_link = page.locator(".shopping_cart_link")
        self.menu_button = page.locator("#react-burger-menu-btn")
        self.logout_link = page.locator("#logout_sidebar_link")

    async def wait_until_loaded(self):
        await self.inventory_list.wait_for(timeout=10000)

    async def scroll_inventory(self):
        await self.page.evaluate("window.scrollTo(0, document.body.scrollHeight / 2)")

    async def sort_low_to_high(self):
        await self.sort_dropdown.select_option("lohi")
        await self.inventory_items.first.wait_for(timeout=5000)

    async def open_random_product(self):
        count = await self.item_names.count()
        idx = random.randint(0, count - 1)
        await self.item_names.nth(idx).click()

    async def open_cart(self):
        await self.cart_link.click()

    async def logout(self):
        await self.menu_button.click()
        await self.logout_link.wait_for(timeout=5000)
        await self.logout_link.click()
