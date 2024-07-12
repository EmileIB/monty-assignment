from fastapi import APIRouter, Header, Request

from app.integrations.stripe.services import construct_webhook_event
from app.features.orders.services import OrderService
from app.features.orders.schemas import ShippingDetails, CustomerDetails

router = APIRouter(tags=["Stripe"], prefix="/stripe")


@router.post("/webhook", summary="Stripe Webhook Endpoint")
async def webhook_received(request: Request, stripe_signature: str = Header(None)):
    data = await request.body()
    try:
        event = construct_webhook_event(data, stripe_signature)
    except Exception as e:
        return {"error": str(e)}

    event_type = event["type"]
    if event_type == "checkout.session.completed":
        checkout_session_id = event.data.object["id"]
        print(f"Checkout session completed: {checkout_session_id}")

        await OrderService.process_order_paid(
            checkout_session_id=checkout_session_id,
            shipping_details=ShippingDetails.model_validate(
                event.data.object["shipping_details"]
            ),
            customer_details=CustomerDetails.model_validate(
                event.data.object["customer_details"]
            ),
        )

    return {"status": "success"}
