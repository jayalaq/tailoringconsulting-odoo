/** @odoo-module */

import { _t } from "@web/core/l10n/translation";
import { patch } from "@web/core/utils/patch";
import { ErrorPopup } from "@point_of_sale/app/errors/popups/error_popup";
import { Order } from "@point_of_sale/app/store/models";

patch(Order.prototype, {
    /**
     * @override
     */
    async pay() {
        const cashier = this.pos.get_cashier();
        if (!cashier.pos_access_make_payments) {
            await this.env.services.popup.add(ErrorPopup, {
                title: _t("Access Denied"),
                body: _t("You do not have access to make payments."),
            });
        } else {
            await super.pay();
        }
    },
});
