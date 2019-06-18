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

plt.plot(volt_vals, cur_vals, 'go-', linewidth=1, markersize=5)
plt.xlabel('Voltage, V')
plt.ylabel('Current, A')
plt.show()

#extract linear coefficient
from scipy.optimize import curve_fit

#volt_vals = [1., 2., 3., 4.,]
#cur_vals = [1., 2., 3., 4.,]

def lin_func(x, a, b):
    return a*x+b

def exp_func(x, a, b, c):
    return a * np.exp(-b * x) + c

popt, pcov = curve_fit(lin_func, volt_vals, cur_vals)
slope = popt[0]
print 'R = ' + slope + ' Ohm'
