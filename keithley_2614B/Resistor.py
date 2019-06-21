import visa
import numpy as np
import matplotlib.pyplot as plt

rm = visa.ResourceManager()
addr = rm.list_resources()[0]
instrument = rm.open_resource(addr)

volt_vals = []
cur_vals = []

level_list = np.arange(-1., 1., 0.1, dtype=np.double)
level_list = np.append(level_list , np.arange(0.95, -1., -0.1, dtype=np.double))
for level in level_list:
    instrument.write("smua.reset()")
    instrument.write("smua.sense = smua.SENSE_LOCAL") #Select local sense (2-wire).
    instrument.write("smua.source.autorangev = smua.AUTORANGE_ON")
    instrument.write("smua.source.rangei = 1e-2")
    instrument.write("smua.source.limiti = 2e-2")
    instrument.write("smua.source.levelv = "+str(level))

    instrument.write("smua.source.output=smua.OUTPUT_ON")
    instrument.write("reading=smua.measure.v()")
    volt_val = np.double(instrument.query("print(reading)"))
    instrument.write("reading=smua.measure.i()")
    cur_val = np.double(instrument.query("print(reading)"))
    print volt_val, 'V; ', cur_val, 'A'
    volt_vals.append(volt_val)
    cur_vals.append(cur_val)

#extract linear coefficient
from scipy.optimize import curve_fit

#volt_vals = [1., 2., 3., 4.,]
#cur_vals = [1., 2., 3., 4.,]

#def lin_func(x, a, b):
#    return a*x+b
#def exp_func(x, a, b, c):
#    return a * np.exp(-b * x) + c

lin_func = lambda x, a, b: a*x+b
exp_func = lambda x, a, b, c: a * np.exp(-b * x) + c

popt, pcov = curve_fit(lin_func, volt_vals, cur_vals)
#print popt
#print pcov

#linear
R = 1./popt[0]
print 'R = ' + str(R) + ' Ohm'
U_0 = -popt[1]/popt[0]
print 'U0 = ' + str(U_0) + ' V'

x_fit = np.arange(min(volt_vals), max(volt_vals), 0.01)
y_fit = lin_func(x_fit, popt[0], popt[1])


plt.plot(volt_vals, cur_vals, 'go-', linewidth=1, markersize=5, label='exp')
plt.plot(x_fit, y_fit, 'b-', linewidth=0.5, label='fit')
plt.xlabel('Voltage, V')
plt.ylabel('Current, A')
plt.grid()
plt.legend()
plt.show()