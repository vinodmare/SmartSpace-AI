class PaymentProvider:
    async def create_order(self, amount_inr: int, metadata: dict) -> dict:
        raise NotImplementedError


class RazorpayProvider(PaymentProvider):
    async def create_order(self, amount_inr: int, metadata: dict) -> dict:
        return {"provider": "razorpay", "amount_inr": amount_inr, "metadata": metadata}

