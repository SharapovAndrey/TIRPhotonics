import visa
rm = visa.ResourceManager()
addr = rm.list_resources()[0]
#(u'USB0::0x0957::0x0A07::MY53001937::INSTR', u'ASRL3::INSTR')
keysight = rm.open_resource(addr)

#reset
keysight.write("*rst; status:preset; *cls")
#print msg on the device screen
keysight.write('DISP:TEXT " Skoltech "')
