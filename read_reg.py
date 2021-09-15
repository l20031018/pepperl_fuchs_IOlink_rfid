#!/usr/bin/env python
# -*- coding: utf-8 -*-

# read_register
# read 10 registers and print result on stdout

# you can use the tiny modbus server "mbserverd" to test this code
# mbserverd is here: https://github.com/sourceperl/mbserverd

# the command line modbus client mbtget can also be useful
# mbtget is here: https://github.com/sourceperl/mbtget

from pyModbusTCP.client import ModbusClient
from pyModbusTCP import utils
import time
   
# if ICE2 or ICE3 modubus tcp address is 1, PDI registers address of port1 is 1000, PDI registers address of port2 is 2000 ...
#                                           PDO registers address of port1 is 1050, PDO registers address of port2 is 2050 ...

class ICE_modubus_rfid:
    
    def __init__(self, ice_ip, port):
        self.ice_ip = ice_ip
        self.port = port
        self.c = ModbusClient()
        self.c.host(self.ice_ip)
        self.c.port(self.port)
        #self.c.debug(True)
        self.connect()
        
        self.device_port = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0}
        self.read_block_size_port = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0}
        self.write_block_size_port = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0}
        for i in range(8):
            device_name = self.device_name2str(self.read_reg(i+1, "device", 32))
            if device_name != '':
                self.device_port[i+1] = device_name 
            time.sleep(0.05)
        for k,v in self.device_port.items():
            if v != 0:
                print("device attached on port " + str(k) + ":  "+v)
                self.read_block_size_port[k] = self.ISDU_data_access(k, 'r', 204, 2, [0,])
                self.write_block_size_port[k] = self.ISDU_data_access(k, 'r', 205, 2, [0,])
        #self.PDI_data_block_size = self.read_reg("ISDU")
        print(self.read_block_size_port)
        print(self.write_block_size_port)
    
   
    
    def device_name2str(self,l):
        s=''
        for i in range(len(l)):
            if l[i] == 0:
                break
            s+=chr(l[i]>>8)
            s+=chr(l[i]&0xff)
        return s    
    
    def ISDU_data_access(self, IO_port, access_mode, index, subindex, data):
        if access_mode == 'r':
            #if access_mode is r, data should be[0]
            
            data.insert(0, 1)
            data.insert(0, subindex)
            data.insert(0, index)
            data.insert(0, 1)
            for i in range(16-len(data)):
                data.append(0)
            #data.insert(-2, 0)
            print(data)
            self.write_reg( IO_port, "ISDU", data )
            time.sleep(0.1)
            return self.read_reg(IO_port, "ISDU", 6)
        if access_mode == 'w':
            data.insert(0, 1)
            data.insert(0, subindex)
            data.insert(0, index)
            data.insert(0, 2)
            for i in range(16-len(data)):
                data.append(0)            
            #data.insert(-2, 0)
            print(data)
            self.write_reg( IO_port, "ISDU", data )
            return self.read_reg(IO_port, "ISDU", 6)
       
    def device_type_to_address(self, IO_port):
        numbers = {
            1 : 1564,
            2 : 2564,
            3 : 3564,
            4 : 4564,
            5 : 5564,
            6 : 6564,
            7 : 7564,
            8 : 8564
        }
        return numbers.get(IO_port, None)        
    
    
    def PDI_port_to_address(self, IO_port):
        numbers = {
            1 : 999,
            2 : 1999,
            3 : 2999,
            4 : 3999,
            5 : 4999,
            6 : 5999,
            7 : 6999,
            8 : 7999
        }
        return numbers.get(IO_port, None)
        
        
    def PDO_port_to_address(self, IO_port):
        numbers = {
            1 : 1049,
            2 : 2049,
            3 : 3049,
            4 : 4049,
            5 : 5049,
            6 : 6049,
            7 : 7049,
            8 : 8049
        }
        return numbers.get(IO_port, None)        


    def recv_ISDU_port_to_address(self, IO_port):
        numbers = {
            1 : 1100,
            2 : 2100,
            3 : 3100,
            4 : 4100,
            5 : 5100,
            6 : 6100,
            7 : 7100,
            8 : 8100
        }
        return numbers.get(IO_port, None)


    def send_ISDU_port_to_address(self, IO_port):
        numbers = {
            1 : 1300,
            2 : 2300,
            3 : 3300,
            4 : 4300,
            5 : 5300,
            6 : 6300,
            7 : 7300,
            8 : 8300
        }
        return numbers.get(IO_port, None)


    def connect(self): 
        
        while True:
            if not self.c.is_open():
                if not self.c.open():
                    print("unable to connect to "+self.ice_ip+":"+str(self.port)) 
                    time.sleep(2)
                else:
                    print("connected to "+self.ice_ip+":"+str(self.port))
                    break 

    def read_reg(self, IO_port, data_type, lentgh):  
        if data_type == "PDI" :
            reg_address = self.PDI_port_to_address(IO_port)
        if data_type == "PDO" :
            reg_address = self.PDO_port_to_address(IO_port)
        if data_type == "ISDU" :
            reg_address = self.recv_ISDU_port_to_address(IO_port) 
        if data_type == "device" :
            reg_address = self.device_type_to_address(IO_port)        
        #print (reg_address)
        if self.c.is_open():
            # read 10 registers at address 0, store result in regs list
            regs = self.c.read_holding_registers(reg_address, lentgh)
            # if success display registers
            if regs:
                #print("reg ad #0 to 9: "+str(regs))
                return regs  
            else:
                return regs            
 #write_multiple_registers(regs_addr, regs_value)   
 
    def write_reg(self, IO_port, data_type, data ):
        if data_type == "PDO" :
            reg_address = self.PDO_port_to_address(IO_port)
        if data_type == "ISDU" :
            reg_address = self.send_ISDU_port_to_address(IO_port)    
        #print ("reg_address", reg_address)            
        if self.c.is_open():
            # read 10 registers at address 0, store result in regs list
            regs = self.c.write_multiple_registers(reg_address, data)
            # if success display registers
            
            return regs 
            
            
    def read_tag(self, IO_port):
        list_16_bits =rfid.read_reg(IO_port, "PDI", 16)
        #print ("^^^^####", list_16_bits)
        #print(utils.get_bits_from_int(list_16_bits[0], val_size=16)[9],utils.get_bits_from_int(list_16_bits[2], val_size=16)[8])
        if utils.get_bits_from_int(list_16_bits[0], val_size=16)[9]==1 and utils.get_bits_from_int(list_16_bits[2], val_size=16)[8]==1:
            uid_data = list_16_bits[4:8]
            #print("read success. uid:",uid_data)

            #配置读取数据为user memory
            rfid.ISDU_data_access(IO_port, 'w', 204, 1, [0x00])
            time.sleep(0.24)
            list_16_bits =rfid.read_reg(IO_port, "PDI", 16)
            #print("in if", list_16_bits)
            if utils.get_bits_from_int(list_16_bits[0], val_size=16)[9]==1 and utils.get_bits_from_int(list_16_bits[2], val_size=16)[8]==1 and list_16_bits[4:8] != uid_data:
                #print("user memory:", list_16_bits[4:8])
                #配置读取数据为uid
                rfid.ISDU_data_access(IO_port, 'w', 204, 1, [0x8000])
                return uid_data, list_16_bits[4:8]
            else:
                rfid.ISDU_data_access(IO_port, 'w', 204, 1, [0x8000])
                return 0
        else:
            rfid.ISDU_data_access(IO_port, 'w', 204, 1, [0x8000])
            return 0
        
        
    def set_mode_easy_autostart_off(self, IO_port):
        return self.ISDU_data_access(IO_port, 'w', 204, 4, [0x0])
       
    def set_mode_easy_autostart_on(self, IO_port):
        return self.ISDU_data_access(IO_port, 'w', 204, 4, [0x8000])

    def write_tag_data(self, IO_port, data):        
        #data is a list each element lentgh is  2 bytes eg. [0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        
        write_data = [512,0]+data
        if self.write_reg(IO_port, "PDO", write_data):
            print("write done")
        #写复位
        self.write_reg(IO_port, "PDO", [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] )
    
    def set_pin2(self, port, status):
        # before use this function, pin 2 on this port has to be set as DO
        if status == 1:
            self.write_reg(port, "PDO", [256,0,0])
        else:
            self.write_reg(port, "PDO", [0,0,0])
            
    def get_pin2(self, port):
            list_16_bits =rfid.read_reg(port, "PDI", 16)
            print(rfid.read_reg(port, "PDI", 16))
            #print([hex(i) for i in list_16_bits])
            if utils.get_bits_from_int(list_16_bits[2], val_size=16)[8]==1:
                return 1
            else:
                return 0
    
    

