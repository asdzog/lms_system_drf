import stripe
from config.settings import STRIPE_API_KEY
from courses.models import Course

stripe.api_key = STRIPE_API_KEY


def create_stripe_product(course: Course):
    return stripe.Product.create(name=course.course_name)


def create_stripe_price(amount, name):
    stripe_price = stripe.Price.create(
        currency="rub",
        unit_amount=amount * 100,
        product_data={"name": name},
        )
    return stripe_price['id']


def create_stripe_session(course):
    create_stripe_product(course)
    stripe_price_id = create_stripe_price(course.price, course.course_name)
    stripe_session = stripe.checkout.Session.create(
        success_url="http://127.0.0.1:8000/",
        line_items=[{
            "price": stripe_price_id,
            "quantity": 1,
        }],
        mode="payment",
        )
    return stripe_session['url'], stripe_session['id']
