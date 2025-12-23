/** @odoo-module */

import { PaymentScreen } from "@point_of_sale/app/screens/payment_screen/payment_screen";
import { patch } from "@web/core/utils/patch";
import { _t } from "@web/core/l10n/translation";
import { ErrorPopup } from "@point_of_sale/app/errors/popups/error_popup";

patch(PaymentScreen.prototype, {

	setup() {
		super.setup();
		this.auto_invoice();
    },

	auto_invoice(){
		let self =this;
		let config = self.pos.config;
		let order = self.pos.get_order();
		if(config.auto_invoice) {
			order.set_to_invoice(true);
			self.render(true);
		}
	},

	shouldDownloadInvoice() {
        if (this.pos.config.stop_invoice_print) {
        	return false;
        } else {
            return super.shouldDownloadInvoice(); 
        }
    },


	
});


