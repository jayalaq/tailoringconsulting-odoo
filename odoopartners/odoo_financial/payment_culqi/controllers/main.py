from odoo import http
from odoo.http import request
from culqi.client import Culqi
from culqi.resources import Charge
from odoo.exceptions import ValidationError


class CulqiController(http.Controller):

    @http.route(
        "/payment/culqi/return",
        type="json",
        auth="public",
        methods=["POST"],
        csrf=False,
    )
    def culqi_return(self, **post):
        token_id = post.get("token_id")
        transaction_id = post.get("transaction_id")

        if not token_id or not transaction_id:
            return {"error": "Falta el token o el ID de la transacción."}

        try:
            transaction_sudo = (
                request.env["payment.transaction"].sudo().browse(int(transaction_id))
            )

            if not transaction_sudo:
                return {"error": "Transacción no encontrada."}

            provider = transaction_sudo.provider_id

            culqi = Culqi(
                public_key=provider.culqi_public_key,
                private_key=provider.culqi_private_key,
            )

            charge_data = {
                "amount": int(transaction_sudo.amount * 100),
                "currency_code": transaction_sudo.currency_id.name,
                "email": transaction_sudo.partner_email,
                "source_id": token_id,
                "description": transaction_sudo.reference,
            }
            charge = Charge(client=culqi).create(data=charge_data)

            if charge["data"].get("object") != "charge":
                error_messages = []

                merchant_message = charge["data"].get("merchant_message")
                user_message = charge["data"].get("user_message")

                if merchant_message:
                    error_messages.append(merchant_message)
                if user_message:
                    error_messages.append(user_message)

                final_message = (
                    "\n\n".join(error_messages) if error_messages else "Error desconocido"
                )

                return {"error": final_message}

            notification_data = {
                "amount": transaction_sudo.amount,
                "currency": transaction_sudo.currency_id.name,
                "reference": transaction_sudo.reference,
                "status": "done",
            }
            transaction_sudo._handle_notification_data("culqi", notification_data)
            return {"success": True}
        except ValidationError:
            return {"error": "No se pudo procesar la compra"}
        except Exception as excep_val:
            return {"error": f"No se pudo procesar la compra:\n{excep_val}"}
