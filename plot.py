import matplotlib.pyplot as plt
import pandas as pd
from os import listdir
from os.path import isfile, join

"""this is a script to plot the heart
voltage data from the 16 test csv files"""

mypath = "/Users/dp/Downloads/BME 547/ecg-analysis-echodpp/test_data/"
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
onlyfiles.remove("README.md")
colnames = ["time", "voltage"]
for i in onlyfiles:
    df = pd.read_csv(mypath + i, names=colnames, header=None)
    df = df.iloc[1:800]
    plt.figure(figsize=(18, 6))
    plt.xlabel("Time (s)")
    plt.ylabel("Voltage (mV)")
    plt.title(i)
    plt.plot(df["time"], df["voltage"], "b")
    plt.savefig(
        "/Users/dp/Downloads/BME 547/ecg-analysis-echodpp/plot_data/"
        + i + ".png"
    )
