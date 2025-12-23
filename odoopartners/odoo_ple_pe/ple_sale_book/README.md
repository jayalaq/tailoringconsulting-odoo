# Ple Sale book 

## Summary

This module called “PLE reports” has been created to generate PLE sales reports for which it will contain an object called account.account.tag and will serve to position the information from the sales book in the columns.
It will contain these fields

- Field company_id “Company” of type many2one
- Field date_start “start date” of type date
- Field date_end “end date” of type date
- Field bool_consolidate_pos “Daily POS consolidation? of type boolean
- Field state_send “sending status” of type selection NOTE: This field must be activated when the next module is installed. SEE
- Field date_ple “Generated on” of type date.
- Field xls_binary “excel report” of type binary and this will contain information that will be explained later.
- Field txt_binary “report .TXT” of type binary and this will contain information that will be explained later.

The .txt, .xlsx files must be generated successfully