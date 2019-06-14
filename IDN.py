import visa
rm = visa.ResourceManager()
#print(rm.list_resources())
addr = rm.list_resources()[0]
#(u'USB0::0x0957::0x0A07::MY53001937::INSTR', u'ASRL3::INSTR')
my_instrument = rm.open_resource(addr)
print my_instrument

print(my_instrument.query('*IDN?'))
#Agilent Technologies,34411A,MY53001937,2.40-2.40-0.09-46-09

#same as the following two strings
#my_instrument.write('*IDN?')
#print(my_instrument.read())