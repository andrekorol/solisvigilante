from datetime import datetime, timedelta
import calendar
import os
import shutil
import multiprocessing as mp
import gc
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Lib.urlget import download_from_url
import Lib.fitsread


def plot_fits_from_date(fits_file_obj, fits_filepath,  year, month, day, instrument_name):
    fits_file_obj.set_hdul_dataset()
    fits_file_obj.plot_db_above_background()
    fits_file_obj.delete_file()
    plot_filename = fits_filepath.split(os.sep)[-1].replace(".fit.gz", ".png")
    src_plot_path = fits_filepath.replace(".fit.gz", ".png")
    dst_path = os.sep.join([os.getcwd(), year, month, day, instrument_name])
    dst_plot_path = os.path.join(dst_path, plot_filename)
    if not os.path.exists(dst_path):
        os.makedirs(dst_path)
    shutil.move(src_plot_path, dst_plot_path)


# Get list of Solar Cycle 24 top flares and save it in the proper directory
# cycle24_dir = os.path.join("..", "solar-cycles", "cycle24")
# top_flares = download_from_url("http://www.solarham.net/top10.txt", cycle24_dir)
second_half_top_flares = "second_half_top_flares.txt"
data_archives = "http://soleil80.cs.technik.fhnw.ch/solarradio/data/2002-20yy_Callisto"

