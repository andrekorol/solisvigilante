from matplotlib import pyplot as plt
import numpy as np
from astropy.io import fits
import os
from tkinter import Tk
from tkinter import messagebox
from tkinter import filedialog
import math


class FitsFile(object):
    """Main entry point to the FITS file format"""
    def __init__(self, filename: str = None):
        self.filename = filename
        self.hdul = None
        self.file_path = None

    def set_filename(self, filename):
        self.filename = filename

    def get_filename(self):
        return self.filename

    def set_file_path(self):
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
                                         'No such file or directory: '
                                         f'{self.filename}')
                    raise FileNotFoundError

        else:
            self.file_path = filedialog.askopenfilename()
            self.set_filename(self.file_path.split('/')[-1])

    def get_gile_path(self):
        return self.file_path

    def set_hdul(self):
        try:
            self.hdul = fits.open(self.file_path)
        except FileNotFoundError as e:
            messagebox.showerror('FileNotFoundError: [Errno 2]',
                                 'No such file or directory: '
                                 f'{self.file_path}')
            raise e
        except OSError as e:
            messagebox.showerror('OSError',
                                 f'{self.file_path} is not a FITS file.')
            raise e

    def get_hdul(self):
        return self.hdul

    def close_hdul(self):
        self.hdul.close()

    def delete_file(self):
        os.remove(self.file_path)


class ECallistoFitsFile(FitsFile):
    def __init__(self, filename: str = None):
        FitsFile.__init__(self, filename)
        self.hdul_dataset = {}

    @staticmethod
    def digit_to_voltage(digits):
        return digits / 255.0 * 2500.0

    def set_hdul_dataset(self):
        if self.hdul is None:
            if self.file_path is None:
                self.set_file_path()
            self.set_hdul()
        hdul_dataset = self.hdul_dataset
        hdul = self.hdul

        hdul_dataset['data'] = hdul[0].data.astype(np.float32)
        hdul_dataset['hh'] = float(hdul[0].header['TIME-OBS'].split(':')[0])
        hdul_dataset['mm'] = float(hdul[0].header['TIME-OBS'].split(':')[1])
        hdul_dataset['ss'] = float(hdul[0].header['TIME-OBS'].split(':')[2])
        hdul_dataset['time'] = hdul[1].data[0][0].astype(np.float32)
        hdul_dataset['f0'] = hdul[1].data[0][1].astype(np.float32)
        # cut lower 10 channels:
        hdul_dataset['frequency'] = hdul_dataset['f0'][:-10]
        hdul_dataset['start_time'] = hdul_dataset['hh'] * 3600 + \
            hdul_dataset['mm'] * 60 + hdul_dataset['ss']
        hdul_dataset['rows'] = hdul_dataset['data'].shape[0]
        hdul_dataset['columns'] = hdul_dataset['data'].shape[1]
        hdul_dataset['dt'] = hdul_dataset['time'][1] - hdul_dataset['time'][0]
        hdul_dataset['time_axis'] = (hdul_dataset['start_time']
                                     + hdul_dataset['dt'] *
                                     np.arange(hdul_dataset['columns'])) / 3600
        hdul_dataset['freq_axis'] = np.linspace(hdul_dataset['frequency'][0],
                                                hdul_dataset['frequency'][-1],
                                                3600)
        self.close_hdul()

    def get_hdul_dataset(self):
        return self.hdul_dataset

    def plot_db_above_background(self, show=False, save=True):
        plt.figure(figsize=(11, 6))
        v_min = -1  # -0.5, 100
        v_max = 8  # 4, 160
        dref = self.hdul_dataset['data'] - np.min(self.hdul_dataset['data'])
        # conversion digit->voltage->into db
        db = self.digit_to_voltage(dref) / 25.4
        db_median = np.median(db, axis=1, keepdims=True)
        plt.imshow(db - db_median, cmap='magma',
                   norm=plt.Normalize(v_min, v_max),
                   aspect='auto', extent=[self.hdul_dataset['time_axis'][0],
                                          self.hdul_dataset['time_axis']
                                          [-1000],
                                          self.hdul_dataset['frequency'][-1],
                                          self.hdul_dataset['frequency'][0]])
        plt.gca().invert_yaxis()
        plt.colorbar(label='dB above background')
        plt.xlabel('Time (UT)', fontsize=15)
        plt.ylabel('Frequency (MHz', fontsize=15)
        plt.title(self.filename, fontsize=16)
        plt.tick_params(labelsize=14)
        if save:
            img_filename = '.'.join(self.file_path.split('.')[:-2]) + '.png'
            plt.savefig(img_filename, bbox_inches='tight')
        if show:
            plt.show()

    def set_fits_linear_regression(self):
        hdul_dataset = self.hdul_dataset
        hdul_dataset['lin_reg'] = np.polyfit(hdul_dataset['time_axis'], hdul_dataset['freq_axis'], 1)

    def get_fits_linear_regression(self):
        return self.hdul_dataset['lin_reg']

    def get_fits_linear_regression_function(self):
        return np.poly1d(self.hdul_dataset['lin_reg'])

    def plot_fits_linear_regression(self, show=False, save=True):
        intercept = self.hdul_dataset['lin_reg'].intercept
        slope = self.hdul_dataset['lin_reg'].slope
        plt.gca().invert_yaxis()
        plt.plot(self.hdul_dataset['time'][2000:],
                 intercept + slope * self.hdul_dataset['time_axis'][2000:],
                 'r')
        plt.xlabel('Time (UT)', fontsize=15)
        plt.ylabel('Frequency (MHz)', fontsize=15)
        plt.title(self.filename + ' Simple Linear Regression\nf(t) = ' +
                  f'{intercept:.2f} + ({slope:.2f}t)', fontsize=16)
        plt.tick_params(labelsize=14)
        if save:
            img_filename = '.'.join(self.file_path.split('.')[:-2]) +\
                           'linear_regression.png'
            plt.savefig(img_filename, bbox_inches='tight')
        if show:
            plt.show()
        # TODO: Improve the plot_fits_linear_regression method


class ChromosphericEvaporationFitsFile(ECallistoFitsFile):
    def __init__(self, filename: str = None):
        ECallistoFitsFile.__init__(self, filename)
        self.front_velocity = None

    def set_front_velocity(self, inf_front_time,
                           sup_front_time,
                           velocity=None):
        if velocity is not None:
            self.front_velocity = velocity
        else:
            lin_reg_fn = self.get_fits_linear_regression_function()
            inf_front_freq = lin_reg_fn(inf_front_time)
            sup_front_freq = lin_reg_fn(sup_front_time)

            inf_density = (inf_front_freq / 8.98e-03) ** 2
            sup_density = (sup_front_freq / 8.98e-03) ** 2

            Nq = 4.6e+8
            H = 7e+4
            inf_height = math.log(Nq / inf_density) * H
            sup_height = math.log(Nq / sup_density) * H

            time_diff = (sup_front_time - inf_front_time) * 3600
            height_diff = sup_height - inf_height

            self.front_velocity = round(height_diff / time_diff, 1)

    def get_front_velocity(self):
        return self.front_velocity
