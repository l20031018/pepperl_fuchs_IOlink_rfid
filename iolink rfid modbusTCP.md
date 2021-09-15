---
title: IO-link module ICE2/3* work with IQT1*IO* 13.56Mhz rfid reader
tags: rfid, io-link, Modbus/TCP
---

1. Dependent library
    pyModbusTCP
    https://github.com/sourceperl/pyModbusTCP.git

    install
	``` shell
	pip install pyModbusTCP
	```

---------

 2. Hardware
 
    3. ICE2/3-8IOL-G65L/K45S-V1D

       The module is a PROFINET IO fieldbus module with 8 type A IO-Link master ports according to IO-Link standard V1.1.

       The fieldbus module serves as an interface between the controller of a PROFINET IO fieldbus system and IO-Link devices in the field level. The integrated web server and IODD interpreter enabling complete configuration of the fieldbus module and attached IO-Link devices without the need for special software tools. Information regarding the status of the module is also displayed and network parameters such as the IP address and subnet mask can be configured. The module is capable of storing all configuration enabling stand-alone usage without a higher-level PLC. MutliLink simultaneously provides data access via different communication protocols like PROFINET IO, Modbus/TCP and OPC UA to multiple controllers. An L-coded M12 connector plug used for supplying power enables a current rating of up to 2 x 16 A.
       The inputs and outputs are equipped with A-coded M12 connector plugs. Connection to the fieldbus is achieved using a D-coded M12 connector plug.
    Status information for each channel is displayed via LEDs as a diagnostic function.



   3. Read/write station IQT1-FP/F61/18GM-IO-V1

      - Operating frequency 13.56 MHz
      - IO-link interface
      - Conforms to ISO 15693 
      - Suitable for FRAM transponder
      - LEDs as function indicators
      - Connection via V1 (M12 x 1) plug connection Degree of protection IP67 For connection to IO-Link master
           

IQT1-FP-IO-V1


IQT1-F61-IO-V1


IQT1-18GM-IO-V1


ICE2/3-8IOL-G65L-V1D


ICE2/3-8IOL-K45S-RJ45

  3. Hardware manual could find here

         https://www.pepperl-fuchs.com/global/en/classid_4996.htm?view=productdetails&prodid=96759#documents
  
  4. Example

```python
from pyModbusTCP.client import ModbusClient
from pyModbusTCP import utils
import time
import read_reg
# instantiate ip address and port
rfid = read_reg.ICE_modubus_rfid('192.168.1.250', 502)

# read tag once on port 3
rfid.read_tag(3)
time.sleep(0.1)
list_32_bits = utils.word_list_to_long(rfid.read_reg(3, "PDI", 16))
print([hex(i) for i in list_32_bits])
time.sleep(0.1)

# write data 0x0102030401020102 to tag
rfid.write_tag_data(3,[0x0102,0x0304,0x0102,0x0102,0,0,0,0,0,0,0,0,0,0])
time.sleep(0.2)

# check the writed data 
rfid.read_tag(3)
time.sleep(0.2)
list_32_bits = utils.word_list_to_long(rfid.read_reg(3, "PDI", 16))
print([hex(i) for i in list_32_bits])

# check DI on port 2 pin 2
list_32_bits = utils.word_list_to_long(rfid.read_reg(2, "PDI", 16))
print(rfid.read_reg(2, "PDI", 16))
print([hex(i) for i in list_32_bits])

# flash the led on port 8(DO on port 8 pin 2)
for i in range(10):
    rfid.set_pin2(8, 1)
    time.sleep(0.200)
    rfid.set_pin2(8, 0)
    time.sleep(0.200)
```