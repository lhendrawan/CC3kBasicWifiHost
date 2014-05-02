#===============================================================================
# Copyright (c) 2014, Leo Hendrawan
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
# 3. Neither the name of the Leo Hendrawan nor the
#    names of its contributors may be used to endorse or promote products
#    derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY LEO HENDRAWAN ''AS IS'' AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#===============================================================================

#-------------------------------------------------------------------------------
# Name:        BasicWiFiHost
#
# Description: host for Basic WiFi module example
#
# Author:      Leo Hendrawan
#
# Version:     0.1.0
#
# Note:        This module requires pyserial (http://pyserial.sourceforge.net/)
#
# Log:
#     - Version 0.1 (2014.04.09) :
#       Hello World! (created)
#
#-------------------------------------------------------------------------------
#!/usr/bin/env python


import sys
import optparse
import serial


#===============================================================================
# Constants
#===============================================================================

# version number
BASIC_WIFI_HOST_MAJOR_VERSION = 0
BASIC_WIFI_HOST_MINOR_VERSION = 1
BASIC_WIFI_HOST_BUILD_VERSION = 0

# command list
BASIC_WIFI_CMD_SMART_CFG  = 0x01
BASIC_WIFI_CMD_CONNECT    = 0x02
BASIC_WIFI_CMD_SOCK_OPEN  = 0x03
BASIC_WIFI_CMD_SEND_DATA  = 0x04
BASIC_WIFI_CMD_RCV_DATA   = 0x05
BASIC_WIFI_CMD_BIND       = 0x06
BASIC_WIFI_CMD_SOCK_CLOSE = 0x07
BASIC_WIFI_CMD_IP_CFG     = 0x08
BASIC_WIFI_CMD_DISCONNECT = 0x09
BASIC_WIFI_CMD_DEL_POLICY = 0x0A
BASIC_WIFI_CMD_MDNS_ADV   = 0x0B
EXIT_CMD = 0x00


