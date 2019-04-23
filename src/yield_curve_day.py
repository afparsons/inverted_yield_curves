# TODO: Convert to datetime
from numpy import diff

class InversionPeriod_Daily:
    def __init__(self, date, start, end):
        assert isinstance(start, tuple)
        assert isinstance(end, tuple)
        self.date = date
        self.inversion_start = start
        self.inversion_end = end
    def __str__(self):
        return "Inversion Period: " + str(self.inversion_start) + " -- " + str(self.inversion_end) 

class YieldCurve_Daily:
    def __init__(self, date, yields):
        self.date = date
        self.yields = yields
        self.inversion_periods = self.find_inversion_periods()
    def __str__(self):
        if len(self.inversion_periods) == 0:
            return str(self.date) + " | No Inversions"
        else:
            inversion_string = ""
            for inversion_period in self.inversion_periods:
                inversion_string += "[Start: " + str(inversion_period.inversion_start) + " ]"
            return str(self.date) + " | " + inversion_string

    def find_inversion_periods(self):
        assert len(self.yields) > 1, "Too few maturity yield values"
        inversion_periods = []
        tupled = [(i,j) for (i,j) in enumerate(self.yields)]
        diffed = list(zip([tup[0] for tup in tupled if tup[1] != None], diff([tup[1] for tup in tupled if tup[1] != None])))
        for i, diff_tup in enumerate(diffed):
            if diff_tup[1] < 0:
                for j in range(i+1, len(diffed)-1):
                    if diffed[j] > diffed[j-1]:
                        inversion_periods.append(InversionPeriod_Daily("date", (diffed[i][0], self.yields[diffed[i][0]]), (diffed[j][0], self.yields[diffed[j][0]])))
                        break
        return inversion_periods
    
    # def old_find_inversion_periods(self):
    #     length = len(self.yields)
    #     assert length > 1, "Too few maturity yield values"
    #     maxima_indices = []
    #     minima_indices = []
    #     inversion_periods = []
    #     if length > 1:
    #         if self.yields[0] > self.yields[1]:
    #             maxima_indices.append(0)
    #             for j in range(1, length-1):
    #                 # print("<" + str(j) + ", " + str(self.yields[j]) + ">")
    #                 if self.yields[j] > self.yields[j-1]:
    #                     minima_indices.append(j-1)
    #                     inversion_periods.append(InversionPeriod_Daily("date", (0, self.yields[0]), (j-1, self.yields[j-1])))
    #                     break
    #         if length > 3:
    #             for i in range(1, length-1):
    #                 if self.yields[i] >= self.yields[i-1] and self.yields[i] > self.yields[i+1]:
    #                     maxima_indices.append(i)
    #                     for j in range(i+1, length-1):
    #                         # print("<" + str(j) + ", " + str(self.yields[j]) + ">")
    #                         if self.yields[j] > self.yields[j-1]:
    #                             minima_indices.append(j-1)
    #                             inversion_periods.append(InversionPeriod_Daily("date", (i, self.yields[i]), (j-1, self.yields[j-1])))
    #                             break
    #     # print("Maxima: " + str(maxima_indices))
    #     # print("Minima: " + str(minima_indices))
    #     return inversion_periods