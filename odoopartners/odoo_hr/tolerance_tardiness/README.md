# Tolerance Tardiness

## Summary

This module creates a field called 'Tolerance Time' (tolerance_time) of type Integer in the employee's work schedule. This field allows you to specify the tolerance time in minutes that the employee has before their minutes are considered late.

This module creates a field called 'Tardiness' (tardiness) of type Char in the attendance section. This field is calculated based on the employee's check-in time, subtracting the scheduled time based on their work schedule for the specific day and adding the established tolerance time. The result is displayed if the elapsed time exceeds the allowed tolerance.
