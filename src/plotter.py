### GENERATE PLOTS ###
######################
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import time
from importlib import reload
from src.params import bkg_clr, frg_clr, hlt1_clr, hlt2_clr, hlt3_clr, txt_clr
from src.timeFreqAnalysis import tf_analysis
import src.fileHandler as file

def init():
    global samplerate
    global data
    samplerate = file.samplerate_
    data = file.data_
    print(samplerate)
    print(data)

# generate amplitude plot of signal 
def plot_amp():
    plot_timeline() # update timeline plot
    x = np.arange(0, len(data))
    y_l = abs(data[:,0]) # separate left and right channel data
    y_r = -abs(data[:,1])
    plt.clf()
    fig = plt.figure(frameon = False, figsize=(7.8, 1.5))
    ax = plt.Axes(fig, [0., 0., 1., 1.], )
    plt.axis('off')
    ax.get_xaxis().set_visible(False) 
    ax.get_yaxis().set_visible(False) 
    plt.plot(x, y_l, color = hlt2_clr)
    plt.plot(x, y_r, color = hlt1_clr)
    plt.savefig("media/amp_plot.png", bbox_inches='tight', pad_inches = 0, dpi=500)

    return True

# generate a timeline of audio (mostly just fancy formatting)
def plot_timeline():
    plt.clf()
    ax = plt.subplot(1, 1, 1)
    ax.spines['right'].set_color('none')
    ax.spines['left'].set_color('none')
    ax.yaxis.set_major_locator(ticker.NullLocator())
    ax.spines['top'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.tick_params(which='major', direction='inout', width=0.5, length=10)
    ax.tick_params(which='minor', direction='inout', width=0.5, length=5)
    ax.set_xlim(0, data.shape[0]/samplerate)
    ax.set_ylim(0, 1)
    ax.patch.set_alpha(0.0)
    ax.xaxis.set_major_locator(ticker.MultipleLocator(len(data)/(10*samplerate)))
    ax.xaxis.set_minor_locator(ticker.MultipleLocator(len(data)/(50*samplerate)))
    formatter = ticker.FuncFormatter(lambda s, x: time.strftime('%M:%S', time.gmtime(s)))
    ax.xaxis.set_major_formatter(formatter)
    plt.xticks(fontsize=5)
    plt.subplots_adjust(left=0.0, right=0.75, bottom=0.025, top=0.05)
    plt.savefig("media/timeline.png", bbox_inches='tight', pad_inches = 0, dpi=500, transparent=True)

# generate time-frequency plot 
def plot_tf(colors=[hlt1_clr,hlt2_clr,hlt3_clr]):
    plt_data = tf_analysis(samplerate, data)
    plt.clf()
    fig = plt.figure(frameon = False, figsize=(7.8, 1.5))
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    plt.axis('off')
    ax.get_xaxis().set_visible(False) 
    ax.get_yaxis().set_visible(False) 
    plt.plot(0.75*plt_data[1], alpha = 0.9, color = colors[1], label="Mid") # mids
    plt.plot(plt_data[0], alpha = 0.9, color = colors[0], label="Low") # lows
    plt.plot(0.5*plt_data[2], alpha = 1.0, color = colors[2], label="High") # highs
    plt.savefig("media/tf_plot.png", bbox_inches='tight', pad_inches = 0, dpi=500)
    return True
