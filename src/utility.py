import datetime

from typing import Tuple


def find_the_adjusted_final_trading_date_of_the_quarter() -> Tuple[str, str]:
    datetime_today = datetime.date.today()
    year_today, month_today = datetime_today.year, datetime_today.month
                    
    if month_today <= 3: # Last quarter of the previous year
        the_final_trading_date_of_the_quarter = datetime.date(year_today - 1, 12, 31)
    elif month_today <= 6: # First quarter of the current year
        the_final_trading_date_of_the_quarter = datetime.date(year_today, 3, 31)
    elif month_today <= 9: # Second quarter of the current year
        the_final_trading_date_of_the_quarter = datetime.date(year_today, 6, 30)
    else: # Third quarter of the current year
        the_final_trading_date_of_the_quarter = datetime.date(year_today, 9, 30)

    # Check if the last day is a workday
    if the_final_trading_date_of_the_quarter.weekday() == 5:  # Adjust Saturday (5) or Sunday (6) to their previous Friday
        the_final_trading_date_of_the_quarter -= datetime.timedelta(days=the_final_trading_date_of_the_quarter.weekday() - 4)

    # Calculate the day before the last day
    the_date_before_the_final_trading_date_of_the_quarter = the_final_trading_date_of_the_quarter - datetime.timedelta(days=1)

    return the_final_trading_date_of_the_quarter.strftime('%Y-%m-%d'), the_date_before_the_final_trading_date_of_the_quarter.strftime('%Y-%m-%d')
