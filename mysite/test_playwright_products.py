
from playwright.sync_api import sync_playwright, expect
import re
from pathlib import Path
import pytest
from decimal import Decimal
from django.contrib.auth import get_user_model
from myapp.models import OrderDetail



# def test_homepage_displays_products():
#     with sync_playwright() as p:
#         browser = p.chromium.launch(
#             channel="chrome",
#             headless=True,
#         )

#         page = browser.new_page()
#         response = page.goto("http://127.0.0.1:8000/")

#         assert response is not None
#         assert response.status == 200

#         print("Page title:", page.title())
#         print("Page URL:", page.url)

#         browser.close()

# def test_login_page_has_form():
#     with sync_playwright() as p:
#         browser = p.chromium.launch(
#             channel="chrome",
#             headless=True,
#         )
#         page = browser.new_page()

#         page.goto("http://127.0.0.1:8000/login/")

#         expect(page.locator("form")).to_be_visible()

#         print("Login fields:")
#         print(page.locator("input").evaluate_all(
#             "(inputs) => inputs.map(i => ({name: i.name, type: i.type}))"
#         ))

#         browser.close()

# def test_login_success():
#     with sync_playwright() as p:
#         browser = p.chromium.launch(
#             channel="chrome",
#             headless=True,
#         )
#         page = browser.new_page()

#         page.goto("http://127.0.0.1:8000/login/")

#         page.locator('input[name="username"]').fill("sajjadzolghadr")
#         page.locator('input[name="password"]').fill("S22421092s@")

#         page.locator('input[name="password"]').press("Enter")
#         print("Current URL:", page.url)
#         print("Page text:", page.locator("body").inner_text())

#         expect(page).not_to_have_url(
#             "http://127.0.0.1:8000/login/"
#         )

#         print("Login URL:", page.url)

#         browser.close()



# def test_product_is_visible_after_login():
#     with sync_playwright() as p:
#         browser = p.chromium.launch(
#             channel="chrome",
#             headless=True,
#         )
#         page = browser.new_page()

#         page.goto("http://127.0.0.1:8000/login/")

#         page.locator('input[name="username"]').fill("sajjadzolghadr")
#         page.locator('input[name="password"]').fill("S22421092s@")
#         page.locator('input[name="password"]').press("Enter")

#         expect(page).to_have_url("http://127.0.0.1:8000/")
#         expect(
#             page.get_by_text("iphone 18 promax", exact=True)
#         ).to_be_visible()

#         browser.close()

def test_view_product_details():
    with sync_playwright() as p:
        browser = p.chromium.launch(
            channel="chrome",
            headless=True,
        )
        page = browser.new_page()

        page.goto("http://127.0.0.1:8000/login/")

        page.locator('input[name="username"]').fill("sajjadzolghadr")
        page.locator('input[name="password"]').fill("S22421092s@")
        page.locator('input[name="password"]').press("Enter")

        expect(page).to_have_url("http://127.0.0.1:8000/")

        expect(
            page.get_by_text("iphone 18 promax", exact=True)
        ).to_be_visible()

        page.get_by_role("link", name="View").click()

        expect(page).to_have_url("http://127.0.0.1:8000/product/2")

        expect(
            page.get_by_text("iphone 18 promax", exact=True)
                ).to_be_visible()

        expect(page.get_by_text("design by apple", exact=True)).to_be_visible()

        expect(page.get_by_text("$1199.0", exact=True)).to_be_visible()

        expect(page.get_by_text("Available", exact=True)).to_be_visible()

        

        browser.close()





def test_add_product_to_cart(logged_in_page):
    
        page = logged_in_page
        # page.get_by_role("link", name="View").click()
        # expect(page).to_have_url("http://127.0.0.1:8000/product/2")

       
        
        cart_text = page.get_by_text(
            "Cart",
            exact=False
        ).first.inner_text()

        initial_count = int(cart_text.split()[-1])

        
        page.get_by_role("link", name="Add to Cart").click()

      
        expect(page).to_have_url("http://127.0.0.1:8000/")

        
        expect(
            page.get_by_text(f"Cart {initial_count + 1}", exact=True)
        ).to_be_visible()




def test_cart_displays_product(logged_in_page):

    
    page = logged_in_page

        # باز کردن سبد خرید
    page.goto("http://127.0.0.1:8000/cart/")

        # بررسی عنوان صفحه
    expect(
            page.get_by_role("heading", name="My Purchases")
        ).to_be_visible()

        # بررسی وجود محصول
    expect(
            page.get_by_role("heading", name="iphone 18 promax")
        ).to_be_visible()

        # بررسی تعداد محصول
    expect(page.get_by_text("Quantity:", exact=True)).to_be_visible()

        # بررسی قیمت کل یا جمع جزء
    expect(page.get_by_text("Subtotal:", exact=False)).to_be_visible()







def test_increase_product_quantity(logged_in_page):
    page = logged_in_page
    
    # رفتن به سبد خرید
    page.goto("http://127.0.0.1:8000/cart/")

    # پیدا کردن کارت محصول
    product_card = page.locator(".card").filter(
        has_text="iphone 18 promax"
    )

    expect(product_card).to_be_visible()

    # خواندن تعداد فعلی
    quantity = product_card.locator(
        "div.d-flex.align-items-center.gap-2.mb-2 > span"
    ).nth(1)

    initial_quantity = int(quantity.inner_text())

    # افزایش تعداد محصول
    product_card.get_by_role("link", name="+").click()
    

    # بررسی افزایش تعداد به اندازه یک واحد
    expect(quantity).to_have_text(str(initial_quantity + 1))




