/** @odoo-module */

import { patch } from "@web/core/utils/patch";
import { PartnerListScreen } from "@point_of_sale/app/screens/partner_list/partner_list";
import { ErrorPopup } from "@point_of_sale/app/errors/popups/error_popup";
import { useService } from "@web/core/utils/hooks";
import { _t } from "@web/core/l10n/translation";


patch(PartnerListScreen.prototype, {
    setup() {
        super.setup(...arguments)
        this.popup = useService("popup")
    },

    triggerValidation() {
        let validation_rut_obj = document.getElementById('validation-ruc')
        validation_rut_obj.checked = !validation_rut_obj.checked
        this.partnerEditor.save()
        validation_rut_obj.checked = false
    },

    async saveChanges(processedChanges) {
        let validation_rut_obj = document.getElementById('validation-ruc')
        if (validation_rut_obj.checked)
            processedChanges = await this.rucValidationSunat(processedChanges)
        if (processedChanges)
            super.saveChanges(processedChanges)
        validation_rut_obj.checked = false
    },

    async rucValidationSunat(processedChanges) {
        try {
            let partner_values = await this.orm.call("res.partner", "handle_data_sunat", [processedChanges]);
            if (!partner_values) {
                await this.popup.add(ErrorPopup, {
                    title: "UPPS!",
                    body: "No se puede realizar la consulta, porque el servicio de SUNAT está demorando en Responder, o su conexión a Internet es demasiado lenta. Pruebe haciendo la consulta manual directo en la página de consulta RUC de SUNAT, porque si el servicio de SUNAT presenta problemas de lentitud, Odoo no se conectará para evitar afectar el rendimiento del sistema.",
                });
                return processedChanges
            }
            if (partner_values) {
                partner_values.l10n_latam_identification_type_id = processedChanges.l10n_latam_identification_type_id
                return partner_values;
            }
        } catch (error) {
            if (error.message.code < 0) {
                await this.popup.add(ErrorPopup, {
                    title: _t('Offline'),
                    body: _t('Unable to save changes.'),
                });
            } else {
                throw error;
            }
            return processedChanges
        }
    }
});