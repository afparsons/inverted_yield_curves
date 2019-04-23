
from datetime import date, timedelta
from collections import namedtuple

recessions = {
    (date(1990, 7, 1), date(1991, 3, 1)) : "Early 1990s",
    (date(2001, 3, 1), date(2001, 11, 1)): "Early 2000s",
    (date(2007, 12, 1), date(2009, 6, 1)): "Great Recession"
}

# class Recession:
#     def __init__(self, start, end, label=""):
#         self.recession_start = start
#         self.recession_end = end
#         self.recession_duration = self.recession_end - self.recession_start
#         self.label = label

class RecessionProjection:
    def __init__(self, claim_date, inversion_periods_index, projected_recession_start, projected_recession_end):
        self.claim_date = claim_date
        self.inversion_periods_index = inversion_periods_index
        self.projected_recession_start = projected_recession_start
        self.projected_recession_end = projected_recession_end
        self.projected_recession_duration = self.projected_recession_end - self.projected_recession_start
        
        self.closest_recession = self.find_closest_recession(self.projected_recession_start)
        self.closest_recession_duration = self.closest_recession[0][1] - self.closest_recession[0][0]
     
        self.start_difference = self.closest_recession[0][0] - self.projected_recession_start
        self.end_difference = self.closest_recession[0][1] - self.projected_recession_end
        self.overlap = self.calculate_overlap()

    def __str__(self):
        return "Start Diff: " + str(self.start_difference)

    def print_report(self):
        print("\033[36mYield Curve Date           : " + str(self.claim_date) + "  @  " + str(self.inversion_periods_index))
        print("\033[0mProjected Recession Start  : " + str(self.projected_recession_start))
        print("Projected Recession End    : " + str(self.projected_recession_end))
        print("Proj. Recession Duration   : " + str(self.projected_recession_duration))
        print()
        print("Closest Actual Recession   : " + self.closest_recession[1])
        print("Closest Recession Start    : " + str(self.closest_recession[0][0]))
        print("Closest Recession End      : " + str(self.closest_recession[0][1]))
        print(self.closest_recession[1] + " Duration   : " + str(self.closest_recession_duration))
        print()
        if self.start_difference.days == 0:
            print("\033[32mExact start prediction     : \033[93m" + str(self.start_difference))
        elif abs(self.start_difference.days) <= 31:
            print("\033[32mClose start prediction     : \033[93m" + str(self.start_difference))
        else:
            print("Proj. vs. Actual Start Diff: \033[93m" + str(self.start_difference))
        # print("Proj. vs. Actual Start Diff: " + str(self.start_difference))
        print("\033[0mProj. vs. Actual End Diff  : " + str(self.end_difference))
        print("Projected / Actual Overlap : " + str(self.overlap[0]) + " days")
        if self.overlap[1] < 1:
            percentage = self.overlap[1] * 100
            print("Misaligned Recn Prediction : \033[33m" + str(int(percentage)) + "% coverage")
        elif self.overlap[1] == 1:
            percentage = self.overlap[1] * 100
            print("Totally Encompassing Pred  : \033[33m" + str(int(percentage)) + "% coverage")
        else:
            print("UNKNOWN ERROR!")
        print("\033[0m-----------------------------------------------")

    def find_closest_recession(self, start_date):
        closest = (date(1, 1, 1), date(1, 1, 1))
        for recession in recessions.items():   
            if abs(start_date - recession[0][0]) < abs(start_date - closest[0]):
                closest = recession[0]
        return (closest, recessions[closest])

    def calculate_overlap(self):
        DateTimeRange = namedtuple("DateTimeRange", ["start", "end"])
        projected_recession_range = DateTimeRange(self.projected_recession_start, self.projected_recession_end)
        closest_recession_range = DateTimeRange(self.closest_recession[0][0], self.closest_recession[0][1])
        latest_start = max(projected_recession_range.start, closest_recession_range.start)
        earliest_end = min(projected_recession_range.end, closest_recession_range.end)
        range_delta = (earliest_end - latest_start).days
        overlap_days = max(0, range_delta)
        return (overlap_days, overlap_days/self.closest_recession_duration.days)