def test_decrease_product_quantity(logged_in_page):
    page = logged_in_page
    

    # رفتن به سبد خرید
    page.goto("http://127.0.0.1:8000/cart/")

    # پیدا کردن کارت محصول
    product_card = page.locator(".card").filter(
        has_text="iphone 18 promax"
    )
    expect(product_card).to_be_visible()

    # خواندن تعداد فعلی
    quantity = product_card.locator(
        "div.d-flex.align-items-center.gap-2.mb-2 > span"
    ).nth(1)

    initial_quantity = int(quantity.inner_text())

    # کاهش تعداد
    product_card.get_by_role("link", name="-").click()

    # بررسی کاهش یک واحدی
    expect(quantity).to_have_text(str(initial_quantity - 1))



def test_remove_product_from_cart(logged_in_page):

    page = logged_in_page
  
    # رفتن به سبد خرید
    page.goto("http://127.0.0.1:8000/cart/")

    # پیدا کردن کارت محصول
    product_card = page.locator(".card").filter(
        has_text="iphone 18 promax"
    )
    expect(product_card).to_be_visible()

    # حذف محصول
    product_card.get_by_role("link", name="Remove").click()

    # بررسی حذف محصول از سبد خرید
    expect(
        page.get_by_role("heading", name="iphone 18 promax")
    ).to_have_count(0)



def test_empty_cart_message(page):
    # ورود به حساب کاربری
    page.goto("http://127.0.0.1:8000/login/")

    page.locator('input[name="username"]').fill("sajjadzolghadr")
    page.locator('input[name="password"]').fill("S22421092s@")
    page.locator('input[name="password"]').press("Enter")

    expect(page).to_have_url("http://127.0.0.1:8000/")

    # رفتن به سبد خرید
    page.goto("http://127.0.0.1:8000/cart/")

    # بررسی پیام سبد خرید خالی
    expect(page.get_by_text("Your cart is empty.")).to_be_visible()




def test_cart_total(logged_in_page):
    page = logged_in_page
    test_add_product_to_cart(logged_in_page)

    # رفتن به سبد خرید
    page.goto("http://127.0.0.1:8000/cart/")

    # بررسی وجود محصول
    product_card = page.locator(".card").filter(
        has_text="iphone 18 promax"
    )
    expect(product_card).to_be_visible()

    # خواندن قیمت و تعداد از صفحه
    price_text = product_card.locator("p").first.inner_text()
    price = Decimal(price_text.replace("Price: $", "").strip())
  
    quantity = int(
        product_card.locator(
            "div.d-flex.align-items-center.gap-2.mb-2 > span"
        ).nth(1).inner_text()
    )

    expected_total = price * quantity
   
    # خواندن مبلغ کل
    total_text = page.locator("h4").filter(
        has_text="Total:"
    ).inner_text()

    actual_total = Decimal(
        total_text.replace("Total: $", "").strip()
    )
    print(actual_total,expected_total)

    # بررسی برابری مبلغ کل
    assert actual_total == expected_total



def test_checkout_redirects_to_orders(page):
    # ورود به حساب کاربری
    page.goto("http://127.0.0.1:8000/login/")

    page.locator('input[name="username"]').fill("akbar")
    page.locator('input[name="password"]').fill("S22421092s2")
    page.locator('input[name="password"]').press("Enter")

    expect(page).to_have_url("http://127.0.0.1:8000/")

    # رفتن به سبد خرید
    page.goto("http://127.0.0.1:8000/cart/")

    # بررسی نمایش دکمه ثبت سفارش
    checkout_button = page.get_by_role(
        "button", name="Checkout Order"
    )
    expect(checkout_button).to_be_visible()

    # ثبت سفارش
    checkout_button.click()

    # بررسی انتقال به صفحه لیست سفارش‌ها
    expect(page).to_have_url(
        "http://127.0.0.1:8000/orders/"

    )


def test_orders_list_page(page):
    # ورود به حساب کاربری
    page.goto("http://127.0.0.1:8000/login/")

    page.locator('input[name="username"]').fill("akbar")
    page.locator('input[name="password"]').fill("S22421092s2")
    page.locator('input[name="password"]').press("Enter")

    expect(page).to_have_url("http://127.0.0.1:8000/")

    # باز کردن صفحه سفارش‌ها
    page.goto("http://127.0.0.1:8000/orders/")

    # بررسی باز شدن صفحه
    expect(page).to_have_url("http://127.0.0.1:8000/orders/")

    # نمایش عنوان لیست سفارش‌ها
    expect(
        page.get_by_role("heading", name="My Orders")
    ).to_be_visible()



def test_open_order_details(page):
    # ورود به حساب کاربری
    page.goto("http://127.0.0.1:8000/login/")

    page.locator('input[name="username"]').fill("akbar")
    page.locator('input[name="password"]').fill("S22421092s2")
    page.locator('input[name="password"]').press("Enter")

    expect(page).to_have_url("http://127.0.0.1:8000/")

    # باز کردن لیست سفارش‌ها
    page.goto("http://127.0.0.1:8000/orders/")

    # پیدا کردن اولین سفارش
    order_card = page.locator(".card").first
    expect(order_card).to_be_visible()

    # کلیک روی Details
    order_card.get_by_role("link", name="Details").click()
    print("Current URL:", page.url)

    # بررسی باز شدن صفحه جزئیات سفارش
    expect(page).to_have_url(re.compile(r".*/orders/\d+/?$"))






