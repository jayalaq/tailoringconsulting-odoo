/** @odoo-module */

import { AbstractAwaitablePopup } from "@point_of_sale/app/popup/abstract_awaitable_popup";
import { useState } from "@odoo/owl";
import { usePos } from "@point_of_sale/app/store/pos_hook";

export class UomOrderlinePopup extends AbstractAwaitablePopup {
    static template = "pos_multi_uom_product_right.UomOrderlinePopup";

    setup() {
        super.setup();
        this.pos = usePos();
        this.state = useState({
            selectedUom: null
        });
    }

    async _clickUom(uom) {
        const order = this.pos.get_order();
        const orderline = order.get_selected_orderline();

        if (orderline && uom) {
            orderline.set_unit_price(uom.price);
            orderline.set_product_uom(uom.id);
            await this.confirm();
        }
    }
}
