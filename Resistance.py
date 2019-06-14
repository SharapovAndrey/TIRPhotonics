import visa
rm = visa.ResourceManager()
addr = rm.list_resources()[0]
keysight = rm.open_resource(addr)

#reset
keysight.write("*rst; status:preset; *cls")
#print msg on the device screen
#keysight.write('DISP:TEXT " Skoltech "')
keysight.write('MEAS:RES?')
res_val = keysight.read()
print res_val
