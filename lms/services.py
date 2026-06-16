import stripe
from django.conf import settings
from rest_framework.serializers import ValidationError

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_stripe_product(course):
    """Создаёт продукт в Stripe"""
    try:
        product = stripe.Product.create(
            name=course.title,
            description=course.description or '',
        )
        return product.id
    except stripe.error.StripeError as e:
        raise ValidationError(f'Ошибка Stripe: {str(e)}')


def create_stripe_price(product_id, amount):
    """Создаёт цену в Stripe (amount в копейках)"""
    try:
        price = stripe.Price.create(
            product=product_id,
            unit_amount=int(amount * 100),
            currency='rub',
        )
        return price.id
    except stripe.error.StripeError as e:
        raise ValidationError(f'Ошибка Stripe: {str(e)}')


def create_stripe_session(price_id, success_url, cancel_url):
    """Создаёт сессию оплаты и возвращает URL"""
    try:
        session = stripe.checkout.Session.create(
            line_items=[{
                'price': price_id,
                'quantity': 1,
            }],
            mode='payment',
            success_url=success_url,
            cancel_url=cancel_url,
        )
        return session.id, session.url
    except stripe.error.StripeError as e:
        raise ValidationError(f'Ошибка Stripe: {str(e)}')