# Parse top_flares data
months = {month_name: month_number for month_number, month_name in enumerate(calendar.month_name)}
if __name__ == '__main__':
    # with open(setop_flares) as f:
    with open(second_half_top_flares) as f:
        for line in f:
            if line[0:5] not in ["CYCLE", "Compi", "     ", "CLASS", "-----"] and line != '\n':
                line = ' '.join(line.split())
                flare_class = line.split()[0]
                flare_month_name = line.split()[2]
                flare_month_number = str(months[flare_month_name])
                if len(flare_month_number) == 1:
                    flare_month_number = '0' + flare_month_number
                flare_day = line.split()[3]
                if len(flare_day) == 1:
                    flare_day = '0' + flare_day
                flare_year = line.split()[4]
                try:
                    peak_time = line.split()[7]
                except IndexError:
                    peak_time = None

                if peak_time is None:
                    date_url = '/'.join([data_archives, flare_year, flare_month_number, flare_day])
                    date_url_index = download_from_url(date_url)
                    date_str = flare_year + flare_month_number + flare_day
                    with open(date_url_index) as index:
                        for item in index:
                            for instrument in ["BLEN5M", "BLENSW", "BLEN7M"]:
                                if item.find(instrument + '_' + date_str) != -1:
                                    fits_url = '/'.join(
                                        [date_url, item[item.find(instrument + '_' + date_str):item.find(".gz") + 3]])
                                    fits_file_path = download_from_url(fits_url)
                                    fits_filename = fits_file_path.split(os.sep)[-1]
                                    fits_file = Lib.fitsread.ECallistoFitsFile(fits_filename)
                                    fits_file.set_file_path()
                                    try:
                                        proc = mp.Process(target=plot_fits_from_date(fits_file, fits_file_path,
                                                                                     flare_year, flare_month_number,
                                                                                     flare_day, instrument))
                                        proc.daemon = True
                                        proc.start()
                                        proc.join()
                                        del proc
                                    except Exception as e:
                                        print(e)
                                        pass
                                    finally:
                                        try:
                                            fits_file.delete_file()
                                            del fits_url, fits_file_path, fits_filename, fits_file
                                            gc.collect()
                                        except Exception as exception:
                                            print(exception)
                                            try:
                                                del fits_url, fits_file_path, fits_filename, fits_file
                                                gc.collect()
                                            except Exception as exception:
                                                print(exception)
                    del date_url, date_str
                    gc.collect()
                    try:
                        os.remove(date_url_index)
                    except Exception as e:
                        print(e)
                        pass
                    del date_url_index
                    gc.collect()
                else:
                    flare_hour, flare_minute = peak_time.split(':')

                    flare_peak_datetime = datetime(int(flare_year), int(flare_month_number), int(flare_day),
                                                   int(flare_hour), int(flare_minute))

                    prev_hour_datetime = flare_peak_datetime - timedelta(hours=1)
                    next_hour_datetime = flare_peak_datetime + timedelta(hours=1)

                    flare_peak_hour = str(flare_peak_datetime.time().hour)
                    if len(flare_peak_hour) == 1:
                        flare_peak_hour = '0' + flare_peak_hour

                    prev_year = str(prev_hour_datetime.year)
                    prev_month = str(prev_hour_datetime.month)
                    if len(prev_month) == 1:
                        prev_month = '0' + prev_month
                    prev_day = str(prev_hour_datetime.day)
                    if len(prev_day) == 1:
                        prev_day = '0' + prev_day
                    prev_hour = str(prev_hour_datetime.time().hour)
                    if len(prev_hour) == 1:
                        prev_hour = '0' + prev_hour

                    next_year = str(next_hour_datetime.year)
                    next_month = str(next_hour_datetime.month)
                    if len(next_month) == 1:
                        next_month = '0' + next_month
                    next_day = str(next_hour_datetime.day)
                    if len(next_day) == 1:
                        next_day = '0' + next_day
                    next_hour = str(next_hour_datetime.time().hour)
                    if len(next_hour) == 1:
                        next_hour = '0' + next_hour

                    prev_date_url = '/'.join([data_archives, prev_year, prev_month, prev_day])
                    prev_date_url_index = download_from_url(prev_date_url)
                    prev_date_str = prev_year + prev_month + prev_day + '_' + prev_hour
                    with open(prev_date_url_index) as prev_index:
                        for item in prev_index:
                            for instrument in ["BLEN5M", "BLENSW", "BLEN7M"]:
                                if item.find(instrument + '_' + prev_date_str) != -1:
                                    fits_url = '/'.join(
                                        [prev_date_url, item[item.find(instrument + '_' +
                                                                       prev_date_str):item.find(".gz") + 3]])
                                    fits_file_path = download_from_url(fits_url)
                                    fits_filename = fits_file_path.split(os.sep)[-1]
                                    fits_file = Lib.fitsread.ECallistoFitsFile(fits_filename)
                                    fits_file.set_file_path()
                                    try:
                                        proc = mp.Process(target=plot_fits_from_date(fits_file, fits_file_path,
                                                                                     prev_year, prev_month, prev_day,
                                                                                     instrument))
                                        proc.daemon = True
                                        proc.start()
                                        proc.join()
                                        del proc
                                    except Exception as e:
                                        print(e)
                                        pass
                                    finally:
                                        try:
                                            fits_file.delete_file()
                                            del fits_url, fits_file_path, fits_filename, fits_file
                                            gc.collect()
                                        except Exception as exception:
                                            print(exception)
                                            try:
                                                del fits_url, fits_file_path, fits_filename, fits_file
                                                gc.collect()
                                            except Exception as exception:
                                                print(exception)
                    del prev_date_url, prev_date_str
                    gc.collect()
                    try:
                        os.remove(prev_date_url_index)
                    except Exception as e:
                        print(e)
                        pass
                    del prev_date_url_index
                    gc.collect()

                    flare_peak_url = '/'.join([data_archives, flare_year, flare_month_number, flare_day])
                    flare_peak_url_index = download_from_url(flare_peak_url)
                    flare_peak_date_str = flare_year + flare_month_number + flare_day + '_' + flare_peak_hour
                    with open(flare_peak_url_index) as flare_peak_index:
                        for item in flare_peak_index:
                            for instrument in ["BLEN5M", "BLENSW", "BLEN7M"]:
                                if item.find(instrument + '_' + flare_peak_date_str) != -1:
                                    fits_url = '/'.join(
                                        [flare_peak_url, item[item.find(instrument + '_' +
                                                                        flare_peak_date_str):item.find(".gz") + 3]])
                                    fits_file_path = download_from_url(fits_url)
                                    fits_filename = fits_file_path.split(os.sep)[-1]
                                    fits_file = Lib.fitsread.ECallistoFitsFile(fits_filename)
                                    fits_file.set_file_path()
                                    try:
                                        proc = mp.Process(target=plot_fits_from_date(fits_file, fits_file_path,
                                                                                     flare_year, flare_month_number,
                                                                                     flare_day, instrument))
                                        proc.daemon = True
                                        proc.start()
                                        proc.join()
                                        del proc
                                    except Exception as e:
                                        print(e)
                                        pass
                                    finally:
                                        try:
                                            fits_file.delete_file()
                                            del fits_url, fits_file_path, fits_filename, fits_file
                                            gc.collect()
                                        except Exception as exception:
                                            print(exception)
                                            try:
                                                del fits_url, fits_file_path, fits_filename, fits_file
                                                gc.collect()
                                            except Exception as exception:
                                                print(exception)
                    del flare_peak_url, flare_peak_date_str
                    gc.collect()
                    try:
                        os.remove(flare_peak_url_index)
                    except Exception as e:
                        print(e)
                        pass
                    del flare_peak_url_index
                    gc.collect()

                    next_date_url = '/'.join([data_archives, next_year, next_month, next_day])
                    next_date_url_index = download_from_url(next_date_url)
                    next_date_str = next_year + next_month + next_day + '_' + next_hour
                    with open(next_date_url_index) as next_index:
                        for item in next_index:
                            for instrument in ["BLEN5M", "BLENSW", "BLEN7M"]:
                                if item.find(instrument + '_' + next_date_str) != -1:
                                    fits_url = '/'.join(
                                        [next_date_url, item[item.find(instrument + '_' +
                                                                       next_date_str):item.find(".gz") + 3]])
                                    fits_file_path = download_from_url(fits_url)
                                    fits_filename = fits_file_path.split(os.sep)[-1]
                                    fits_file = Lib.fitsread.ECallistoFitsFile(fits_filename)
                                    fits_file.set_file_path()
                                    try:
                                        proc = mp.Process(target=plot_fits_from_date(fits_file, fits_file_path,
                                                                                     next_year, next_month, next_day,
                                                                                     instrument))
                                        proc.daemon = True
                                        proc.start()
                                        proc.join()
                                        del proc
                                    except Exception as e:
                                        print(e)
                                        pass
                                    finally:
                                        try:
                                            fits_file.delete_file()
                                            del fits_url, fits_file_path, fits_filename, fits_file
                                            gc.collect()
                                        except Exception as exception:
                                            print(exception)
                                            try:
                                                del fits_url, fits_file_path, fits_filename, fits_file
                                                gc.collect()
                                            except Exception as exception:
                                                print(exception)
                    del next_date_url, next_date_str
                    gc.collect()
                    try:
                        os.remove(next_date_url_index)
                    except Exception as e:
                        print(e)
                        pass
                    del next_date_url_index
                    gc.collect()
