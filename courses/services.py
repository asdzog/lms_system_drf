import stripe
from config.settings import STRIPE_API_KEY
stripe.api_key = STRIPE_API_KEY


def create_stripe_product(name):
    return stripe.Product.create(name=name)


def create_stripe_price(amount, name):
    stripe_price = stripe.Price.create(
        currency="rub",
        unit_amount=amount,
        product_data={"name": name},
        )
    return stripe_price['id']


def create_stripe_session(stripe_price_id):
    stripe_session = stripe.checkout.Session.create(
        success_url="http://127.0.0.1:8000/",
        line_items=[{
            "price": stripe_price_id,
            "quantity": 1,
        }],
        mode="payment",
        )
    return stripe_session['url'], stripe_session['id']
