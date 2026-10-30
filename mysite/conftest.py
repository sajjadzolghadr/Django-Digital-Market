import pytest
from playwright.sync_api import Page, expect


@pytest.fixture
def logged_in_page(page: Page):
    page.goto("http://127.0.0.1:8000/login/")

    page.locator('input[name="username"]').fill("akbar")
    page.locator('input[name="password"]').fill("S22421092s2")
    page.locator('input[name="password"]').press("Enter")

    expect(page).to_have_url("http://127.0.0.1:8000/")

    return page

@pytest.fixture
def logged_in_page_seller(page: Page):
    page.goto("http://127.0.0.1:8000/login/")

    page.locator('input[name="username"]').fill("hosein")
    page.locator('input[name="password"]').fill("S22421092s2")
    page.locator('input[name="password"]').press("Enter")

    expect(page).to_have_url("http://127.0.0.1:8000/")

    return page

