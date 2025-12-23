# Struct Rules Days

## Summary

This module has been designed with the purpose of extending the configuration actions in the hr.payroll.structure model by adding a many2many type field called "Days Rules" (struct_days_ids).

The objective is to filter the lines of the "Days worked and entries" by removing the lines defined in the struct_days_ids field at the time of executing the payroll.