#===============================================================================
# BasicWiFiHost class
#===============================================================================
class BasicWiFiHost:
    #---------------------------------------------------------------------------
    # Class variables
    #---------------------------------------------------------------------------
    # serial port name
    serial_port_name = ""
    # serial port handle
    serial_port = 0
    # AP name
    ap_ssid = ""
    # IP address
    ip_addr = []
    # socket opened flag
    sock_opened = False
    # UDP port
    udp_port = 0

    #---------------------------------------------------------------------------
    # Class functions
    #---------------------------------------------------------------------------

    #---------------------------------------------------------------------------
    # init function - instantiation operation
    #---------------------------------------------------------------------------
    def __init__(self, serial_port_name):
        # save com port name
        self.serial_port_name = serial_port_name
        pass

    #---------------------------------------------------------------------------
    # setting serial port name
    #---------------------------------------------------------------------------
    def set_serial_port_name(self, port_name):
        self.serial_port_name = port_name
        pass

    #---------------------------------------------------------------------------
    # read line from target
    #---------------------------------------------------------------------------
    def read_line_target(self):
        msg = ""
        byte = ""
        while(byte != '\r'):
            byte = self.serial_port.read()
            msg = msg + byte
        return msg

    #---------------------------------------------------------------------------
    # print line from target
    #---------------------------------------------------------------------------
    def print_line_target(self, line):
        line = line.strip('\f')
        line = line.strip('\r')
        line = line.strip('\f')
        if (line != ""):
            print "[T]:", line
        pass

    #---------------------------------------------------------------------------
    # print command list
    #---------------------------------------------------------------------------
    def print_cmd_list(self):
        print "\r\n------------------------------------------------------------"
        print " Command List:"
        print "------------------------------------------------------------"
        print "", EXIT_CMD, "- exit"
        print "", BASIC_WIFI_CMD_SMART_CFG, "- run SmartConfig"
        print "", BASIC_WIFI_CMD_CONNECT, "- connect to AP"
        print "", BASIC_WIFI_CMD_SOCK_OPEN, "- open (UDP) socket"
        print "", BASIC_WIFI_CMD_SEND_DATA, "- send data"
        print "", BASIC_WIFI_CMD_RCV_DATA, "- receive data"
        print "", BASIC_WIFI_CMD_BIND, "- bind to port"
        print "", BASIC_WIFI_CMD_SOCK_CLOSE, "- close (UDP) socket"
        print "", BASIC_WIFI_CMD_IP_CFG, "- configure static IP"
        print "", BASIC_WIFI_CMD_DISCONNECT, "- disconnect from AP"
        print "", BASIC_WIFI_CMD_DEL_POLICY, "- delete policy"
        print "", BASIC_WIFI_CMD_MDNS_ADV, "- send mDNS advertisement"
        print "------------------------------------------------------------"
        print " Status:"
        print "  - Access Point SSID :",
        if(self.ap_ssid == ""):
            print "- (not connected)"
        else:
            print self.ap_ssid
        print "  - Local IP Address  :",
        if(self.ip_addr == []):
            print "-"
        else:
            print "%i.%i.%i.%i" % (self.ip_addr[0], self.ip_addr[1], self.ip_addr[2], self.ip_addr[3])
        print "  - Socket            :",
        if(self.sock_opened == False):
            print "N/A"
        else:
            print "opened"
        print "  - Port              :", self.udp_port
        print "------------------------------------------------------------"
        print "\r\nEnter command:",
        pass

    #---------------------------------------------------------------------------
    # run SmartConfig
    #---------------------------------------------------------------------------
    def run_smartcfg(self):
        print "\r\nRunning SmartConfig"
        # construct command message
        msg = "01" + "\r"
        print "[DBG] SmartCfg MSG:", msg
        # send command message
        self.serial_port.write(msg)
        # wait for acknowledgement
        line =""
        while(line.find("DONE") == -1):
            line = self.read_line_target()
            self.print_line_target(line)
        print "SmartConfig success\r\n"
        pass

    #---------------------------------------------------------------------------
    # connect to an AP
    #---------------------------------------------------------------------------
    def connect(self, ssid):
        if(type(ssid) == str) and (len(ssid) < 16):
            print "\r\nConnecting to AP with SSID:", ssid
            # construct command message
            msg = "02" + hex(len(ssid)).split('x')[1] + ssid + "\r"
            print "[DBG] Connect MSG:", msg
            # send command message
            self.serial_port.write(msg)
            # wait for acknowledgement
            line =""
            while(line.find("DONE") == -1):
                line = self.read_line_target()
                self.print_line_target(line)
            # parser for local IP address information
            line =""
            while(line.find("IP:") == -1):
                line = self.read_line_target()
                self.print_line_target(line)
            ip_addr = line.split(":")[1].strip("\f\r").split(".")
            self.ip_addr = []
            for n in ip_addr:
                self.ip_addr.append(int(n))
            print "Connected - local IP Addr: %i.%i.%i.%i" % (self.ip_addr[0], self.ip_addr[1], self.ip_addr[2], self.ip_addr[3])
            #set flag
            self.ap_ssid = ssid
        else:
            print "ERROR: invalid SSID:", ssid, ", max length SSID name is 15 bytes"

        pass

    #---------------------------------------------------------------------------
    # open socket
    #---------------------------------------------------------------------------
    def open_sock(self):
        print "\r\nOpening (UDP) socket"
        # construct command message
        msg = "03" + "\r"
        print "[DBG] Open Socket MSG:", msg
        # send command message
        self.serial_port.write(msg)
        # wait for acknowledgement
        line =""
        while(line.find("DONE") == -1):
            line = self.read_line_target()
            self.print_line_target(line)
        # set flag
        self.sock_opened = True
        print "Socket successfully opened\r\n"
        pass

    #---------------------------------------------------------------------------
    # send data
    #---------------------------------------------------------------------------
    def send_data(self, addr, port, data):
        print "\r\nSending data:"
        print " - Address :",
        i = 0
        addr_str = ""
        for byte in addr:
            addr_str += str(byte)
            i += 1
            if (i != 4):
                addr_str += "."
            else:
                addr_str
        print addr_str
        print " - Port    :", port, "/", hex(port)
        print " - Data    :", data

        # construct command message
        msg = "04" + "%0.2X" % len(data)
        msg += data
        msg += "02" + "%0.4x" % port
        for byte in addr:
            msg += "%0.2x" % int(byte)
        msg += '\r'
        print "[DBG] Send Data MSG:", msg
        # send command message
        self.serial_port.write(msg)

        # wait for acknowledgement
        line =""
        while(line.find("DONE") == -1):
            line = self.read_line_target()
            self.print_line_target(line)
        print "Data successfully sent\r\n"
        pass

    #---------------------------------------------------------------------------
    # receive data
    #---------------------------------------------------------------------------
    def rcv_data(self):
        print "\r\nReceiving data"
        # construct command message
        msg = "05" + "\r"
        print "[DBG] Receive Data MSG:", msg
        # send command message
        self.serial_port.write(msg)
        # wait for acknowledgement
        line =""
        while(line.find("DONE") == -1):
            line = self.read_line_target()
            self.print_line_target(line)
        print "Data successfully received\r\n"
        pass

    #---------------------------------------------------------------------------
    # bind
    #---------------------------------------------------------------------------
    def bind(self, port):
        print "\r\nBinding port:", port, "/", hex(port)
        # construct command message
        msg = "06" + hex(port).split('x')[1] + "\r"
        print "[DBG] Bind port MSG:", msg
        # send command message
        self.serial_port.write(msg)
        # wait for acknowledgement
        line =""
        while(line.find("DONE") == -1):
            line = self.read_line_target()
            self.print_line_target(line)
        # set flag
        self.udp_port = port
        print "Successfully binding UDP port", port, "\r\n"
        pass

    #---------------------------------------------------------------------------
    # close socket
    #---------------------------------------------------------------------------
    def close_sock(self):
        print "\r\Closing (UDP) socket"
        # construct command message
        msg = "07" + "\r"
        print "[DBG] Close Socket MSG:", msg
        # send command message
        self.serial_port.write(msg)
        # wait for acknowledgement
        line =""
        while(line.find("DONE") == -1):
            line = self.read_line_target()
            self.print_line_target(line)
        # reset flag
        self.sock_opened = False
        self.udp_port = 0
        print "Socket successfully closed\r\n"
        pass

    #---------------------------------------------------------------------------
    # IP configure
    #---------------------------------------------------------------------------
    def ip_cfg(self, local_addr, gateway):
        pass

    #---------------------------------------------------------------------------
    # disconnect from an AP
    #---------------------------------------------------------------------------
    def disconnect(self):
        print "\r\Disconnect from AP"
        # construct command message
        msg = "09" + "\r"
        print "[DBG] Disconnect MSG:", msg
        # send command message
        self.serial_port.write(msg)
        # wait for acknowledgement
        line =""
        while(line.find("DONE") == -1):
            line = self.read_line_target()
            self.print_line_target(line)
        # reset flag
        self.ap_ssid = ""
        self.ip_addr = []
        print "Disconnecting from AP succeeds\r\n"
        pass

    #---------------------------------------------------------------------------
    # delete policy
    #---------------------------------------------------------------------------
    def del_policy(self):
        pass

    #---------------------------------------------------------------------------
    # send mDNS advert
    #---------------------------------------------------------------------------
    def mdns_advert(self):
        pass

    #---------------------------------------------------------------------------
    # run console
    #---------------------------------------------------------------------------
    def run_console(self):
        version_str = str(BASIC_WIFI_HOST_MAJOR_VERSION) + "." + \
                    str(BASIC_WIFI_HOST_MINOR_VERSION) + "." + \
                    str(BASIC_WIFI_HOST_BUILD_VERSION)
        print "\r\n------------------------------------------------------------"
        print " CC3000 BasicWiFi Host Script"
        print " Version:", version_str
        print "------------------------------------------------------------\r\n"
        # open serial port
        try:
            print "Opening Serial Port:", self.serial_port_name
            # 9600 8N1 is the default setting
            self.serial_port = serial.Serial(self.serial_port_name)
        except:
            print "ERROR: Failed to open serial port"
            sys.exit(1)

        # waiting for innitial message from target
        print "Waiting for initial message from target - reset target if necessary"
        line =""
        while(line.find("Example App") == -1):
            line = self.read_line_target()
            self.print_line_target(line)

        # main loop
        exit = 0
        while(exit == 0):
            # print out command
            self.print_cmd_list()

            try:
                # read command from user
                cmd = int(raw_input()[0])

                # process command
                if(cmd == BASIC_WIFI_CMD_SMART_CFG):
                    self.run_smartcfg()

                elif(cmd == BASIC_WIFI_CMD_CONNECT):
                    # ask for SSID name input
                    print "Enter AP SSID:",
                    ssid = raw_input()
                    self.connect(ssid)

                elif(cmd == BASIC_WIFI_CMD_SOCK_OPEN):
                    self.open_sock()

                elif(cmd == BASIC_WIFI_CMD_SEND_DATA):
                    # ask for address, port, and data to be sent
                    print "Enter destination address:",
                    addr_str = raw_input()
                    try:
                        addr = addr_str.split('.')
                        if(len(addr) != 4):
                            print "ERROR: invalid destination address length (must be 4 bytes)!"
                    except:
                        print "ERROR: invalid destination address!"
                    print "Enter destination port:",
                    port = raw_input()
                    print "Enter data to be sent:",
                    data = raw_input()
                    self.send_data(addr, int(port), data)

                elif(cmd == BASIC_WIFI_CMD_RCV_DATA):
                    self.rcv_data()

                elif(cmd == BASIC_WIFI_CMD_BIND):
                    # ask for UDP port input
                    print "Enter bind port:",
                    port = raw_input()
                    self.bind(int(port))

                elif(cmd == BASIC_WIFI_CMD_SOCK_CLOSE):
                    self.close_sock()

                elif(cmd == BASIC_WIFI_CMD_IP_CFG):
                    self.ip_cfg()

                elif(cmd == BASIC_WIFI_CMD_DISCONNECT):
                    self.disconnect()

                elif(cmd == BASIC_WIFI_CMD_DEL_POLICY):
                    self.del_policy()

                elif(cmd == BASIC_WIFI_CMD_MDNS_ADV):
                    self.mdns_advert()

                elif(cmd == EXIT_CMD):
                    print "\r\nExiting...\r\n"
                    exit = 1

                else:
                    print "ERROR: invalid command!"
            except:
                print "ERROR: invalid command/input failed!"
                pass

        pass

#===============================================================================
# main script
#===============================================================================
if __name__ == '__main__':

    #parse the command line parameters using OptionParser
    cmd_line_parser = optparse.OptionParser()
    cmd_line_parser.add_option("-p", "--port", action="store", type="string",
            dest="serial_port_name", help="serial port name with name PORT",
            metavar="PORT")
    (options, args) = cmd_line_parser.parse_args()

    # check mandatory parameter
    if(options.serial_port_name == None):
        print "ERROR: Serial Port parameter is missing!"
        cmd_line_parser.print_help()
        sys.exit(1)

    # instantiate BasicWiFiHost
    host = BasicWiFiHost(options.serial_port_name)

    # run the host console
    host.run_console()

    pass