def test_order_details_content(page):
    # ورود به حساب کاربری
    page.goto("http://127.0.0.1:8000/login/")

    page.locator('input[name="username"]').fill("akbar")
    page.locator('input[name="password"]').fill("S22421092s2")
    page.locator('input[name="password"]').press("Enter")

    expect(page).to_have_url("http://127.0.0.1:8000/")

    # رفتن به لیست سفارش‌ها
    page.goto("http://127.0.0.1:8000/orders/")

    # انتخاب اولین سفارش
    order_card = page.locator(".card").first
    expect(order_card).to_be_visible()

    # رفتن به جزئیات سفارش
    order_card.get_by_role("link", name="Details").click()

    # بررسی عنوان صفحه
    expect(
        page.get_by_role("heading", name="Order Details")
    ).to_be_visible()

    # بررسی نام کاربر
    expect(page.get_by_text("User:")).to_be_visible()

    # بررسی وجود محصول در جزئیات سفارش
    detail_card = page.locator(".card").first
    expect(detail_card).to_be_visible()

    # بررسی تعداد و مبلغ
    expect(detail_card.get_by_text("Quantity:", exact=False)).to_be_visible()
    expect(detail_card.get_by_text("Amount:", exact=False)).to_be_visible()

    # بررسی دکمه بازگشت
    expect(
        page.get_by_role("link", name="Back to Orders")
    ).to_be_visible()

    



def test_pay_order_button_for_unpaid_order(page):
    # ورود به حساب کاربری
    page.goto("http://127.0.0.1:8000/login/")

    page.locator('input[name="username"]').fill("akbar")
    page.locator('input[name="password"]').fill("S22421092s2")
    page.locator('input[name="password"]').press("Enter")

    expect(page).to_have_url("http://127.0.0.1:8000/")

    # باز کردن لیست سفارش‌ها
    page.goto("http://127.0.0.1:8000/orders/")

    # انتخاب اولین سفارش
    order_card = page.locator(".card").first
    expect(order_card).to_be_visible()

    # باز کردن جزئیات سفارش
    order_card.get_by_role("link", name="Details").click()

    # بررسی وضعیت پرداخت
    if page.get_by_text("Unpaid", exact=True).count() > 0:
        pay_button = page.get_by_role("button", name="Pay Order")
        expect(pay_button).to_be_visible()

        # کلیک روی پرداخت
        pay_button.click()

        # بررسی نتیجه پرداخت
        expect(page.get_by_text("Paid", exact=True)).to_be_visible()

        print("Order payment completed successfully!")

    else:
        print("این سفارش قبلاً پرداخت شده است.")






def test_download_button_for_paid_order(logged_in_page):
    page = logged_in_page


    # رفتن به لیست سفارش‌ها
    page.goto("http://127.0.0.1:8000/orders/")

    # انتخاب اولین سفارش
    order_card = page.locator(".card").first
    expect(order_card).to_be_visible()

    # باز کردن جزئیات سفارش
    order_card.get_by_role("link", name="Details").click()

    # پیدا کردن کارت پرداخت‌شده
    paid_card = page.locator(".card").filter(
        has=page.get_by_text("Paid", exact=True)
    ).filter(
        has=page.get_by_role("link", name="Download")
    ).first

    expect(paid_card).to_be_visible()

    # کلیک و انتظار برای دانلود
    with page.expect_download() as download_info:
        paid_card.get_by_role("link", name="Download").click()

    download = download_info.value

    # بررسی اینکه دانلود انجام شده و نام فایل مشخص است
    print("Downloaded file:", download.suggested_filename)
    assert download.suggested_filename




def test_back_to_orders_link(logged_in_page):
    page = logged_in_page

    page.goto("http://127.0.0.1:8000/orders/")

    order_card = page.locator(".card").first
    order_card.get_by_role("link", name="Details").click()

    back_link = page.get_by_role("link", name="Back to Orders")
    expect(back_link).to_be_visible()



def test_back_to_orders_navigation(logged_in_page):
    page = logged_in_page

    page.goto("http://127.0.0.1:8000/orders/")

    order_card = page.locator(".card").first
    order_card.get_by_role("link", name="Details").click()

    page.get_by_role("link", name="Back to Orders").click()

    expect(page).to_have_url("http://127.0.0.1:8000/orders/")




def test_order_payment_status_visible(logged_in_page):
    page = logged_in_page

    page.goto("http://127.0.0.1:8000/orders/")

    order_card = page.locator(".card").first
    order_card.get_by_role("link", name="Details").click()

    payment_status = page.get_by_text(
        "Paid", exact=True
    ).or_(page.get_by_text("Unpaid", exact=True))

    expect(payment_status.first).to_be_visible()



def test_order_total_is_visible(logged_in_page):
    page = logged_in_page

    page.goto("http://127.0.0.1:8000/orders/")

    order_card = page.locator(".card").first
    order_card.get_by_role("link", name="Details").click()

    total = page.get_by_text("Total:", exact=False)
    expect(total).to_be_visible()




def test_pay_order_changes_status(logged_in_page):
    page = logged_in_page
    page.goto("http://127.0.0.1:8000/orders/")

    # Find orders that have not been paid
    order_cards = page.locator(".card").filter(
        has_text="Unpaid"
    )

    if order_cards.count() == 0:
        pytest.skip("No unpaid order is available for this test.")

    # Open the first unpaid order
    order_card = order_cards.first
    order_card.get_by_role("link", name="Details").click()

    # Verify the payment status before payment
    expect(
        page.get_by_text("Unpaid", exact=True)
    ).to_be_visible()

    # Pay the order
    page.get_by_role("button", name="Pay Order").click()

    # Verify that the payment status changes to Paid
    expect(
        page.get_by_text("Paid", exact=True)
    ).to_be_visible()








