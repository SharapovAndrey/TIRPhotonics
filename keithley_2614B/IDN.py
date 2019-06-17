import visa
rm = visa.ResourceManager()
addr = rm.list_resources()[0]
my_instrument = rm.open_resource(addr)
print my_instrument
#USBInstrument at USB0::0x05E6::0x2614::4071436::INSTR
print(my_instrument.query('*IDN?'))
#Keithley Instruments Inc., Model 2614B, 4071436, 3.2.2

#same as the following two strings
#my_instrument.write('*IDN?')
#print(my_instrument.read())
