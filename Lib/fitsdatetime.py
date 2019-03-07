import os
import shutil
from datetime import date, datetime, time, timedelta
from Lib.fitsread import ECallistoFitsFile
from Lib.urlget import download_from_url


class DateTimeFitsFile(ECallistoFitsFile):
    def __init__(self, datetime_obj: datetime):
        ECallistoFitsFile.__init__(self)
        self.datetime_obj = datetime_obj
        self.year = str(datetime_obj.year)
        self.month = str(datetime_obj.month)
        self.day = str(datetime_obj.day)
        self.hour = str(datetime_obj.hour)
        self.minute = str(datetime_obj.minute)

    @staticmethod
    def pad_string(string: str, width: int):
        return string.zfill(width)

    def format_datetime(self):
        self.month = self.pad_string(self.month, 2)
        self.day = self.pad_string(self.day, 2)
        self.hour = self.pad_string(self.hour, 2)
        self.minute = self.pad_string(self.minute, 2)

    def plot_fits_from_date(self, instrument: str, move_plot: bool = False):
        self.format_datetime()
        data_archives = "http://soleil80.cs.technik.fhnw.ch/solarradio/data/2002-20yy_Callisto"
        if self.hour == "00" and self.minute == "00":
            date_url = '/'.join([data_archives, self.year, self.month, self.day])
            date_url_index = download_from_url(date_url)
            date_str = self.year + self.month + self.day
            with open(date_url_index) as index:
                for item in index:
                    if item.find(instrument + '_' + date_str) != -1:
                        fits_url = '/'.join([date_url, item[item.find(instrument + '_' + date_str):item.find(".gz")+3]])
                        print("Fits url = ", fits_url)
                        fits_file_path = download_from_url(fits_url)
                        print("Fits file path = ", fits_file_path)
                        self.set_file_path(fits_file_path)
                        self.set_hdul_dataset()
                        self.plot_db_above_background()
                        self.delete_file()
                        if move_plot:
                            plot_filename = fits_file_path.split(os.sep)[-1].replace(".fit.gz", ".png")
                            src_plot_path = fits_file_path.replace(".fit.gz", ".png")
                            dst_path = os.sep.join([os.getcwd(), self.year, self.month, self.day, instrument])
                            dst_plot_path = os.path.join(dst_path, plot_filename)
                            if not os.path.exists(dst_path):
                                os.makedirs(dst_path)
                            shutil.move(src_plot_path, dst_plot_path)

            os.remove(date_url_index)
