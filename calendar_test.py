import datetime
     




class Calendar:
    def __init__(self) -> None:
        self.calendar = {}
        months = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"]
        for year in range(2000, 2100):
            temp = {}
            for month in range(len(months)):
                if months[month] == "Février":
                    if year % 4 == 0:
                        temp[months[month]] = [i for i in range(1, 30)]
                    else:
                        temp[months[month]] = [i for i in range(1, 29)]
                
                elif month % 2 == 0:
                    if month < 7:
                        temp[months[month]] = [i for i in range(1, 32)]
                    else:
                        temp[months[month]] = [i for i in range(1, 31)]

                    
                elif month % 2 == 1:
                    if month < 6:
                        temp[months[month]] = [i for i in range(1, 31)]
                    else:
                        temp[months[month]] = [i for i in range(1, 32)]

            self.calendar[year] = temp


    def get_all_calendar(self):
        return self.calendar
    
    
    def get_year(self, year):
        return self.calendar[year]
    
    
    def get_month(self, year, month):
        return self.calendar[year][month]
    
    
    def get_day(self, year, month, day):
        return self.calendar[year][month][day]
    
    
    def get_current_day(self):
        # TODO
        """# using now() to get current time
        current_time = datetime.datetime.now()
        current_time = [current_time.year, current_time.month, current_time.day]
        print(current_time)"""
        pass

test = Calendar()
print(test.get_year(2000))