from datetime import date, datetime, time, timedelta
import calendar
import os
from Lib.urlget import download_from_url
from Lib.fitsdatetime import DateTimeFitsFile


# Get list of Solar Cycle 24 top flares and save it in the proper directory
cycle24_dir = os.path.join("..", "solar-cycles", "cycle24")
top_flares = download_from_url("http://www.solarham.net/top10.txt", cycle24_dir)

# Parse top_flares data
months = {month_name: month_number for month_number, month_name in enumerate(calendar.month_name)}
with open(top_flares) as f:
    for line in f:
        if line[0:5] not in ["CYCLE", "Compi", "     ", "CLASS", "-----"] and line != '\n':
            line = ' '.join(line.split())
            flare_class = line.split()[0]
            flare_month_name = line.split()[2]
            flare_month_number = months[flare_month_name]
            flare_day = line.split()[3]
            if len(flare_day) == 1:
                flare_day = '0' + flare_day
            flare_year = line.split()[4]
            try:
                peak_time = line.split()[7]
            except IndexError:
                peak_time = None

            if peak_time is not None:
                flare_datetime = datetime(int(flare_year), int(flare_month_number), int(flare_day),
                                          int(peak_time.split(':')[0]), int(peak_time.split(':')[1]))
                # hours_list = get_hours_list(peak_time)
                # print(hours_list)
                flare_datetime_fits = DateTimeFitsFile(flare_datetime)
                flare_datetime_fits.plot_fits_from_date("BLEN5M", True)
                # del flare_datetime_fits
                # plot_fits_from_date(["BLEN5M", "BLENSW", "BLEN7M"], flare_datetime)
            else:
                flare_datetime = datetime(int(flare_year), int(flare_month_number), int(flare_day))
                flare_datetime_fits = DateTimeFitsFile(flare_datetime)
                flare_datetime_fits.plot_fits_from_date("BLEN5M", True)
                # del flare_datetime_fits
                # plot_fits_from_date(["BLEN5M", "BLENSW", "BLEN7M"], flare_year, flare_month_number, flare_day)
                # plot_fits_from_date(["BLEN5M", "BLENSW", "BLEN7M"], flare_datetime)