if __name__ == "__main__":
    rfid = ICE_modubus_rfid('192.168.1.250', 502)
    #rfid.connect()
    #设置port1读取UID
    rfid.ISDU_data_access(1, 'w', 204, 1, [0x8000])
    #设置port1自动读取
    rfid.set_mode_easy_autostart_on(1)
    time.sleep(1)
    for i in range(10):
        tag_data = rfid.read_tag(1)
        if tag_data:
            #这里可更具业务逻辑判断uid是否合规
            #do something 
            print(tag_data)  #[uid, user memory]  8 bytes both uid and user memory
            time.sleep(0.24)
        time.sleep(0.05)
        #time.sleep(0.1)
    #time.sleep(0.1)
    #list_32_bits = utils.word_list_to_long(rfid.read_reg(1, "PDI", 16))
    #print([hex(i) for i in list_32_bits])
    #rfid.set_mode_easy_autostart_off(1)
    #time.sleep(0.1)
    rfid.write_tag_data(1,[0x0102,0x0304,0x0102,0x0102,0,0,0,0,0,0,0,0,0,0])
    time.sleep(0.2)
    #rfid.set_mode_easy_autostart_on(3)
    #rfid.read_tag(1)
    #time.sleep(0.2)
    #list_32_bits = utils.word_list_to_long(rfid.read_reg(1, "PDI", 16))
    #d = [i for i in list_32_bits]
    #s = 0x00
    #for i in d:
    #   s<<32^i
    #print(s)
    print("port 7 Pin4 status:", rfid.get_pin2(7))
    
    
    for i in range(10):
        rfid.set_pin2(2, 1)
        rfid.set_pin2(3, 1)
        time.sleep(0.150)
        rfid.set_pin2(2, 0)
        rfid.set_pin2(3, 0)
        time.sleep(0.150)
    for i in range(10):
        rfid.set_pin2(5, 1)
        rfid.set_pin2(4, 1)
        time.sleep(0.150)
        rfid.set_pin2(5, 0)
        rfid.set_pin2(4, 0)
        time.sleep(0.150)
    rfid.set_mode_easy_autostart_off(1)
    
    
    