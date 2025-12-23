# Additional Fields Employee

## Summary

This module has been created with the purpose of improving the management of employees' personal information by allowing the assignment of the health, disability and work status regime that corresponds to them, with the aim of offering greater flexibility in data collection.

This module introduces the following fields into the model employee file 'hr.employee':

- health_regime_id : It will be of type Many2one where a relationship with all the health regimens registered in the 'health.regime' model is displayed.
- disability : It will be of type Boolean.

In the employee contract, model 'hr.contract' creates the following fields:

- labor_regime_id
- labor_condition_id
- work_occupation_id
- maximum_working_day
- atypical_cumulative_day
- nocturnal_schedule
- unionized
- is_practitioner