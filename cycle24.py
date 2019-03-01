import os
from lib.urlget import download_from_url


def get_start_time(time):
    hours_str = time.split(':')[0]
    minutes = int(time.split(':')[1])
    if 0 <= minutes < 15:
        time_str = hours_str + "00"
    elif 15 <= minutes < 30:
        time_str = hours_str + "15"
    elif 30 <= minutes < 45:
        time_str = hours_str + "30"
    else:
        time_str = hours_str + "45"

    return time_str


def plot_fits_from_date(spectrograph, year, month, day, start_time=''):
    data_archives = "http://soleil80.cs.technik.fhnw.ch/solarradio/data/2002-20yy_Callisto"
    date_url = '/'.join([data_archives, year, month, day])
    date_url_index = download_from_url(date_url)
    datetime_str = year + month + day + '_' + start_time
    fits_href = 'href="{}_{}'.format(spectrograph, datetime_str)
    with open(date_url_index) as index:
        for item in index:
            if fits_href in item:
                print(item)
    os.remove(date_url_index)


# Get list of Solar Cycle 24 top flares and save it in the proper directory
cycle24_dir = os.path.join("solar-cycles", "cycle24")
top_flares = download_from_url("http://www.solarham.net/top10.txt", cycle24_dir)

# Parse top_flares data
months = {"January": "01", "February": "02", "March": "03", "April": "04", "May": "05", "June": "06", "July": "07",
          "August": "08", "September": "09", "October": "10", "November": "11", "December": "12"}

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
                start_time_str = get_start_time(peak_time)
                plot_fits_from_date("BLENSW", flare_year, flare_month_number, flare_day, start_time_str)
            else:
                plot_fits_from_date("BLENSW", flare_year, flare_month_number, flare_day)
