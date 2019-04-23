#%%
import csv, os
from inverted_yield_curves.src.yield_curve_day import YieldCurve_Daily
from inverted_yield_curves.src.projection_check import RecessionProjection

series = []
treasury_yield_csv_path = "/home/aparsons/Development/econ_490/irp/inverted_yield_curves/data/daily/Treasury_Yields_from_2002_1mo-30yr.csv"
with open(treasury_yield_csv_path, newline='') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',')
    next(csvreader)
    for row in csvreader:
        yields = []
        for column in row[1:]:
            if str(column) != str("#N/A") and str(column) != "":
                yields.append(float(column))
            else:
                yields.append(None)
        series.append(YieldCurve_Daily(row[0], yields))

#%%
from datetime import date
from datetime import timedelta

maturities = {
    0: timedelta(28), 
    1: timedelta(91), 
    2: timedelta(182),
    3: timedelta(365),
    4: timedelta(730),
    5: timedelta(1095),
    6: timedelta(1825),
    7: timedelta(2555),
    8: timedelta(3650),
    9: timedelta(7300),
    10: timedelta(10950)
}

sub_60 = 0
over_60 = 0

for day in series:
    if day.inversion_periods:
        # TODO: use datetime in YIELD classes
        date_split = day.date.split('-')
        day_date = date(int(date_split[0]), int(date_split[1]), int(date_split[2]))
        # inversion_period = day.inversion_periods[0]
        for index, inversion_period in enumerate(day.inversion_periods):
            inversion_start = inversion_period.inversion_start[0]
            inversion_end = inversion_period.inversion_end[0]
            projected_recession_start = day_date + maturities[inversion_start]
            projected_recession_end = day_date + maturities[inversion_end]
            projected_recession_duration = projected_recession_end-projected_recession_start

            recession_projection = RecessionProjection(day_date, index, projected_recession_start, projected_recession_end)
            
            if abs(recession_projection.start_difference) <= timedelta(65):
                recession_projection.print_report()
                print()
                sub_60 += 1
            else:
                over_60 += 1
print("Correct Predict: " + str(sub_60))
print("False Positives: " + str(over_60))
print("Accuracy: " + str((sub_60/over_60) * 100) + "%")
