/** @odoo-module */

import { _t } from "@web/core/l10n/translation";
import { patch } from "@web/core/utils/patch";
import { parseFloat } from "@web/views/fields/parsers";
import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";
import { ErrorPopup } from "@point_of_sale/app/errors/popups/error_popup";

patch(ProductScreen.prototype, {
    /**
     * @override
     */
    _setValue(val) {
        if (this._validateAccessPermisionCashier(val)) {
            super._setValue(val);
        }
    },
    _validateAccessPermisionCashier(val) {
        const { numpadMode } = this.pos;
        const keyboard = this.numberBuffer.eventsBuffer[0]?.detail.key || '';
        const keyboardDisallow = ["Backspace", "Delete"];
        const cashier = this.pos.get_cashier();
        const order = this.pos.get_order();
        const selectedLine = order.get_selected_orderline();

        if (!cashier.pos_access_decrease_quantity_order_lines && (keyboardDisallow.includes(keyboard) || (selectedLine && numpadMode === "quantity" && selectedLine.quantity > parseFloat(val)))) {
            this.popup.add(ErrorPopup, {
                title: _t("Access Denied"),
                body: _t("You do not have access to decrease the quantity on order lines."),
            });
        } else if (!cashier.pos_access_delete_order_lines && val === "remove" && numpadMode === "quantity") {
            this.popup.add(ErrorPopup, {
                title: _t("Access Denied"),
                body: _t("You do not have access to delete order lines."),
            });
        } else if (!cashier.pos_access_make_discounts && numpadMode === "discount") {
            this.popup.add(ErrorPopup, {
                title: _t("Access Denied"),
                body: _t("You do not have access to make discounts"),
            });
        } else if (!cashier.pos_access_change_price && numpadMode === "price") {
            this.popup.add(ErrorPopup, {
                title: _t("Access Denied"),
                body: _t("You do not have access to change the price."),
            });
        } else {
            return true;
        }
        return false;
    },
});
