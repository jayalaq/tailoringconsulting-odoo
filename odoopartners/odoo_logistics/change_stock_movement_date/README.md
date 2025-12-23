# Change stock movement date

## Summary

Allows you to enter an "effective date" of the transfer that will be used to record the proof of delivery, instead of the date on which it is validated. Without this module, Odoo always takes the validation date. It also creates the "accounting date" field in the "Stock Movements" and in the "Product Movements".

The “Effective Date” field is a native Odoo field, now what this module will do is make this “Effective Date” field visible with the technical name “date_note” in the “stock.picking” model.
