import matplotlib.pyplot as plt
import numpy as np
import matplotlib.mlab as mlab
import pandas as pd
import endaq.calc.psd

def compare(refFile, testFile, title = "Default",minHz = 700, maxHz = 110000):
    bin = 1
    df_ref = pd.read_csv(refFile,index_col=0)
    df_test = pd.read_csv(testFile,index_col=0)

    df_ref = df_ref.drop(df_ref.columns[[3,4,5]],axis = 1)
    df_test = df_test.drop(df_test.columns[[3,4,5]],axis = 1)

    psd_ref = endaq.calc.psd.welch(df_ref,bin)
    psd_test = endaq.calc.psd.welch(df_test,bin)

    #Discard the last elements of the longest DF to get equal length
    if (psd_ref.shape[0] > psd_test.shape[0]):
        psd_ref = psd_ref.iloc[:psd_test.shape[0]]
    elif (psd_ref.shape[0] < psd_test.shape[0]):
        psd_test = psd_test.iloc[:psd_ref.shape[0]]

    #Narrowing span of frequency to be plotted
    psd_ref = psd_ref.iloc[:int(maxHz/bin)]
    psd_test = psd_test.iloc[:int(maxHz/bin)]
    psd_ref = psd_ref.iloc[int(minHz/bin):]
    psd_test = psd_test.iloc[int(minHz/bin):]

    #Combine the DF, handling rounding errors
    psd_I1 = pd.DataFrame(index=psd_ref.index)
    psd_I1["I1_ref"] = psd_ref['I1'].to_list()
    psd_I1["I1_test"] = psd_test['I1'].to_list()

    psd_I2 = pd.DataFrame(index=psd_ref.index)
    psd_I2["I2_ref"] = psd_ref['I2'].to_list()
    psd_I2["I2_test"] = psd_test['I2'].to_list()

    psd_I3 = pd.DataFrame(index=psd_ref.index)
    psd_I3["I3_ref"] = psd_ref['I3'].to_list()
    psd_I3["I3_test"] = psd_test['I3'].to_list()

    psd_ref['I1n'] = psd_test['I1'].to_list()
    psd_ref['I2n'] = psd_test['I2'].to_list()
    psd_ref['I3n'] = psd_test['I3'].to_list()

    figure, axis = plt.subplots(3, 1)
    figure.suptitle(title)
    # For Sine Function
    axis[0].plot(psd_I1["I1_ref"], color= "k")
    axis[0].plot(psd_I1["I1_test"], color= "r", ls="dotted")
    axis[0].set_title("I1")
    axis[0].set_xscale("log")
    axis[0].legend(["I_ref", "I_test"])
    axis[0].grid(color='grey')

    
    # For Cosine Function
    axis[1].plot(psd_I2["I2_ref"], color= "k")
    axis[1].plot(psd_I2["I2_test"], color= "r", ls="dotted")
    axis[1].set_title("I2")
    axis[1].set_xscale("log")
    axis[1].legend(["I_ref", "I_test"])
    axis[1].grid(color='grey')

    
    # For Tangent Function
    axis[2].plot(psd_I3["I3_ref"], color= "k")
    axis[2].plot(psd_I3["I3_test"], color= "r", ls="dotted")
    axis[2].set_title("I3")
    axis[2].set_xscale("log")
    axis[2].legend(["I_ref", "I_test"])
    axis[2].grid(color='grey')
    plt.show()