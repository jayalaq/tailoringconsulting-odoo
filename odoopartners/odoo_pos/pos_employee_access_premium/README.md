# POS Employee Access Premium

## Summary

This module extends the base HR employee model to include access controls for various Point of Sale (POS) functionalities.

It introduces the following fields to manage POS permissions:

- Access Close POS: Indicates whether the employee has permission to close the POS.
- Access Make Payments: Controls whether the employee can make payments through the POS.
- Access Make Refunds: Determines if the employee can make refunds through the POS.
- Access Make Discounts: Indicates if the employee can apply discounts during a POS transaction.
- Access Change Price: Controls whether the employee can change prices during a POS transaction.
- Access Delete Orders: Determines if the employee can delete complete transactions (orders) in the POS.
- Access Delete Order Lines: Indicates if the employee has permission to delete individual lines of an order in the POS.
- Access Decrease Quantity Order Lines: Controls whether the employee can decrease the quantity of products or services in a POS order line.
- Access Cash In/Out: Determines if the employee has authorization to perform cash in/out operations in the POS.
- Access Product Information: Indicates whether the employee has access to detailed product information in the POS.

By default, all employees have these permissions enabled.
