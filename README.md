# Inverted Yield Curves

*ECON 490: Financial Frictions and Monetary Policy*

*Individual Research Project*

## Description

This program calculates all partially inverted yield curves over a given time span.

Each inversion is considerted to be a predicted "recessionary window". For example, if the yield curve from a given date has a negative slope for 3-month, 6-month, and 1-year Treasury bills, then that is treated as a prediction of a recession starting on `DATE + (3 months)` and ending on `DATE + (1 year)`.

## Files

| File                 | Description                                                                                                                                                                                                                                              | Status |
|----------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------|
| yield_curve_day.py   | Defines the `InversionPeriod_Daily` class containing a date, and the inversion start and end dates. Defines the `YieldCurve_Daily` class containing a date, the yield rates, the inversion periods, and a function to find the inversion periods.        |        |
| yield_curve_month.py | Defines the `InversionPeriod_Monthly` class containing a date, and the  inversion start and end dates. Defines the `YieldCurve_Monthly` class  containing a date, the yield rates, the inversion periods, and a  function to find the inversion periods. |        |
| projection_check.py  | Defines the `RecessionProjection` class containing inversion period information. Calculates alignment with the nearest actual recession.                                                                                                                 |        |
| daily_yields.py      | Loads data from CSV, creates a list of YieldCurve_Day objects, and determines if there are projected recessions.                                                                                                                                         |        |
| monthly_yields.oy    | Loads data from CSV, creates a list of YieldCurve_Month objects, and determines if there are projected recessions.                                                                                                                                       |        |


## Directories

| Directory | Items                          | Status |
|-----------|--------------------------------|--------|
| src       | Python source files            |        |
| data      | Data sources as CSV; from FRED |        |
| output    | Program output                 |        |



