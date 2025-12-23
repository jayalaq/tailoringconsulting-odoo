/** @odoo-module **/

import { _t } from "@web/core/l10n/translation";
import { patch } from "@web/core/utils/patch";
import { ProductsWidget } from "@point_of_sale/app/screens/product_screen/product_list/product_list";
import { ErrorPopup } from "@point_of_sale/app/errors/popups/error_popup";

patch(ProductsWidget.prototype, {
    /**
     * @override
     */
    async onProductInfoClick(product) {
        const cashier = this.pos.get_cashier();
        if (!cashier.pos_access_product_information) {
            await this.popup.add(ErrorPopup, {
                title: _t("Access Denied"),
                body: _t("You do not have access to product information."),
            });
        } else {
            await super.onProductInfoClick(product);
        }
    },
});
