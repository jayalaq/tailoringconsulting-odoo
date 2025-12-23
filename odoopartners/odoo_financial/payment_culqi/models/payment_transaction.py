import logging

from odoo import models, _
from odoo.tools.float_utils import float_compare
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class CulqiPaymentTransaction(models.Model):
    _inherit = "payment.transaction"

    def _get_specific_processing_values(self, processing_values):
        res = super()._get_specific_processing_values(processing_values)
        if self.provider_code != "culqi":
            return res

        culqi_config = {
            "settings": {
                "title": "Culqi",
                "currency": self.currency_id.name,
                "amount": int(self.amount * 100),
            },
            "options": {
                "lang": "auto",
                "modal": True,
            },
            "appearance": {
                "theme": "default",
            },
            "client": {
                "email": self.partner_email,
            },
        }

        res.update(
            {
                "transaction_id": self.id,
                "culqi_public_key": self.provider_id.culqi_public_key,
                "culqi_config": culqi_config,
            }
        )

        return res

    def _get_tx_from_notification_data(self, provider_code, notification_data):
        """Override of payment to find the transaction based on Culqi data.

        :param str provider_code: The code of the provider that handled the transaction
        :param dict notification_data: The notification data sent by the provider
        :return: The transaction if found
        :rtype: recordset of `payment.transaction`
        :raise: ValidationError if the data match no transaction
        """
        tx = super()._get_tx_from_notification_data(provider_code, notification_data)
        if provider_code != "culqi":
            return tx
        reference, amount = notification_data.get("reference"), notification_data.get(
            "amount"
        )
        if not reference or not amount:
            raise ValidationError(
                "Culqi: "
                + _(
                    "received data with missing reference (%s) or amount (%s)"
                    % (reference, amount)
                )
            )
        tx = self.search(
            [("reference", "=", reference), ("provider_code", "=", "culqi")]
        )
        if not tx or len(tx) > 1:
            error_msg = _("Authorize: received data for reference %s' % reference")
            if not tx:
                error_msg += _("; no order found")
            else:
                error_msg += _("; multiple order found")
            raise ValidationError(error_msg)
        return tx

    def _process_notification_data(self, notification_data):
        """Override of payment to process the transaction based on Culqi data.

        Note: self.ensure_one()

        :param dict notification_data: The notification data sent by the provider
        :return: None
        """
        super()._process_notification_data(notification_data)
        if self.provider_code != "culqi":
            return

        if (
            float_compare(float(notification_data.get("amount", "0.0")), self.amount, 2)
            != 0
        ):
            logging_values = {
                "amount": notification_data.get("amount", "0.0"),
                "total": self.amount,
                "fees": self.fees,
                "reference": self.reference,
            }
            _logger.error(
                "the paid amount (%(amount)s) does not match the total + fees (%(total)s + "
                "%(fees)s) for the transaction with reference %(reference)s",
                logging_values,
            )
            raise ValidationError(
                "Culqi: " + _("The amount does not match the total + fees.")
            )
        if notification_data.get("currency") != self.currency_id.name:
            raise ValidationError(
                "Culqi: "
                + _(
                    "The currency returned by Culqi %(rc)s does not match the transaction "
                    "currency %(tc)s.",
                    rc=notification_data.get("currency"),
                    tc=self.currency_id.name,
                )
            )

        payment_status = notification_data.get("status")
        if payment_status == "done":
            self._set_done()
        else:
            _logger.info(
                "Received data with invalid payment status: %s", payment_status
            )
            self._set_error(
                "Culqi: "
                + _("Received data with invalid payment status: %s", payment_status)
            )
