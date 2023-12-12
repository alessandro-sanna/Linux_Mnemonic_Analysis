from matplotlib import pyplot as plt
import pandas as pd


if __name__ == "__main__":
    dfArm = pd.read_csv("~/.mnt/ELF_Dataset/ELF_Dataset_ARM_samples.csv")
    dfCount = dfArm.groupby("year").count().reset_index()
    fig, ax = plt.subplots()

    x = list(dfCount.year)
    x = x[0:1] + [2008, 2009] + x[1:]
    y = list(dfCount.sha256_hash)
    y = y[0:1] + [0, 0] + y[1:]
    

    bars = ax.barh(x, y, log=True)
    ax.set_yticks(x, labels=map(str, x))
    ax.set_xlim([1, 10**5])
    ax.bar_label(bars, padding=2)

    plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, horizontalalignment='right')
    fig.tight_layout()
    fig.savefig("yeardist.pdf")
