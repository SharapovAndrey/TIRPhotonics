import visa
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.lines import Line2D

rm = visa.ResourceManager()
addr = rm.list_resources()[0]
keysight = rm.open_resource(addr)

#reset
keysight.write("*rst; status:preset; *cls")

res_val_arr = []

time_interval = 0.02

class Scope(object):
    def __init__(self, ax, maxt=2, dt=time_interval):
        self.ax = ax
        self.dt = dt
        self.maxt = maxt
        self.tdata = [0]
        self.ydata = [0]
        self.line = Line2D(self.tdata, self.ydata)
        self.ax.add_line(self.line)
        self.ax.set_ylim(0,1e2, auto=True)#(-.1, 1.1)
        self.ax.set_xlim(0, self.maxt)

    def update(self, y):
        lastt = self.tdata[-1]
        if lastt > self.tdata[0] + self.maxt:  # reset the arrays
            self.tdata = [self.tdata[-1]]
            self.ydata = [self.ydata[-1]]
            self.ax.set_xlim(self.tdata[0], self.tdata[0] + self.maxt)
            self.ax.figure.canvas.draw()

        t = self.tdata[-1] + self.dt
        self.tdata.append(t)
        self.ydata.append(y)
        self.line.set_data(self.tdata, self.ydata)
        #print res_val_arr
        self.ax.set_ylim(0., max(res_val_arr)+1e-2, auto=True)
        return self.line,

def receiver():
    keysight.write('MEAS:RES?')
    res_val = np.double(keysight.read())
    res_val_arr.append(res_val)
    #print res_val
    time.sleep(time_interval)
    yield res_val

#fig, ax = plt.subplots()
fig = plt.figure(num='Resistance Meter from Keysight multimeter')
plt.xlabel('Time, s')
plt.ylabel('Resistance, Ohm')
ax = fig.add_subplot(111)
scope = Scope(ax)

# pass a generator in "receiver" to produce data for the update func
ani = animation.FuncAnimation(fig, scope.update, receiver, interval=0, blit=False)

plt.show()
