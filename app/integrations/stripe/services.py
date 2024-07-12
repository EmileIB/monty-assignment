import stripe
from app.core.settings import settings

from .schemas import LineItem, CheckoutMetadata

stripe.api_key = settings.STRIPE_SECRET_KEY


async def create_checkout_session(
    line_items: list[LineItem],
    metadata: CheckoutMetadata,
    success_url: str = "https://google.com",
    cancel_url: str = "https://google.com",
) -> stripe.checkout.Session:
    session = await stripe.checkout.Session.create_async(
        payment_method_types=["card"],
        line_items=[item.model_dump(mode="json") for item in line_items],
        mode="payment",
        metadata=metadata.model_dump(),
        success_url=success_url,
        cancel_url=cancel_url,
        shipping_address_collection={"allowed_countries": ["US", "LB"]},
        phone_number_collection={"enabled": True},
    )

    return session


def construct_webhook_event(payload: bytes, sig_header: str):
    return stripe.Webhook.construct_event(
        payload=payload, sig_header=sig_header, secret=settings.WEBHOOK_SECRET
    )


async def get_session(session_id: str) -> stripe.checkout.Session:
    return await stripe.checkout.Session.retrieve_async(session_id)


async def expire_session(session_id: str):
    session = await get_session(session_id)
    print(f"Session status: {session.status}")
    if session.status == "open":
        await stripe.checkout.Session.expire_async(session_id)