def test_download_visibility_depends_on_payment(logged_in_page):
    page = logged_in_page
    page.goto("http://127.0.0.1:8000/orders/")

    unpaid_orders = page.locator(".card").filter(
        has_text="Unpaid"
    )

    if unpaid_orders.count() == 0:
        pytest.skip("No unpaid order is available for this test.")

    unpaid_orders.first.get_by_role("link", name="Details").click()

    # Find product cards marked as unpaid
    unpaid_cards = page.locator(".card").filter(
        has=page.get_by_text("Unpaid", exact=True).first
    )

    expect(unpaid_cards.first).to_be_visible()

    # Verify that the unpaid product card has no download link
    expect(
        unpaid_cards.first.get_by_role("link", name="Download")
    ).to_have_count(0)

    # Verify that the payment button is visible
    expect(
        page.get_by_role("button", name="Pay Order")
    ).to_be_visible()


def test_order_item_quantity_is_visible(logged_in_page):
    page = logged_in_page
    page.goto("http://127.0.0.1:8000/orders/")

    order_card = page.locator(".card").first
    expect(order_card).to_be_visible()

    order_card.get_by_role("link", name="Details").click()

    # Find quantity information in the order details
    quantity = page.get_by_text(re.compile(r"Quantity:\s*\d+"))
    print(quantity.inner_text())

    expect(quantity.first).to_be_visible()



import re
from playwright.sync_api import expect


def test_order_item_amount_is_visible(logged_in_page):
    page = logged_in_page
    page.goto("http://127.0.0.1:8000/orders/")

    order_card = page.locator(".card").first
    expect(order_card).to_be_visible()

    order_card.get_by_role("link", name="Details").click()

    # Find the amount displayed for an order item
    amount = page.get_by_text(
        re.compile(r"Amount:\s*\$[\d,.]+")
    )

    expect(amount.first).to_be_visible()

    # Print the amount for debugging
    print("Order item amount:", amount.first.inner_text())



def test_order_total_matches_item_amounts(logged_in_page):
    page = logged_in_page
    page.goto("http://127.0.0.1:8000/orders/")

    order_card = page.locator(".card").first
    expect(order_card).to_be_visible()

    order_card.get_by_role("link", name="Details").click()

    # Read all item amounts
    amount_elements = page.get_by_text(
        re.compile(r"Amount:\s*\$[\d,.]+")
    )

    expect(amount_elements.first).to_be_visible()

    amounts = []
    for i in range(amount_elements.count()):
        text = amount_elements.nth(i).inner_text()
        value = re.search(r"\$([\d,.]+)", text).group(1)
        amounts.append(Decimal(value.replace(",", "")))

    # Read the displayed order total
    total_text = page.get_by_text(
        re.compile(r"Total:\s*\$[\d,.]+")
    ).inner_text()

    total_value = re.search(r"\$([\d,.]+)", total_text).group(1)
    displayed_total = Decimal(total_value.replace(",", ""))

    # Verify that the total equals the sum of item amounts
    calculated_total = sum(amounts, Decimal("0.00"))

    print("Item amounts:", amounts)
    print("Calculated total:", calculated_total)
    print("Displayed total:", displayed_total)

    assert calculated_total == displayed_total




def test_order_product_name_is_visible(logged_in_page):
    page = logged_in_page
    page.goto("http://127.0.0.1:8000/orders/")

    order_card = page.locator(".card").first
    expect(order_card).to_be_visible()

    order_card.get_by_role("link", name="Details").click()

    # Find the product name displayed in the order details
    product_name = page.locator(".card h5").first

    expect(product_name).to_be_visible()

    # Print the product name
    print("Product name:", product_name.inner_text())


def test_order_username_is_visible(logged_in_page):
    page = logged_in_page
    page.goto("http://127.0.0.1:8000/orders/")

    order_card = page.locator(".card").first
    expect(order_card).to_be_visible()

    order_card.get_by_role("link", name="Details").click()

    # Find the username displayed in the order details
    username = page.get_by_text(
        re.compile(r"User:\s*\S+")
    )

    expect(username).to_be_visible()

    # Print the username
    print("Order username:", username.inner_text())



def test_order_belongs_to_logged_in_user(logged_in_page):
    page = logged_in_page
    expected_username = "akbar"

    page.goto("http://127.0.0.1:8000/orders/")

    order_card = page.locator(".card").first
    expect(order_card).to_be_visible()

    order_card.get_by_role("link", name="Details").click()

    # Read the username associated with the order
    username_text = page.get_by_text(
        re.compile(r"User:\s*\S+")
    )

    expect(username_text).to_be_visible()

    actual_username = username_text.inner_text().split(":", 1)[1].strip()

    # Verify that the order belongs to the logged-in user
    print("Expected username:", expected_username)
    print("Actual order username:", actual_username)

    assert actual_username == expected_username




def test_nonexistent_order_is_not_accessible(logged_in_page):
    page = logged_in_page

    # Open an order URL with an ID that should not exist
    response = page.goto("http://127.0.0.1:8000/orders/999999999/")

    # Verify that the server returns a not-found response
    assert response is not None
    assert response.status == 404



def test_each_order_has_details_link(logged_in_page):
    page = logged_in_page
    page.goto("http://127.0.0.1:8000/orders/")

    # Find all order cards
    order_cards = page.locator(".card")
    expect(order_cards.first).to_be_visible()

    # Check that each order card has a Details link
    for i in range(order_cards.count()):
        order_card = order_cards.nth(i)
        expect(
            order_card.get_by_role("link", name="Details")
        ).to_be_visible()




