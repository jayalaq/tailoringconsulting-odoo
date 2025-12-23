/** @odoo-module */

import { patch } from "@web/core/utils/patch";
import { Orderline } from "@point_of_sale/app/generic_components/orderline/orderline";
import { UomOrderlinePopup } from "@pos_multi_uom_product_right/apps/uom_orderline_popup/uom_orderline_popup";
import { usePos } from "@point_of_sale/app/store/pos_hook";

patch(Orderline.prototype, {
    props: {
        ...Orderline.props,
        line: {
            shape: {
                has_multi_uom: { type: Boolean, optional: true },
            },
        },
    },
    setup() {
        super.setup();
        this.pos = usePos();
    },
    async changeUomLine() {
        const order = this.pos.get_order();
        const orderline = order.get_selected_orderline();
        const lines_all_units = this.pos.units;
        const data = [];
        const price = orderline.price * orderline.get_unit().factor;
        const product = orderline.product;

        lines_all_units.forEach(line => {
            if (orderline.get_unit().category_id[0] === line.category_id[0]) {
                if (product.show_all_uom) {
                    line.price = price / line.factor;
                    data.push(line);
                } else if (product.allow_uoms.includes(line.id)) {
                    line.price = price / line.factor;
                    data.push(line);
                }
            }
        });

        await this.env.services.popup.add(UomOrderlinePopup, {
            title: "Seleccionar unidad de medida",
            confirmText: 'Cancelar',
            orderline_allow_uoms: data,
            product: product,
        });
    },
});
