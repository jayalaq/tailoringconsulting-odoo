/** @odoo-module */

import { patch } from "@web/core/utils/patch";
import { PartnerDetailsEdit } from "@point_of_sale/app/screens/partner_list/partner_editor/partner_editor";


patch(PartnerDetailsEdit.prototype, {
    saveChanges() {
        let validation_rut_obj = document.getElementById('validation-ruc')
        if (validation_rut_obj.checked)
            this.changes.name = "name"
        super.saveChanges(...arguments)
    }
});
