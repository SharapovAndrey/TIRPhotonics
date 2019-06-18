General purpose: read measurement information from Keysight 2614B Source Meter

To work with this model of digital multimeter one requires the following software:
1. National Instruments Visa www.ni.com/visa/
2. Python (2 / 3) + PyVisa www.pyvisa.readthedocs.io
* Keithley2600 https://pypi.org/project/keithley2600/ did not work because of unsolved issues with PyUSB

Steps:
1) Read device information (IDN.py)
2) Build current–voltage curve of 100 Ohm resistor and estimate the resistance by linear fitting (Resistor.py)
