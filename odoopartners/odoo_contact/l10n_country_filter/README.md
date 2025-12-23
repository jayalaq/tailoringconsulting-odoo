# L10n Country Filter

## Summary

This module introduces a dynamic mechanism to control the visibility of specific XML tags within partner views based on the country of the current company. The functionality is implemented in the ResPartner model.

Features:

- Allows customization of XML tag visibility in partner views.
- Tags are made invisible in the XML arch based on the current company's country and specified criteria.

Usage:

1. Specify the target tags and their criteria in the ResPartner._tags_invisible_per_country method.
2. Tags are made invisible in the XML arch if the current company's country does not match the specified criteria.

Example:

Assuming ```tags = ['ubigeo', ('group', 'extended_info')]```, ```countries = [self.env.ref('base.pe')]```,
and the current company's country is 'Peru', the function will modify the arch XML to make
elements with Xpath queries ```"//field[@name='ubigeo']"``` and ```"//group[@name='extended_info']"```
invisible.

Note: Ensure proper configuration and understanding of the XML structure before customization.
