from matplotlib import pyplot as plt
import numpy as np
from astropy.io import fits
import os
from tkinter import Tk
from tkinter import messagebox
from tkinter import filedialog


class FitsFile(object):
    """Main entry point to the FITS file format"""
    def __init__(self, filename: object = None) -> object:
        self.filename = filename
        self.hdul = None
        self.fisle_path = None

    def get_file_path(self):
        root = Tk()
        root.withdraw()
        if self.filename is not None:
            try:
                top = os.getcwd()
                for root, dirs, files in os.walk(top):
                    for file in files:
                        if file == self.filename:
                            self.file_path = os.path.abspath(file)
            finally:
                if self.file_path is None:
                    messagebox.showerror('FileNotFoundError: [Errno 2]',
                                         f'No such file or directory: {self.filename}')
                    raise FileNotFoundError

        else:
            self.file_path = filedialog.askopenfilename()

        return self.file_path

    def get_hdul(self):
        try:
            self.hdul = fits.open(self.file_path)
        except FileNotFoundError as e:
            messagebox.showerror('FileNotFoundError: [Errno 2]',
                                 f'No such file or directory: {self.file_path}')
            raise e
        except OSError as e:
            messagebox.showerror('OSError', f'{self.file_path} is not a FITS file.')
            raise e

        return self.hdul

    def close(self):
        self.hdul.close()

    def delete_file(self):
        os.remove(self.file_path)

    @staticmethod
    def digit_to_voltage(digits):
        return digits / 255.0 * 2500.0

    def plot_db_above_background(self, save=True):
        data = self.hdul[0].data.astype(np.float32)
        hh = float(self.hdul[0].header['TIME-OBS'].split(':')[0])
        mm = float(self.hdul[0].header['TIME-OBS'].split(':')[1])
        ss = float(self.hdul[0].header['TIME-OBS'].split(':')[2])
        time = self.hdul[1].data[0][0].astype(np.float32)
        f0 = self.hdul[1].data[0][1].astype(np.float32)
        frequency = f0[:-10]  # cut lower 10 channels

        start_time = hh * 3600 + mm * 60 + ss  # all in seconds

        rows = data.shape[0]
        columns = data.shape[1]
        print('Rows =', rows)
        print('Columns =', columns)

        dt = time[1] - time[0]
        time_axis = (start_time + dt * np.arange(data.shape[1])) / 3600

        plt.figure(figsize=(11, 6))
        v_min = -1  # -0.5, 100
        v_max = 8  # 4, 160
        dref = data - np.min(data)
        db = self.digit_to_voltage(dref) / 25.4  # conversion digit->voltage->into db
        db_median = np.median(db, axis=1, keepdims=True)

        plt.imshow(db - db_median, cmap='magma', norm=plt.Normalize(v_min, v_max),
                   aspect='auto', extent=[time_axis[0], time_axis[-1000],
                                          frequency[-1], frequency[0]])
        plt.gca().invert_yaxis()
        plt.colorbar(label='dB above background')
        plt.xlabel('Time (UT)', fontsize=15)
        plt.ylabel('Frequency (MHz)', fontsize=15)
        filename = os.path.basename(self.file_path)
        plt.title(filename, fontsize=16)
        plt.tick_params(labelsize=14)

        if save:
            img_filename = '.'.join(self.file_path.split('.')[:-2]) + '.png'
            plt.savefig(img_filename, bbox_inches='tight')

        plt.show()


class ECallistoFitsFile(FitsFile):
    def __init__(self, filename: str = None):
        FitsFile.__init__(self, filename)