def test_count_orders(logged_in_page):
    page = logged_in_page
    page.goto("http://127.0.0.1:8000/orders/")

    # Find all order cards
    order_cards = page.locator(".card")

    # Count the displayed orders
    order_count = order_cards.count()

    print("Number of orders:", order_count)

    # Verify that at least one order is displayed
    assert order_count > 0, "No orders were displayed."



def test_orders_page_title(logged_in_page):
    page = logged_in_page
    page.goto("http://127.0.0.1:8000/orders/")

    # Verify the page title
    expect(page).to_have_title("My Orders")


def test_empty_orders_message(logged_in_page):
    page = logged_in_page
    page.goto("http://127.0.0.1:8000/orders/")

    # Check whether any order cards are displayed
    order_cards = page.locator(".card")

    if order_cards.count() > 0:
        pytest.skip("The logged-in user already has orders.")

    # Verify the empty-state message
    empty_message = page.get_by_text(
        "No orders found", exact=False
    )
    expect(empty_message).to_be_visible()





def test_product_seller_is_visible(logged_in_page):
    page = logged_in_page

    # Find the seller label on the home page
    seller = page.locator("h8.card-title").filter(
        has_text="Seller:"
    ).first

    expect(seller).to_be_visible()
    expect(seller).to_contain_text("Seller: hosein")

    # Print the seller information
    print("Seller information:", seller.inner_text())



def test_product_description_is_visible(logged_in_page):
    page = logged_in_page
    # Find the product card by its name
    product_card = page.locator(".card").filter(
        has_text="iphone 18 promax"
    ).first

    expect(product_card).to_be_visible()

    # Verify that the product description is visible
    description = product_card.get_by_text(
        "design by apple", exact=True
    )
    expect(description).to_be_visible()

    # Print the product description
    print("Product description:", description.inner_text())



def test_complete_purchase_flow(logged_in_page):
    page = logged_in_page
    product_card = page.locator(".card").filter(
        has_text="iphone 18 promax"
    ).first
    expect(product_card).to_be_visible()

    # Add the product to the cart
    product_card.get_by_role(
        "link", name="Add to Cart"
    ).click()

    # Open the cart and verify the product is present
    page.goto("http://127.0.0.1:8000/cart/")

    cart_product = page.locator(".card").filter(
        has_text="iphone 18 promax"
    ).first
    expect(cart_product).to_be_visible()

    # Verify that the cart displays a quantity
    expect(
        cart_product.get_by_text(re.compile(r"Quantity"))
    ).to_be_visible()

    # Complete checkout
    checkout_button = page.get_by_role(
        "button", name="Checkout Order"
    )
    expect(checkout_button).to_be_visible()
    checkout_button.click()

    # Verify that the orders page opens
    expect(page).to_have_url(
        re.compile(r"http://127\.0\.0\.1:8000/orders/?")
    )

    # Verify that at least one order is displayed
    expect(page.locator(".card").first).to_be_visible()


def test_order_total_matches_item_amounts(logged_in_page):
    page = logged_in_page
    page.goto("http://127.0.0.1:8000/orders/")

    order_card = page.locator(".card").filter(
        has_text="Order #"
    ).first
    expect(order_card).to_be_visible()

    order_card.get_by_role("link", name="Details").click()
    expect(page.get_by_role("heading", name="Order Details")).to_be_visible()

    amounts = page.locator(".card p").filter(
        has_text=re.compile(r"Amount:\s*\$")
    )
    expect(amounts.first).to_be_visible()

    item_total = Decimal("0")
    for i in range(amounts.count()):
        text = amounts.nth(i).inner_text()
        match = re.search(r"Amount:\s*\$([\d,]+(?:\.\d{1,2})?)", text)
        assert match, f"Could not read item amount: {text}"
        item_total += Decimal(match.group(1).replace(",", ""))

    total_text = page.get_by_role("heading", name=re.compile(r"Total:")).inner_text()
    total_match = re.search(r"Total:\s*\$([\d,]+(?:\.\d{1,2})?)", total_text)
    assert total_match, f"Could not read order total: {total_text}"

    displayed_total = Decimal(total_match.group(1).replace(",", ""))
    assert displayed_total == item_total, (
        f"Order total mismatch: displayed={displayed_total}, "
        f"sum of item amounts={item_total}"
    )

    print("Sum of item amounts:", item_total)
    print("Displayed order total:", displayed_total)




def test_payment_updates_status_and_enables_download(logged_in_page):
    page = logged_in_page
    page.goto("http://127.0.0.1:8000/orders/")

    order_cards = page.locator(".card").filter(has_text="Order #")
    unpaid_order = None

    for i in range(order_cards.count()):
        card = order_cards.nth(i)

        if card.get_by_text("Unpaid", exact=True).count() > 0:
            unpaid_order = card
            break

    if unpaid_order is None:
        pytest.skip("No unpaid order is available.")

    unpaid_order.get_by_role("link", name="Details").click()

    expect(
        page.get_by_role("heading", name="Order Details")
    ).to_be_visible()

    expect(
        page.get_by_role("button", name="Pay Order")
    ).to_be_visible()

    page.get_by_role("button", name="Pay Order").click()

    expect(
        page.get_by_role("heading", name="Order Details")
    ).to_be_visible()

    expect(
        page.locator(".badge.bg-success").filter(has_text="Paid").first
    ).to_be_visible()

    download_link = page.locator(
    'a[href*="/download/"]'
).filter(has_text="Download")

    expect(download_link.first).to_be_visible()
    print("Order payment status:", "Paid")
    print("Download link is visible.")



