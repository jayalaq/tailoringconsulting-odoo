/** @odoo-module */

import { onMounted } from "@odoo/owl";
import { patch } from "@web/core/utils/patch";
import { SaleOrderManagementControlPanel } from "@pos_sale/app/order_management_screen/sale_order_management_control_panel/sale_order_management_control_panel";

patch(SaleOrderManagementControlPanel.prototype, {
    /**
     * @override
     */
    setup() {
        super.setup();
        onMounted(this.onMounted);
    },
    onMounted() {
        this.pos.orderManagement.searchString = "";
        this.saleOrderFetcher.setSearchDomain(this._computeDomain());
    },
});
