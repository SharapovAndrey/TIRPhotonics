import visa
import time
import matplotlib.pyplot as plt
rm = visa.ResourceManager()
addr = rm.list_resources()[0]
keysight = rm.open_resource(addr)

#reset
keysight.write("*rst; status:preset; *cls")
#print msg on the device screen
#keysight.write('DISP:TEXT " Skoltech "')

#plt.ion()
fig = plt.figure()
ax = fig.add_subplot(111)

res_val_arr = []

for i in range(5):
    #request resistance measurement (warning: it is possible to set integration time)
    keysight.write('MEAS:RES?')

    res_val = keysight.read()
    res_val_arr.append(res_val)
    print i, res_val
    ax = fig.add_subplot(111)
    ax.scatter(i, res_val, c='b')
    time.sleep(0.5)
fig.show()

