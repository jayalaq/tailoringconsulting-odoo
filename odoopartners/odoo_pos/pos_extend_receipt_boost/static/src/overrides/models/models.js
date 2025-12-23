/** @odoo-module */

import { Order } from "@point_of_sale/app/store/models";
import { patch } from "@web/core/utils/patch";
import { PosStore } from "@point_of_sale/app/store/pos_store";

patch(PosStore.prototype, {
    
   getReceiptHeaderData(order) {
        const result = super.getReceiptHeaderData(...arguments);
        result.is_order_number = this.config.order_number;
        result.is_customer_details = this.config.customer_details;
        result.is_customer_name = this.config.customer_name;
        result.customer_address = this.config.customer_address;
        result.customer_mobile = this.config.customer_mobile;
        result.customer_phone = this.config.customer_phone;
        result.customer_email = this.config.customer_email;
        result.customer_vat = this.config.customer_vat;
        result.invoice_number = this.config.invoice_number;
        result.order_barcode = this.config.order_barcode;
        result.barcode_selection = this.config.barcode_selection;
        result.order= order;

        result.customer_name_custom_title = this.config.customer_name_custom_title;
        result.customer_address_custom_title = this.config.customer_address_custom_title;
        result.customer_mobile_custom_title = this.config.customer_mobile_custom_title;
        result.customer_phone_custom_title = this.config.customer_phone_custom_title;
        result.customer_email_custom_title = this.config.customer_email_custom_title;
        result.customer_vat_custom_title = this.config.customer_vat_custom_title;

        result.font_size = this.config.font_size;
        result.is_bold = this.config.bold_format

        if (order?.uid) {
            var barcode = '/report/barcode/Code128/' + order.uid;
            result.barcode= barcode;
            var qrcode = '/report/barcode/QR/' + order.uid;
            result.qrcode = qrcode;
        }
        return result;
    }
});



patch(Order.prototype, {
    setup() {
        super.setup(...arguments);
        this.invoice_number = this.invoice_number || false;
    },
    set_invoice_number(invoice_number){
        this.invoice_number = invoice_number;
    },
    get_invoice_number(){
        return this.invoice_number;
    },
    export_as_JSON() {
        const json = super.export_as_JSON(...arguments);
        json.invoice_number = this.get_invoice_number() || false;
        return json;
    },
    init_from_JSON(json) {
        super.init_from_JSON(...arguments);
        this.invoice_number = json.invoice_number || false;
    },
    export_for_printing() {
        const json = super.export_for_printing(...arguments);
        json.invoice_number = this.get_invoice_number() || 0;
        return json;
    },
});
