**Locust Playwright Framework**

A browser-based **performance testing** framework for SauceDemo built with Locust and Playwright.

It simulates realistic user journeys such as:
- logging in with valid credentials
- browsing the inventory
- sorting products
- opening a product detail page
- adding an item to cart
- viewing the cart
- logging out

Why this project is useful

This framework helps you test more than raw API throughput. It measures end-to-end browser behavior and captures timings for each user action in the journey.

#Key benefits:
- Real browser execution with Playwright
- Step-level performance visibility with Locust events
- Human-like delays using think time
- Modular page objects for maintainability
- Support for valid and invalid login flows

#Project structure
```
project/
├── config/
│   └── settings.py
├── pages/
│   ├── __init__.py
│   ├── base_page.py
│   ├── cart_page.py
│   ├── inventory_page.py
│   ├── login_page.py
│   └── product_page.py
├── tests/
│   └── locustfile.py
└── utils/
    └── helpers.py
```
#Requirements

- Python 3.10+
- Locust
- locust-plugins
- Playwright

#Setup

Install dependencies:

pip install locust locust-plugins playwright
playwright install

If you use a virtual environment, activate it before installing packages.

#Configuration

Update your configuration values in config/settings.py:

BASE_URL = "https://www.saucedemo.com"
HEADLESS = False
SLOW_MO = 0

#Running the test

Locust web UI:

locust -f tests/locustfile.py

Then open:
http://localhost:8089

Headless mode:

locust -f tests/locustfile.py --headless -u 5 -r 1 -t 60s

Single-user debug run:

python tests/locustfile.py

#Test behavior

The current scenario follows one complete journey:
1. Open login page
2. Fill credentials
3. Submit login
4. View inventory
5. Sort products
6. Open a random product
7. Add item to cart
8. View cart
9. Logout

#Page objects

The framework uses a simple Page Object Model:

- LoginPage handles login actions and error messages
- InventoryPage handles browsing, sorting, and logout
- ProductPage handles product detail actions
- CartPage handles cart validation

This keeps the Locust task readable and makes selector updates easier.

#Helper methods

The utils/helpers.py module is used for shared utilities such as:
- selecting a random test user
- adding think time between actions

#Troubleshooting

Browser does not appear

Set HEADLESS = False in config/settings.py and run with a single user for debugging.


#Contributing

If you want to extend the framework:
- add new page objects under pages/
- keep browser actions inside page classes
- keep Locust orchestration inside tests/locustfile.py
- avoid hardcoded waits where possible


