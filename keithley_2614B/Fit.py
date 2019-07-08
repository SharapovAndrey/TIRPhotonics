import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.optimize import curve_fit

def exp_func(x, a, b):
    #e = 1.602176634e-19
    #k = 8.617333262145e-5
    #T = 3.00e2
    return a * np.exp(b * np.double(x))
    #return a * np.exp(- e * np.double(x) / b / k / T)

specimen_name = '48_2_7-6'
input_filename = 'Sh_48_2_7-6_08079.csv'
#specimen_name = '48_3_1_1'
#input_filename = 'Sh_48_3_1_1_01079.csv'

positive_diapason_tuples = [(0.5, 0.8), (0.8, 1.25), (1.25, 2.0)]#, (0.55, 0.65)]
negative_diapason_tuples = [(0.3, 0.48), (0.5, 1.0)]

df = pd.read_csv(input_filename)
#{'Voltage, V': volt_vals, 'Current, A': cur_vals})
#df.to_csv('Sh_48_3_2_1_01079_full_high.csv')
cur_vals = df['Current, A'].to_list()
volt_vals = df['Voltage, V'].to_list()

print cur_vals
print volt_vals

#divide positive part of UV-characteristic from negative one
pos_cur_vals, pos_volt_vals = zip(*[(j, v) for (j, v) in zip(cur_vals, volt_vals)
                                                if v >= 0.])
#now let's invert and fit the negative part of IV-characteristic
neg_cur_vals, neg_volt_vals = zip(*[(-j, -v) for (j, v) in zip(cur_vals, volt_vals)
                                                if v <= 0.])
neg_cur_vals = list(neg_cur_vals)
neg_volt_vals = list(neg_volt_vals)
pos_cur_vals = list(pos_cur_vals)
pos_volt_vals = list(pos_volt_vals)

#plt.plot(volt_vals, cur_vals, 'go', linewidth=1, markersize=1.5, label='exp')
fig = plt.figure(figsize=(15, 20))
plt.plot(pos_volt_vals, pos_cur_vals, 'go', linewidth=1, markersize=1.5, label='positive branch')
plt.plot(neg_volt_vals, neg_cur_vals, 'bo', linewidth=1, markersize=1.5, label='negative inverted')

opt_parameters = []

#plt.plot(volt_vals, cur_vals, 'go', linewidth=1, markersize=1.5, label='exp')

for i in range(len(positive_diapason_tuples)):
    print 'Diapason ' + str(i) + ' for fit'
    #select diapason
    selected_cur_vals, selected_volt_vals = zip(*[(j, v) for (j, v) in zip(cur_vals, volt_vals)
                                                if positive_diapason_tuples[i][0] <= v <= positive_diapason_tuples[i][1]])
    #zip(cur_vals, volt_vals)[0]
    selected_cur_vals = list(selected_cur_vals)
    selected_volt_vals = list(selected_volt_vals)

    popt, pcov = curve_fit(exp_func, selected_volt_vals, selected_cur_vals)

    e = 1. # 1.602176634e-19 # C
    k = 8.617333262145e-5 # eV/K
    T = 273.15+25. # K
    print popt
    eta = np.double(e) / k / T / popt[1]
    print 'Nonideality factor = ' + str(eta)
    opt_parameters.append([popt[0]*1e3, eta])#(popt)
    print pcov
    perr = np.sqrt(np.diag(pcov))
    print perr

    x_fit = np.arange(min(selected_volt_vals), max(selected_volt_vals), 0.01) #np.arange(min(volt_vals), max(volt_vals), 0.01)
    y_fit = exp_func(x_fit, popt[0], popt[1])

    plt.plot(x_fit, y_fit, 'r-', linewidth=1, label='fit pos '+str(i))
    plt.plot(x_fit, y_fit, 'r-', linewidth=10, alpha=0.3)

#plt.xlabel('Voltage, V')
#plt.ylabel('Current, A')
plt.yscale('log')
#plt.grid()
#plt.legend()
#plt.show()

print '\nNegative part fitting\n'

for i in range(len(negative_diapason_tuples)):
    print 'Diapason ' + str(i) + ' for fit'
    #select diapason
    selected_cur_vals, selected_volt_vals = zip(*[(j, v) for (j, v) in zip(neg_cur_vals, neg_volt_vals)
                                                if negative_diapason_tuples[i][0] <= v <= negative_diapason_tuples[i][1]])
    #zip(cur_vals, volt_vals)[0]
    selected_cur_vals = list(selected_cur_vals)
    selected_volt_vals = list(selected_volt_vals)

    popt, pcov = curve_fit(exp_func, selected_volt_vals, selected_cur_vals)

    e = 1. # 1.602176634e-19 # C
    k = 8.617333262145e-5 # eV/K
    T = 273.15+25. # K
    print popt
    eta = np.double(e) / k / T / popt[1]
    print 'Nonideality factor = ' + str(eta)
    opt_parameters.append([popt[0]*1e3, eta])
    print pcov
    perr = np.sqrt(np.diag(pcov))
    print perr

    x_fit = np.arange(min(selected_volt_vals), max(selected_volt_vals), 0.01) #np.arange(min(volt_vals), max(volt_vals), 0.01)
    y_fit = exp_func(x_fit, popt[0], popt[1])

    plt.plot(x_fit, y_fit, 'r-', linewidth=1, label='fit neg '+str(i))
    plt.plot(x_fit, y_fit, 'r-', linewidth=10, alpha=0.3)

plt.xlabel('Voltage, V')
plt.ylabel('Current, A')
plt.title('Specimen ' + specimen_name)
plt.grid()
plt.legend(loc='lower right')
plt.show()
fig.savefig('Specimen ' + specimen_name + '.png')

#df_opt_param = pd.DataFrame
negative_diapason_tuples = [(-j, -v) for (j, v) in negative_diapason_tuples]
#print positive_diapason_tuples + negative_diapason_tuples
#print np.array(opt_parameters)[:,0]
t = {'Diapason, V': positive_diapason_tuples + negative_diapason_tuples,
     'I_0, mA': np.array(opt_parameters)[:,0],
     'Nonideality factor': np.array(opt_parameters)[:,1]}

df_opt_param = pd.DataFrame(t)
print df_opt_param

filename = r'opt_params.csv'
erase_before_writing = False
with open(filename, 'a') as f:
    if erase_before_writing:
        f.truncate()
    f.write('\nSpecimen ' + specimen_name + '\n\n')
    df_opt_param.to_csv(f, header=True, index=False)