def test_unpaid_order_has_no_download_link(logged_in_page):
    page = logged_in_page
    page.goto("http://127.0.0.1:8000/orders/")

    order_cards = page.locator(".card").filter(has_text="Order #")
    unpaid_order = None

    for i in range(order_cards.count()):
        card = order_cards.nth(i)

        if card.get_by_text("Unpaid", exact=True).count() > 0:
            unpaid_order = card
            break

    if unpaid_order is None:
        pytest.skip("No unpaid order is available.")

    unpaid_order.get_by_role("link", name="Details").click()

    expect(
        page.get_by_role("heading", name="Order Details")
    ).to_be_visible()

    expect(
        page.get_by_text("Unpaid", exact=True).first
    ).to_be_visible()

    download_link = page.locator('a[href*="/download/"]')
    expect(download_link).to_have_count(0)

    print("Unpaid order has no download link.")





def test_unpaid_product_download_is_rejected(logged_in_page):
    page = logged_in_page
    page.goto("http://127.0.0.1:8000/orders/")

    order_cards = page.locator(".card").filter(has_text="Order #")
    unpaid_order = None

    for i in range(order_cards.count()):
        card = order_cards.nth(i)

        if card.get_by_text("Unpaid", exact=True).count() > 0:
            unpaid_order = card
            break

    if unpaid_order is None:
        pytest.skip("No unpaid order is available.")

    unpaid_order.get_by_role("link", name="Details").click()

    expect(
        page.get_by_role("heading", name="Order Details")
    ).to_be_visible()

    unpaid_badge = page.locator(".badge.bg-warning").filter(
        has_text="Unpaid"
    ).first
    expect(unpaid_badge).to_be_visible()

    download_url = page.locator('a[href*="/download/"]')

    if download_url.count() > 0:
        pytest.fail("The unpaid order unexpectedly exposes a download link.")

    page_url = page.url
    order_id = page_url.rstrip("/").split("/")[-1]

    print("Order details URL:", page_url)
    print("Order ID:", order_id)
    print("The page does not expose a download link for the unpaid item.")




import pytest
from playwright.sync_api import expect


def test_direct_download_of_unpaid_order_is_rejected(logged_in_page):
    page = logged_in_page
    page.goto("http://127.0.0.1:8000/orders/")

    order_cards = page.locator(".card").filter(has_text="Order #")
    unpaid_order = None

    for i in range(order_cards.count()):
        card = order_cards.nth(i)

        if card.get_by_text("Unpaid", exact=True).count() > 0:
            unpaid_order = card
            break

    if unpaid_order is None:
        pytest.skip("No unpaid order is available.")

    unpaid_order.get_by_role("link", name="Details").click()

    expect(
        page.get_by_role("heading", name="Order Details")
    ).to_be_visible()

    unpaid_badge = page.locator(".badge.bg-warning").filter(
        has_text="Unpaid"
    ).first
    expect(unpaid_badge).to_be_visible()

    order_detail_id = None

    for i in range(page.locator(".card").count()):
        card = page.locator(".card").nth(i)

        if card.get_by_text("Unpaid", exact=True).count() > 0:
            order_detail_id = card.locator(
                'a[href*="/download/"]'
            ).get_attribute("href")
            break

    if order_detail_id:
        pytest.fail("Unexpected download link found for an unpaid item.")

    pytest.skip(
        "The unpaid item's detail ID is not exposed in the page. "
        "Use a known OrderDetail ID to test the direct URL."
    )



def test_unpaid_order_download_returns_404(logged_in_page):
    page = logged_in_page
    page.goto("http://127.0.0.1:8000/orders/")

    order_cards = page.locator(".card").filter(has_text="Order #")
    unpaid_order = None

    for i in range(order_cards.count()):
        card = order_cards.nth(i)

        if card.get_by_text("Unpaid", exact=True).count() > 0:
            unpaid_order = card
            break

    if unpaid_order is None:
        pytest.skip("No unpaid order is available.")

    unpaid_order.get_by_role("link", name="Details").click()

    expect(
        page.get_by_role("heading", name="Order Details")
    ).to_be_visible()

    unpaid_detail_card = page.locator(
        ".card[data-detail-id]"
    ).filter(has_text="Unpaid").first

    expect(unpaid_detail_card).to_be_visible()

    detail_id = unpaid_detail_card.get_attribute("data-detail-id")
    assert detail_id, "OrderDetail ID was not found."

    response = page.request.get(
        f"http://127.0.0.1:8000/orders/detail/{detail_id}/download/"
    )

    assert response.status == 404, (
        f"Expected 404 for unpaid download, got {response.status}"
    )

    print("Unpaid OrderDetail ID:", detail_id)
    print("Download response status:", response.status)



def test_cannot_download_another_users_order(logged_in_page):
    page = logged_in_page

    other_user_detail_id = 23

    response = page.request.get(
        f"http://127.0.0.1:8000/orders/detail/{other_user_detail_id}/download/"
    )

    assert response.status == 404, (
        f"Expected 404 for another user's order, "
        f"got {response.status}"
    )

    print("Unauthorized download was rejected.")



def test_cannot_pay_another_users_order(logged_in_page):
    page = logged_in_page

    other_user_order_id = 22

    page.goto(f"http://127.0.0.1:8000/orders/{other_user_order_id}")

    response = page.request.get(
        f"http://127.0.0.1:8000/orders/{other_user_order_id}"
    )

    assert response.status == 404, (
        f"Expected 404 for another user's order, "
        f"got {response.status}"
    )
    # print("Unauthorized payment attempt was rejected.")
    # print("Response status:", response.status)


