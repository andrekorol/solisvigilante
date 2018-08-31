from matplotlib import pyplot as plt
import numpy as np
from astropy.io import fits
import os
from tkinter import Tk
from tkinter import messagebox
from tkinter import filedialog
from scipy import stats


def Digit2Voltage(d):
    return d / 255.0 * 2500.0


def GetFitsPath():
    Tk().withdraw()
    file_path = filedialog.askopenfilename()
    return file_path


def PlotFitsdB(file_path, save=True):
    root = Tk()
    root.withdraw()

    try:
        hdul = fits.open(file_path)
    except FileNotFoundError as e:
        messagebox.showerror('FileNotFoundError: [Errno 2]',
                             f'No such file or directory: {file_path}')
        raise e
    except OSError as e:
        messagebox.showerror('OSError', f'{file_path} is not a FITS file.')
        raise e

    data = hdul[0].data.astype(np.float32)
    hh = float(hdul[0].header['TIME-OBS'].split(':')[0])
    mm = float(hdul[0].header['TIME-OBS'].split(':')[1])
    ss = float(hdul[0].header['TIME-OBS'].split(':')[2])
    time = hdul[1].data[0][0].astype(np.float32)
    f0 = hdul[1].data[0][1].astype(np.float32)
    rows = f0.shape[0]
    frequency = f0[:-10]  # cut lower 10 channels
    hdul.close()

    start_time = hh * 3600 + mm * 60 + ss  # all in seconds

    rows = data.shape[0]
    columns = data.shape[1]
    print('Rows =', rows)
    print('Columns =', columns)

    dT = time[1] - time[0]
    time_axis = (start_time + dT * np.arange(data.shape[1])) / 3600

    plt.figure(figsize=(11, 6))
    vmin = -1  # -0.5, 100
    vmax = 8  # 4, 160
    dref = data - np.min(data)
    dB = Digit2Voltage(dref) / 25.4  # conversion digit->voltage->into dB
    dB_median = np.median(dB, axis=1, keepdims=True)

    plt.imshow(dB - dB_median, cmap='magma', norm=plt.Normalize(vmin, vmax),
               aspect='auto', extent=[time_axis[0], time_axis[-1000],
                                      frequency[-1], frequency[0]])
    plt.gca().invert_yaxis()
    plt.colorbar(label='dB above background')
    plt.xlabel('Time (UT)', fontsize=15)
    plt.ylabel('Frequency (MHz)', fontsize=15)
    filename = os.path.basename(file_path)
    plt.title(filename, fontsize=16)
    plt.tick_params(labelsize=14)
    print(time_axis[0], time_axis[-1])

    if save:
        img_filename = '.'.join(file_path.split('.')[:-2]) + '.png'
        plt.savefig(img_filename, bbox_inches='tight')

    # plt.ion()
    plt.show()


def FitsLinearRegression(file_path, save=True):
    root = Tk()
    root.withdraw()

    try:
        hdul = fits.open(file_path)
    except FileNotFoundError as e:
        messagebox.showerror('FileNotFoundError: [Errno 2]',
                             f'No such file or directory: {file_path}')
        raise e
    except OSError as e:
        messagebox.showerror('OSError', f'{file_path} is not a FITS file.')
        raise e

    data = hdul[0].data.astype(np.float32)
    hh = float(hdul[0].header['TIME-OBS'].split(':')[0])
    mm = float(hdul[0].header['TIME-OBS'].split(':')[1])
    ss = float(hdul[0].header['TIME-OBS'].split(':')[2])
    time = hdul[1].data[0][0].astype(np.float32)
    f0 = hdul[1].data[0][1].astype(np.float32)
    frequency = f0[:-10]  # cut lower 10 channels
    hdul.close()

    start_time = hh * 3600 + mm * 60 + ss  # all in seconds
    dT = time[1] - time[0]
    time_axis = (start_time + dT * np.arange(data.shape[1])) / 3600
    # time_axis = time_axis.reshape(len(time_axis), 1)

    freq_axis = np.linspace(frequency[0], frequency[-1], 3600)
    # freq_axis = freq_axis.reshape(len(freq_axis), 1)

    linear_regression = stats.linregress(time_axis, freq_axis)
    print(linear_regression)

    intercept = linear_regression.intercept
    slope = linear_regression.slope
    plt.gca().invert_yaxis()
    plt.plot(time_axis[2000:], intercept + slope * time_axis[2000:], 'r')
    plt.xlabel('Time (UT)', fontsize=15)
    plt.ylabel('Frequency (MHz)', fontsize=15)
    filename = os.path.basename(file_path)
    plt.title(filename + ' Simple Linear Regression\nf(t) = ' + f'{intercept:.2f} + ({slope:.2f}t)', fontsize=16)
    plt.tick_params(labelsize=14)

    if save:
        img_filename = '.'.join(file_path.split('.')[:-2]) + 'linear_regression.png'
        plt.savefig(img_filename, bbox_inches='tight')

    plt.show()
