/** @odoo-module */

import { patch } from "@web/core/utils/patch";
import { PaymentScreen } from "@point_of_sale/app/screens/payment_screen/payment_screen";

patch(PaymentScreen.prototype, {
    /**
     * @override
     */
    toggleIsToInvoice() {
        this.currentOrder.setL10nLatamDocumentTypeId(false);
        super.toggleIsToInvoice();
    },
    onChangeL10nLatamDocumentTypeId(event) {
        const value = event.target && $(event.target).val() ? parseInt($(event.target).val()) : false;
        this.currentOrder.setL10nLatamDocumentTypeId(value);
    },
});
