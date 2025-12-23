/** @odoo-module */

import { _t } from "@web/core/l10n/translation";
import { patch } from "@web/core/utils/patch";
import { ConfirmPopup } from "@point_of_sale/app/utils/confirm_popup/confirm_popup";
import { PaymentScreen } from "@point_of_sale/app/screens/payment_screen/payment_screen";

patch(PaymentScreen.prototype, {
    /**
     * @override
     */
    async validateOrder(isForceValidate) {
        if (!this.currentOrder.is_to_invoice() && this.pos.config.always_move_account) {
            if (!this.currentOrder.get_partner()) {
                const { confirmed } = await this.popup.add(ConfirmPopup, {
                    title: _t("Customer Required"),
                    body: _t("You need to select the customer before you can invoice an order."),
                });
                if (confirmed) {
                    this.selectPartner();
                }
                return;
            }
            this.currentOrder.to_invoice = true;
            this.currentOrder.fake_invoice = true;
        }
        await super.validateOrder(isForceValidate);
    },
});
