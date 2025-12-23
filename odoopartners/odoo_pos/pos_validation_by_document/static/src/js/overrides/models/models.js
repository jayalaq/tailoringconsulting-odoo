/** @odoo-module */

import { patch } from "@web/core/utils/patch";
import { PosStore } from "@point_of_sale/app/store/pos_store";

patch(PosStore.prototype, {
    /**
     * @override
     */
    async _processData(loadedData) {
        await super._processData(...arguments);
        this.l10n_latam_identification_types = loadedData['l10n_latam.identification.type'];
    },
});