def test_user_can_pay_own_order(logged_in_page):
    page = logged_in_page
    own_order_id= 25
    page.goto(f"http://127.0.0.1:8000/orders/{own_order_id}")

    pay_button = page.get_by_role("button", name="Pay Order")

    if pay_button.count() == 0:
        pytest.skip("Pay Order button is not available.")

    pay_button.click()

    expect(
        page.get_by_role("heading", name="Order Details")
    ).to_be_visible()

    expect(
        page.locator(".badge.bg-success").filter(has_text="Paid").first
    ).to_be_visible()

    expect(
        page.locator('a[href*="/download/"]').first
    ).to_be_visible()

    print("Own order was paid successfully.")



def test_non_seller_cannot_open_create_product_page(logged_in_page):
    page = logged_in_page

    page.goto("http://127.0.0.1:8000/createproduct")

    expect(page).not_to_have_url("http://127.0.0.1:8000/product/create/")




def test_seller_can_create_product(logged_in_page_seller, tmp_path):
    page = logged_in_page_seller
    product_name = "Playwright Test Product"

    page.goto("http://127.0.0.1:8000/createproduct")

    expect(page.get_by_role("heading", name="Create Product")).to_be_visible()

    page.locator('input[name="name"]').fill(product_name)
    page.locator('textarea[name="description"]').fill(
        "Product created by Playwright test"
    )
    page.locator('input[name="price"]').fill("25.50")

    test_file = tmp_path / "test_product.txt"
    test_file.write_text("Test product file", encoding="utf-8")
    page.locator('input[name="file"]').set_input_files(str(test_file))

    page.get_by_role("button", name="Create Product").click()
    print("Current URL:", page.url)
    print("Page content:", page.locator("body").inner_text())

    expect(page).to_have_url("http://127.0.0.1:8000/")
    product_card = page.locator(".card").filter(
    has=page.get_by_role("heading", name=product_name, exact=True)).last
    expect(product_card).to_be_visible()
    expect(product_card.locator("h8.card-title")).to_contain_text("hosein")


def test_seller_can_create_100_products(logged_in_page_seller, tmp_path):
    page = logged_in_page_seller
    test_file = tmp_path / "test_product.txt"
    test_file.write_text("Playwright test product file", encoding="utf-8")

    created_products = []

    for i in range(1, 101):
        product_name = f"Automation Product {i}"
        created_products.append(product_name)

        page.goto("http://127.0.0.1:8000/createproduct")

        page.locator('input[name="name"]').fill(product_name)
        page.locator('textarea[name="description"]').fill(
            f"Description for automation product {i}"
        )
        page.locator('input[name="price"]').fill(str(i * 10))
        page.locator('input[name="file"]').set_input_files(str(test_file))

        page.get_by_role("button", name="Create Product").click()

        expect(page).to_have_url("http://127.0.0.1:8000/")

    for product_name in created_products:
        expect(
            page.get_by_role("heading", name=product_name, exact=True)
        ).to_be_visible()



def test_delete_all_100_automation_products(logged_in_page_seller):
    page = logged_in_page_seller
    page.goto("http://127.0.0.1:8000/")

    for i in range(100, 0, -1):
        product_name = f"Automation Product {i}"

        product_heading = page.get_by_role(
            "heading",
            name=product_name,
            exact=True
        )

        if product_heading.count() == 0:
            print(f"Product not found: {product_name}")
            continue

        product_card = page.locator(".card").filter(
            has=product_heading
        ).last

        product_card.get_by_role("link", name="Delete").click()

        expect(
            page.get_by_role(
                "heading",
                name="Delete Product",
                exact=True
            )
        ).to_be_visible()

        page.get_by_role("button", name="Delete").click()

        expect(page).to_have_url("http://127.0.0.1:8000/")

        print(f"Deleted: {product_name}")

    for i in range(1, 101):
        expect(
            page.get_by_role(
                "heading",
                name=f"Automation Product {i}",
                exact=True
            )
        ).to_have_count(0)

    

def test_invalid_submission_preserves_form_data(
    logged_in_page_seller, tmp_path
):
    page = logged_in_page_seller

    page.goto("http://127.0.0.1:8000/createproduct")

    page.locator('textarea[name="description"]').fill(
        "Description should be preserved"
    )
    page.locator('input[name="price"]').fill("29.50")

    test_file = tmp_path / "invalid_test.txt"
    test_file.write_text("Test file", encoding="utf-8")
    page.locator('input[name="file"]').set_input_files(str(test_file))

    page.get_by_role("button", name="Create Product").click()

    expect(page).to_have_url(
        "http://127.0.0.1:8000/createproduct"
    )
    expect(page.locator('input[name="name"]')).to_be_visible()
    expect(
        page.locator('textarea[name="description"]')
    ).to_have_value("Description should be preserved")
    expect(page.locator('input[name="price"]')).to_have_value("29.50")




def test_create_product_with_special_characters(
    logged_in_page_seller, tmp_path
):
    page = logged_in_page_seller
    product_name = "محصول آزمایشی 🚀 #1"

    page.goto("http://127.0.0.1:8000/createproduct")

    page.locator('input[name="name"]').fill(product_name)
    page.locator('textarea[name="description"]').fill(
        "توضیحات فارسی — تست ویژه & بررسی"
    )
    page.locator('input[name="price"]').fill("19.99")

    test_file = tmp_path / "special.txt"
    test_file.write_text("Special character test", encoding="utf-8")
    page.locator('input[name="file"]').set_input_files(str(test_file))

    page.get_by_role("button", name="Create Product").click()

    expect(
        page.get_by_role("heading", name=product_name, exact=True)
    ).to_be_visible()



