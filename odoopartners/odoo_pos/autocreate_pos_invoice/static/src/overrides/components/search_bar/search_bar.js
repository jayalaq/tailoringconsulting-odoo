/** @odoo-module */

import { onMounted } from "@odoo/owl";
import { patch } from "@web/core/utils/patch";
import { SearchBar } from "@point_of_sale/app/screens/ticket_screen/search_bar/search_bar";

patch(SearchBar.prototype, {
    /**
     * @override
     */
    setup() {
        super.setup();
        onMounted(this.onMounted);
    },
    onMounted() {
        this.state.searchInput = "";
    },
});
