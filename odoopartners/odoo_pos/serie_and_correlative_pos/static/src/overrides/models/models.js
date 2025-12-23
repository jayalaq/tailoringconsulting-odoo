/** @odoo-module */

import { patch } from "@web/core/utils/patch";
import { PosStore } from "@point_of_sale/app/store/pos_store";
import { Order } from "@point_of_sale/app/store/models";

patch(PosStore.prototype, {
    /**
     * @override
     */
    async _processData(loadedData) {
        await super._processData(loadedData);
        this.document_type_ids = loadedData["l10n_latam.document.type"];
    },
    /**
     * @override
     */
    push_single_order(order) {
        order.configureL10nLatamDocumentTypeId();
        order.configureL10nLatamJournalId();
        return super.push_single_order(order);
    },
    filterDocumentTypeByMove(records, documentTypeIds) {
        let filter_ids = [];
        for (let rec in records) {
            for (let doc in documentTypeIds) {
                if (records[rec] === documentTypeIds[doc]["id"]) {
                    filter_ids.push({
                        "id": documentTypeIds[doc]["id"],
                        "internal_type": documentTypeIds[doc]["internal_type"],
                        "name": documentTypeIds[doc]["name"]
                    })
                }
            }
        }
        return filter_ids;
    },
    getInvoiceTypeDocumentIds() {
        return this.filterDocumentTypeByMove(
            this.config.invoice_l10n_latam_document_type_ids,
            this.document_type_ids
        );
    },
    getTicketTypeDocumentIds() {
        return this.filterDocumentTypeByMove(
            this.config.ticket_l10n_latam_document_type_ids,
            this.document_type_ids
        );
    },
});

patch(Order.prototype, {
    /**
     * @override
     */
    init_from_JSON(json) {
        super.init_from_JSON(json);
        this.l10n_latam_document_type_id = json.l10n_latam_document_type_id || false;
        this.l10n_latam_journal_id = json.l10n_latam_journal_id || false;
    },
    /**
     * @override
     */
    export_as_JSON() {
        const json = super.export_as_JSON();
        json.l10n_latam_document_type_id = this.l10n_latam_document_type_id || false;
        json.l10n_latam_journal_id = this.l10n_latam_journal_id || false;
        return json;
    },
    /**
     * @override
     */
    export_for_printing() {
        const receipt = super.export_for_printing();
        receipt.l10n_latam_document_type_id = this.l10n_latam_document_type_id || false;
        receipt.l10n_latam_journal_id = this.l10n_latam_journal_id || false;
        return receipt;
    },
    setL10nLatamDocumentTypeId(l10n_latam_document_type_id) {
        this.l10n_latam_document_type_id = l10n_latam_document_type_id;
    },
    configureL10nLatamDocumentTypeId() {
        if (this.is_to_invoice() && !this.is_fake_invoice()) {
            const documentIds = this.pos.getInvoiceTypeDocumentIds();
            if (documentIds.length > 0 && !this.l10n_latam_document_type_id) {
                this.l10n_latam_document_type_id = parseInt($("#invoice_l10n_latam_document_type_ids").val());
            }
        } else {
            const documentIds = this.pos.getTicketTypeDocumentIds();
            if (documentIds.length > 0 && !this.l10n_latam_document_type_id) {
                this.l10n_latam_document_type_id = parseInt($("#ticket_l10n_latam_document_type_ids").val());
            }
        }
    },
    configureL10nLatamJournalId() {
        if (this.is_to_invoice() && !this.is_fake_invoice()) {
            this.l10n_latam_journal_id = this.pos.config.invoice_journal_id[0];
        } else {
            this.l10n_latam_journal_id = this.pos.config.ticket_journal_id[0];
        }
    },
});