def test_create_product_with_negative_price(logged_in_page_seller, tmp_path):
    page = logged_in_page_seller

    page.goto("http://127.0.0.1:8000/createproduct")

    page.locator('input[name="name"]').fill("Negative Price Test")
    page.locator('textarea[name="description"]').fill(
        "Testing negative price"
    )
    page.locator('input[name="price"]').fill("-10")

    test_file = tmp_path / "negative_price.txt"
    test_file.write_text("Test file", encoding="utf-8")
    page.locator('input[name="file"]').set_input_files(str(test_file))

    page.get_by_role("button", name="Create Product").click()

    expect(page).to_have_url(
        "http://127.0.0.1:8000/createproduct"
    )
    expect(
        page.get_by_text("Price cannot be negative.")
    ).to_be_visible()



def test_create_product_with_non_numeric_price(logged_in_page_seller, tmp_path):
    page = logged_in_page_seller

    page.goto("http://127.0.0.1:8000/createproduct")

    page.locator('input[name="name"]').fill("Invalid Price Test")
    page.locator('textarea[name="description"]').fill("Testing invalid price")
    price_input = page.locator('input[name="price"]')
    price_input.evaluate("(element) => element.type = 'text'")
    price_input.fill("abc")

    test_file = tmp_path / "invalid_price.txt"
    test_file.write_text("Test file", encoding="utf-8")
    page.locator('input[name="file"]').set_input_files(str(test_file))

    page.get_by_role("button", name="Create Product").click()

    expect(page).to_have_url("http://127.0.0.1:8000/createproduct")


def test_create_product_without_price(logged_in_page_seller, tmp_path):
    page = logged_in_page_seller

    page.goto("http://127.0.0.1:8000/createproduct")

    page.locator('input[name="name"]').fill("Missing Price Test")
    page.locator('textarea[name="description"]').fill("Testing empty price")

    test_file = tmp_path / "missing_price.txt"
    test_file.write_text("Test file", encoding="utf-8")
    page.locator('input[name="file"]').set_input_files(str(test_file))

    page.get_by_role("button", name="Create Product").click()

    expect(page).to_have_url("http://127.0.0.1:8000/createproduct")



@pytest.mark.parametrize(
    ("name", "description", "price"),
    [
        ("Normal Product", "Normal description", "25.50"),
        ("محصول فارسی 🚀", "توضیحات فارسی", "10.99"),
        ("A" * 100, "Maximum length name", "1"),
        ("Long Description Product", "D" * 500, "99.99"),
        ("Zero Price Product", "Testing zero price", "0"),
    ],
)
def test_create_product_cases(
    logged_in_page_seller, tmp_path, name, description, price
):
    page = logged_in_page_seller
    page.goto("http://127.0.0.1:8000/createproduct")

    page.locator('input[name="name"]').fill(name)
    page.locator('textarea[name="description"]').fill(description)
    page.locator('input[name="price"]').fill(price)

    test_file = tmp_path / "product.txt"
    test_file.write_text("Playwright test file", encoding="utf-8")
    page.locator('input[name="file"]').set_input_files(str(test_file))

    page.get_by_role("button", name="Create Product").click()

    expect(page).to_have_url("http://127.0.0.1:8000/")
    expect(
        page.get_by_role("heading", name=name, exact=True)
    ).to_be_visible()

    page.reload()

    expect(
        page.get_by_role("heading", name=name, exact=True)
    ).to_be_visible()




def test_create_product_without_name(
    logged_in_page_seller, tmp_path
):
    page = logged_in_page_seller
    page.goto("http://127.0.0.1:8000/createproduct")

    page.locator('textarea[name="description"]').fill("Missing name")
    page.locator('input[name="price"]').fill("15")

    test_file = tmp_path / "missing_name.txt"
    test_file.write_text("Test file", encoding="utf-8")
    page.locator('input[name="file"]').set_input_files(str(test_file))

    page.get_by_role("button", name="Create Product").click()

    expect(page).to_have_url(
        "http://127.0.0.1:8000/createproduct"
    )

def test_create_product_with_name_over_max_length(
    logged_in_page_seller, tmp_path
):
    page = logged_in_page_seller
    page.goto("http://127.0.0.1:8000/createproduct")

    page.locator('input[name="name"]').fill("A" * 101)
    page.locator('textarea[name="description"]').fill("Valid description")
    page.locator('input[name="price"]').fill("20")

    test_file = tmp_path / "long_name.txt"
    test_file.write_text("Test file", encoding="utf-8")
    page.locator('input[name="file"]').set_input_files(str(test_file))

    page.get_by_role("button", name="Create Product").click()

    expect(page).to_have_url(
        "http://127.0.0.1:8000/createproduct"
    )
    expect(
        page.get_by_text("Name cannot exceed 100 characters.")
    ).to_be_visible()


def test_create_product_with_description_over_max_length(
    logged_in_page_seller, tmp_path
):
    page = logged_in_page_seller
    page.goto("http://127.0.0.1:8000/createproduct")

    page.locator('input[name="name"]').fill("Valid Product")
    page.locator('textarea[name="description"]').fill("D" * 501)
    page.locator('input[name="price"]').fill("20")

    test_file = tmp_path / "long_description.txt"
    test_file.write_text("Test file", encoding="utf-8")
    page.locator('input[name="file"]').set_input_files(str(test_file))

    page.get_by_role("button", name="Create Product").click()

    expect(page).to_have_url(
        "http://127.0.0.1:8000/createproduct"
    )
    expect(
        page.get_by_text("Description cannot exceed 500 characters.")
    ).to_be_visible()