import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from reporting.custom_report import collector

from locust import run_single_user, task, between
from locust_plugins.users.playwright import PlaywrightUser, pw, event
from config.settings import HEADLESS
from utils.helpers import get_random_user, think
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.product_page import ProductPage
from pages.cart_page import CartPage


class SauceDemoUser(PlaywrightUser):
    wait_time = between(2, 5)
    headless = HEADLESS

    @task
    @pw
    async def login_browse_and_cart(self, page):
        user = get_random_user()

        login_page = LoginPage(page)
        inventory_page = InventoryPage(page)
        product_page = ProductPage(page)
        cart_page = CartPage(page)

        async with event(self, "01 - Load Login Page"):
            await login_page.open()
        await think(0.5, 1.5)

        async with event(self, "02 - Fill Credentials"):
            await login_page.fill_credentials(user["username"], user["password"])
        await think(0.5, 1.0)

        async with event(self, "03 - Submit Login"):
            await login_page.submit()
            await login_page.wait_for_success()
        await think()

        async with event(self, "04 - View Inventory"):
            await inventory_page.wait_until_loaded()
            await inventory_page.scroll_inventory()
        await think()

        async with event(self, "05 - Sort Products"):
            await inventory_page.sort_low_to_high()
        await think(0.5, 1.5)

        async with event(self, "06 - Open Product Detail"):
            await inventory_page.open_random_product()
            await product_page.wait_until_loaded()
        await think()

        async with event(self, "07 - Add to Cart"):
            await product_page.add_to_cart()
        await think(0.5, 1.5)

        async with event(self, "08 - View Cart"):
            await inventory_page.open_cart()
            await cart_page.wait_until_loaded()
        await think()

        async with event(self, "09 - Logout"):
            await inventory_page.logout()
            await page.wait_for_url("**/", timeout=10000)


if __name__ == "__main__":
    run_single_user(SauceDemoUser)