import matplotlib.pyplot as plt
import numpy as np
import matplotlib.mlab as mlab
import pandas as pd
import endaq.calc.psd



df_ref_1250PWM = pd.read_csv('refrun 3.csv',index_col=0)
df_test = pd.read_csv('1250PWM 3420RPM 47C small tape.csv',index_col=0)

df_ref_1250PWM = df_ref_1250PWM.drop(df_ref_1250PWM.columns[[3,4,5]],axis = 1)
df_test = df_test.drop(df_test.columns[[3,4,5]],axis = 1)

psd_ref_1250PWM = endaq.calc.psd.welch(df_ref_1250PWM,1)
psd_test = endaq.calc.psd.welch(df_test,1)

if (psd_ref_1250PWM.shape[0] > psd_test.shape[0]):
    psd_ref_1250PWM = psd_ref_1250PWM.iloc[:psd_test.shape[0]]
elif (psd_ref_1250PWM.shape[0] < psd_test.shape[0]):
    psd_test = psd_test.iloc[:psd_ref_1250PWM.shape[0]]


psd_I1 = pd.DataFrame(index=psd_ref_1250PWM.index)
psd_I1["I1_ref"] = psd_ref_1250PWM['I1'].to_list()
psd_I1["I1_test"] = psd_test['I1'].to_list()

psd_I2 = pd.DataFrame(index=psd_ref_1250PWM.index)
psd_I2["I2_ref"] = psd_ref_1250PWM['I2'].to_list()
psd_I2["I2_test"] = psd_test['I2'].to_list()

psd_I3 = pd.DataFrame(index=psd_ref_1250PWM.index)
psd_I3["I3_ref"] = psd_ref_1250PWM['I3'].to_list()
psd_I3["I3_test"] = psd_test['I3'].to_list()

psd_ref_1250PWM['I1n'] = psd_test['I1'].to_list()
psd_ref_1250PWM['I2n'] = psd_test['I2'].to_list()
psd_ref_1250PWM['I3n'] = psd_test['I3'].to_list()

figure, axis = plt.subplots(3, 1)
# For Sine Function
axis[0].plot(psd_I1)
axis[0].set_title("I1")
axis[0].set_xscale("log")

  
# For Cosine Function
axis[1].plot(psd_I2)
axis[1].set_title("I2")
axis[1].set_xscale("log")

  
# For Tangent Function
axis[2].plot(psd_I3)
axis[2].set_title("I3")
axis[2].set_xscale("log")



#plt.plot(psd_I1)
#plt.title('Sample name data')
#plt.ylabel('Power')
##plt.yscale("log")
#plt.xlabel('Frequency (Hz)')
#plt.xscale("log")

plt.legend(["I_ref", "I_test"])
plt.grid(color='grey')
plt.show()
