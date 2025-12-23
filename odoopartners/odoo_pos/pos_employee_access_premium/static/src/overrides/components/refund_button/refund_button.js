/** @odoo-module */

import { _t } from "@web/core/l10n/translation";
import { patch } from "@web/core/utils/patch";
import { useService } from "@web/core/utils/hooks";
import { RefundButton } from "@point_of_sale/app/screens/product_screen/control_buttons/refund_button/refund_button";
import { ErrorPopup } from "@point_of_sale/app/errors/popups/error_popup";

patch(RefundButton.prototype, {
    /**
     * @override
     */
    setup() {
        super.setup(...arguments);
        this.popup = useService("popup");
    },
    /**
     * @override
     */
    click() {
        const cashier = this.pos.get_cashier();
        if (!cashier.pos_access_make_refunds) {
            this.popup.add(ErrorPopup, {
                title: _t("Access Denied"),
                body: _t("You do not have access to make refunds."),
            });
        } else {
            super.click();
        }
    },
});
