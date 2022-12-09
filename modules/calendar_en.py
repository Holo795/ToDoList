import datetime as dt



class Calendar:
    """Class to create a calendar from 2000 to 2100 and get the current day"""
    
    def __init__(self) -> None:
        self.calendar = {}
        self.current_time = self.get_current_day()
        
        self.months = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"]
        self.days = ["Samedi", "Dimanche", "Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi"]
        self.days_loop = 0
        
        for year in range(2000, 2100):
            temp = {}
            for month in range(len(self.months)):
                if self.months[month] == "Février":
                    if year % 4 == 0:
                        temp[self.months[month]] = self.set_days(29)
                    else:
                        temp[self.months[month]] = self.set_days(28)
                
                elif month % 2 == 0:
                    if month < 7:
                        temp[self.months[month]] = self.set_days(31)
                    else:
                        temp[self.months[month]] = self.set_days(30)

                    
                elif month % 2 == 1:
                    if month < 6:
                        temp[self.months[month]] = self.set_days(30)
                    else:
                        temp[self.months[month]] = self.set_days(31)

            self.calendar[year] = temp
        
        self.calendar[self.current_time["year"]][self.months[self.current_time["month"]-1]][self.current_time["day"]][2] = "active"



    def set_days(self, nb_days_per_month:int):
        """Set the days of the month. (Useless for the user)

        Args:
            nb_days_per_month (int): Number of days in the month
            
        Returns:
            var_temp (list): List of days in a month
        """
        var_temp = []
        for day in range(1, nb_days_per_month+1):
            var_temp.append({"nb_jour": day, "jour": self.days[self.days_loop], "type": "inactive", "nb_jour_semaine": self.days_loop})
            self.days_loop += 1
            if self.days_loop == 7:
                self.days_loop = 0
        return var_temp



    def get_all_calendar(self) -> dict:
        """Get the all calendar

        Returns:
            self.calendar (dict): Calendar
        """
        return self.calendar
    
    
    def get_year(self, year:int) -> dict:
        """Get a year
        
        Args:
            year (int): Year (ex: 2000)
            
        Returns:
            self.calendar[year] (dict): Year
        """
        return self.calendar[year]
    
    
    def get_month(self, year, month) -> dict:
        """Get a month from a specific year
        
        Args:
            year (int): Year (ex: 2000)
            month (str): Month (ex: "Janvier")
            
        Returns:
            self.calendar[year][month] (dict): Month
        """
        return self.calendar[year][month]
    
    
    def get_day(self, year, month, day) -> list:
        """Get a day from a specific month form a year
        
        Args:
            year (int): Year (ex: 2000)
            month (str): Month (ex: "Janvier")
            day (int): Day (ex: 1), (ex: 0 for the last day of the month)
            
        Returns:
            self.calendar[year][month][day-1] (dict): Day
        """
        return self.calendar[year][month][day-1]
    
    
    def get_days_from_name(self, year, month, day_name) -> list:
        """Get all days from a specific month form a year with the same name

        Args:
            year (_type_): Year (ex: 2000)
            month (_type_): Month (ex: "Janvier")
            day_name (_type_): Day (ex: "Lundi")

        Returns:
            list: All days
        """
        all_days = []
        for day in self.get_month(year, month):
            if day["jour"] == day_name:
                all_days.append(day)
        return all_days
    
    
    def get_current_day(self, month_in_str=False) -> dict:
        """Get the current day
        
        Returns:
            Dict with the current day, month and year (dict): Current day"""
        if month_in_str:
            months = {1: "Janvier", 2: "Février", 3: "Mars", 4: "Avril", 5: "Mai", 6: "Juin", 7: "Juillet", 8: "Août", 9: "Septembre", 10: "Octobre", 11: "Novembre", 12: "Décembre"}
            return {"year": dt.datetime.now().year, "month": months[dt.datetime.now().month], "day": dt.datetime.now().day}
        return {"year": dt.datetime.now().year, "month": dt.datetime.now().month, "day": dt.datetime.now().day}


if __name__ == "__main__":
    test = Calendar()
    #print(test.get_month(2000, "Janvier"))
    #print(test.get_year(2000))
    #print(test.get_current_day(True))
    print(test.get_day(2022, "Décembre", 9))
    #print(test.get_days_from_name(2022, "Décembre", "Lundi"))
    pass

