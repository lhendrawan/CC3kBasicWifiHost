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
import argparse
import serial
import time


#===============================================================================
# Constants
#===============================================================================

# version number
BASIC_WIFI_HOST_MAJOR_VERSION = 0
BASIC_WIFI_HOST_MINOR_VERSION = 1
BASIC_WIFI_HOST_BUILD_VERSION = 0

# console command list
BASIC_WIFI_CONSOLE_CMD_SMART_CFG  = 0x01
BASIC_WIFI_CONSOLE_CMD_CONNECT    = 0x02
BASIC_WIFI_CONSOLE_CMD_SOCK_OPEN  = 0x03
BASIC_WIFI_CONSOLE_CMD_SEND_DATA  = 0x04
BASIC_WIFI_CONSOLE_CMD_RCV_DATA   = 0x05
BASIC_WIFI_CONSOLE_CMD_BIND       = 0x06
BASIC_WIFI_CONSOLE_CMD_SOCK_CLOSE = 0x07
BASIC_WIFI_CONSOLE_CMD_IP_CFG     = 0x08
BASIC_WIFI_CONSOLE_CMD_DISCONNECT = 0x09
BASIC_WIFI_CONSOLE_CMD_DEL_POLICY = 0x0A
BASIC_WIFI_CONSOLE_CMD_MDNS_ADV   = 0x0B
EXIT_CMD = 0x00

# console command list
BASIC_WIFI_SCRIPT_CMD_SMART_CFG    = "SMART_CFG"
BASIC_WIFI_SCRIPT_CMD_CONNECT      = "CONNECT"
BASIC_WIFI_SCRIPT_CMD_SOCK_OPEN    = "SOCK_OPEN"
BASIC_WIFI_SCRIPT_CMD_SEND_DATA    = "SEND"
BASIC_WIFI_SCRIPT_CMD_RCV_DATA     = "RECEIVE"
BASIC_WIFI_SCRIPT_CMD_BIND         = "BIND"
BASIC_WIFI_SCRIPT_CMD_SOCK_CLOSE   = "SOCK_CLOSE"
BASIC_WIFI_SCRIPT_CMD_IP_CFG       = "IP_CFG"
BASIC_WIFI_SCRIPT_CMD_DISCONNECT   = "DISCONNECT"
BASIC_WIFI_SCRIPT_CMD_DEL_POLICY   = "DEL_POLICY"
BASIC_WIFI_SCRIPT_CMD_MDNS_ADV     = "MDNS_ADV"
BASIC_WIFI_SCRIPT_CMD_PRINT_STATUS = "PRINT_STATUS"
BASIC_WIFI_SCRIPT_CMD_DELAY        = "DELAY"


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
    # local IP address string
    local_ip_addr = ""
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
    # print status
    #---------------------------------------------------------------------------
    def print_status(self):
        print "\r\n STATUS:"
        print "  - Access Point SSID :",
        if(self.ap_ssid == ""):
            print "- (not connected)"
        else:
            print self.ap_ssid
        print "  - Local IP Address  :",
        if(self.local_ip_addr == ""):
            print "-"
        else:
            print self.local_ip_addr
        print "  - Socket            :",
        if(self.sock_opened == False):
            print "N/A"
        else:
            print "opened"
        print "  - Port              :", self.udp_port
        pass

    #---------------------------------------------------------------------------
    # print console command list
    #---------------------------------------------------------------------------
    def print_console_cmd_list(self):
        print "\r\n------------------------------------------------------------"
        self.print_status()
        print "\r\n------------------------------------------------------------"
        print " Command List:"
        print "------------------------------------------------------------"
        print "", EXIT_CMD, "- exit"
        print "", BASIC_WIFI_CONSOLE_CMD_SMART_CFG, "- run SmartConfig"
        print "", BASIC_WIFI_CONSOLE_CMD_CONNECT, "- connect to AP"
        print "", BASIC_WIFI_CONSOLE_CMD_SOCK_OPEN, "- open (UDP) socket"
        print "", BASIC_WIFI_CONSOLE_CMD_SEND_DATA, "- send data"
        print "", BASIC_WIFI_CONSOLE_CMD_RCV_DATA, "- receive data"
        print "", BASIC_WIFI_CONSOLE_CMD_BIND, "- bind to port"
        print "", BASIC_WIFI_CONSOLE_CMD_SOCK_CLOSE, "- close (UDP) socket"
        print "", BASIC_WIFI_CONSOLE_CMD_IP_CFG, "- configure static IP"
        print "", BASIC_WIFI_CONSOLE_CMD_DISCONNECT, "- disconnect from AP"
        print "", BASIC_WIFI_CONSOLE_CMD_DEL_POLICY, "- delete policy"
        print "", BASIC_WIFI_CONSOLE_CMD_MDNS_ADV, "- send mDNS advertisement"
        print "------------------------------------------------------------"
        print "\r\nEnter command:",
        pass

    #---------------------------------------------------------------------------
    # print script command list
    #---------------------------------------------------------------------------
    def print_script_cmd_list(self, cmd_string):
        print "\r\n SCRIPT CMD USAGE:"
        if(cmd_string == "") or (cmd_string == BASIC_WIFI_SCRIPT_CMD_SMART_CFG):
            print BASIC_WIFI_SCRIPT_CMD_SMART_CFG
            pass

        if(cmd_string == "") or (cmd_string == BASIC_WIFI_SCRIPT_CMD_CONNECT):
            print BASIC_WIFI_SCRIPT_CMD_CONNECT, "<SSID_NAME>"
            pass

        if(cmd_string == "") or (cmd_string == BASIC_WIFI_SCRIPT_CMD_SOCK_OPEN):
            print BASIC_WIFI_SCRIPT_CMD_SOCK_OPEN
            pass

        if(cmd_string == "") or (cmd_string == BASIC_WIFI_SCRIPT_CMD_SEND_DATA):
            print BASIC_WIFI_SCRIPT_CMD_SEND_DATA, "<DEST_IP_ADDR> <DEST_PORT> <DATA>"
            pass

        if(cmd_string == "") or (cmd_string == BASIC_WIFI_SCRIPT_CMD_RCV_DATA):
            print BASIC_WIFI_SCRIPT_CMD_RCV_DATA
            pass

        if(cmd_string == "") or (cmd_string == BASIC_WIFI_SCRIPT_CMD_BIND):
                pass

        if(cmd_string == "") or (cmd_string == BASIC_WIFI_SCRIPT_CMD_SOCK_CLOSE):
            print BASIC_WIFI_SCRIPT_CMD_SOCK_CLOSE
            pass

        if(cmd_string == "") or (cmd_string == BASIC_WIFI_SCRIPT_CMD_IP_CFG):
            print BASIC_WIFI_SCRIPT_CMD_DISCONNECT
            pass

        if(cmd_string == "") or (cmd_string == BASIC_WIFI_SCRIPT_CMD_DEL_POLICY):
            print BASIC_WIFI_SCRIPT_CMD_DEL_POLICY
            pass

        if(cmd_string == "") or (cmd_string == BASIC_WIFI_SCRIPT_CMD_MDNS_ADV):
            print BASIC_WIFI_SCRIPT_CMD_MDNS_ADV
            pass

        if(cmd_string == "") or (cmd_string == BASIC_WIFI_SCRIPT_CMD_DELAY):
            print BASIC_WIFI_SCRIPT_CMD_DELAY, "<DELAY_TIME_IN_MS>"
            pass

        if(cmd_string == "") or (cmd_string == BASIC_WIFI_SCRIPT_CMD_PRINT_STATUS):
            pass

    #---------------------------------------------------------------------------
    # wait for acknowledgement from CC3000 after sending command
    #---------------------------------------------------------------------------
    def wait_ack(self):
        line =""
        # ack contains "DONE" string
        while(line.find("DONE") == -1):
            line = self.read_line_target()
            self.print_line_target(line)
        pass

    #---------------------------------------------------------------------------
    # convert IPv4 address string to hexadecimal byte string
    #---------------------------------------------------------------------------
    def ip_addr_str_to_hex_bytes(self, ip_addr_str):
        hex_str = ""
        # parse the IP address string
        try:
            addr_array = ip_addr_str.split('.')
            if(len(addr_array) == 4):
                for byte in addr_array:
                    if((int(byte)) < 255):
                        hex_str += "%0.2x" % int(byte)
                    else:
                        # invalid integer value (> 255)
                        return ""
                # success - return hex bytes
                return hex_str
            else:
                # invalid IPv4 address format xxx.xxx.xxx.xxx
                return ""
        except:
            return ""

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
        self.wait_ack()

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
            self.wait_ack()

            # parser for local IP address information
            line =""
            while(line.find("IP:") == -1):
                line = self.read_line_target()
                self.print_line_target(line)
            ip_addr_str = line.split(":")[1]
            ip_addr_str = ip_addr_str.strip('\f')
            ip_addr_str = ip_addr_str.strip('\r')
            ip_addr_str = ip_addr_str.strip('\f')
            # check if the IP address format is valid
            if(self.ip_addr_str_to_hex_bytes(ip_addr_str) != ""):
                # valid IP address format
                self.local_ip_addr = ip_addr_str
                print "Connected - local IP Addr:", self.local_ip_addr
                #set flag
                self.ap_ssid = ssid
            else:
                # invalid IP address format - should not happen actually
                print "ERROR: invalid IP address:", ip_addr_str
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
        self.wait_ack()

        # set flag
        self.sock_opened = True

        print "Socket successfully opened\r\n"

        pass

    #---------------------------------------------------------------------------
    # send data
    #---------------------------------------------------------------------------
    def send_data(self, addr_str, port_str, data_str):
        # print out parameter
        print "\r\nSending data:"
        print " - Address :", addr_str
        if(self.ip_addr_str_to_hex_bytes(addr_str) == ""):
            print "ERROR: invalid IPv4 address format -", addr_str
            return
        print " - Port    :", port_str, "/", hex(int(port_str))
        print " - Data    :", data_str

        # construct command message
        msg = "04" + "%0.2X" % len(data_str)
        msg += data_str
        msg += "02" + "%0.4x" % int(port_str)
        msg += self.ip_addr_str_to_hex_bytes(addr_str)
        msg += '\r'
        print "[DBG] Send Data MSG:", msg

        # send command message
        self.serial_port.write(msg)

        # wait for acknowledgement
        self.wait_ack()

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
        self.wait_ack()

        print "Data successfully received\r\n"

        pass

    #---------------------------------------------------------------------------
    # bind
    #---------------------------------------------------------------------------
    def bind(self, port_str):
        print "\r\nBinding port:", port_str, "/", hex(int(port))

        # construct command message
        msg = "06" + "%0.4x" % int(port_str)
        msg += "\r"
        print "[DBG] Bind port MSG:", msg

        # send command message
        self.serial_port.write(msg)

        # wait for acknowledgement
        self.wait_ack()

        # set flag
        self.udp_port = port

        print "Successfully binding UDP port", port, "\r\n"

        pass

    #---------------------------------------------------------------------------
    # close socket
    #---------------------------------------------------------------------------
    def close_sock(self):
        print "\r\nClosing (UDP) socket"

        # construct command message
        msg = "07" + "\r"
        print "[DBG] Close Socket MSG:", msg

        # send command message
        self.serial_port.write(msg)

        # wait for acknowledgement
        self.wait_ack()

        # reset flag
        self.sock_opened = False
        self.udp_port = 0

        print "Socket successfully closed\r\n"

        pass

    #---------------------------------------------------------------------------
    # IP configure
    #---------------------------------------------------------------------------
    def ip_cfg(self, local_addr_str, gateway_str):
        # print out parameter
        print "\r\nConfigure Static IP"
        print " - Local Address :", local_addr_str
        if(self.ip_addr_str_to_hex_bytes(local_addr_str) == ''):
            print "ERROR: invalid IPv4 address format -", local_addr_str
            return
        print " - Gateway       :", gateway_str
        if(self.ip_addr_str_to_hex_bytes(gateway_str) == ''):
            print "ERROR: invalid IPv4 address format -", gateway_str
            return

        # construct command message
        msg = "08"
        msg += self.ip_addr_str_to_hex_bytes(local_addr_str)
        msg += self.ip_addr_str_to_hex_bytes(gateway_str)
        print "[DBG] Send Data MSG:", msg

        # send command message
        self.serial_port.write(msg)

        # wait for acknowledgement
        self.wait_ack()

        # save local ip address
        self.local_ip_addr = local_addr_str

        print "Successfully setting static IP configuration\r\n"

        pass

    #---------------------------------------------------------------------------
    # disconnect from an AP
    #---------------------------------------------------------------------------
    def disconnect(self):
        print "\r\nDisconnect from AP"

        # construct command message
        msg = "09" + "\r"
        print "[DBG] Disconnect MSG:", msg

        # send command message
        self.serial_port.write(msg)

        # wait for acknowledgement
        self.wait_ack()

        # reset flag
        self.ap_ssid = ""
        self.local_ip_addr = ""

        print "Disconnecting from AP succeeds\r\n"

        pass

    #---------------------------------------------------------------------------
    # delete policy
    #---------------------------------------------------------------------------
    def del_policy(self):
        print "\r\nDelete Policy"

        # construct command message
        msg = "0A" + "\r"
        print "[DBG] Deletec Policy MSG:", msg

        # send command message
        self.serial_port.write(msg)

        # wait for acknowledgement
        self.wait_ack()

        print "Deleting policy succeeds\r\n"

        pass

    #---------------------------------------------------------------------------
    # send mDNS advert
    #---------------------------------------------------------------------------
    def mdns_advert(self):
        print "\r\nmDNS Advertisement"

        # construct command message
        msg = "0B" + "\r"
        print "[DBG] mDNS Advert MSG:", msg

        # send command message
        self.serial_port.write(msg)

        # wait for acknowledgement
        self.wait_ack()

        print "Sending mDNS advertisement succeeds\r\n"

        pass

    #---------------------------------------------------------------------------
    # run console
    #---------------------------------------------------------------------------
    def run_console(self):
        # main loop
        exit = 0
        while(exit == 0):
            # print out command
            self.print_console_cmd_list()

            try:
                # read command from user
                cmd = int(raw_input()[0])

                # process command
                if(cmd == BASIC_WIFI_CONSOLE_CMD_SMART_CFG):
                    self.run_smartcfg()

                elif(cmd == BASIC_WIFI_CONSOLE_CMD_CONNECT):
                    # ask for SSID name input
                    print "Enter AP SSID:",
                    ssid = raw_input()
                    self.connect(ssid)

                elif(cmd == BASIC_WIFI_CONSOLE_CMD_SOCK_OPEN):
                    self.open_sock()

                elif(cmd == BASIC_WIFI_CONSOLE_CMD_SEND_DATA):
                    # ask for address, port, and data to be sent
                    print "Enter destination address:",
                    addr_str = raw_input()
                    print "Enter destination port:",
                    port_str = raw_input()
                    print "Enter data to be sent:",
                    data = raw_input()
                    self.send_data(addr_str, port_str, data)

                elif(cmd == BASIC_WIFI_CONSOLE_CMD_RCV_DATA):
                    self.rcv_data()

                elif(cmd == BASIC_WIFI_CONSOLE_CMD_BIND):
                    # ask for UDP port input
                    print "Enter bind port:",
                    port_str = raw_input()
                    self.bind(port_str)

                elif(cmd == BASIC_WIFI_CONSOLE_CMD_SOCK_CLOSE):
                    self.close_sock()

                elif(cmd == BASIC_WIFI_CONSOLE_CMD_IP_CFG):
                    # ask for local address input
                    print "Enter local address:",
                    local_addr_str = raw_input()

                    # ask for gateway address input
                    print "Enter gateway address:",
                    gateway_addr_str = raw_input()

                    # process input
                    self.ip_cfg(local_addr_str, gateway_addr_str)

                elif(cmd == BASIC_WIFI_CONSOLE_CMD_DISCONNECT):
                    self.disconnect()

                elif(cmd == BASIC_WIFI_CONSOLE_CMD_DEL_POLICY):
                    self.del_policy()

                elif(cmd == BASIC_WIFI_CONSOLE_CMD_MDNS_ADV):
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


    #---------------------------------------------------------------------------
    # parse input file name
    #---------------------------------------------------------------------------
    def parse_file(self, file_name):
        print "Parsing input file:", file_name
        try:
            file = open(file_name, 'r')
        except:
            print "ERROR: failed to open", file_name

        for line in file:
            # strip newline characters
            line = line.strip('\r')
            line = line.strip('\n')

            # remove multiple consecutive whitespaces
            line_str = ""
            is_space = False
            for ch in line:
                if (ch != ' '):
                    # not whitespace, add to string
                    line_str += ch
                    # mark that it is not a white space char
                    is_space = False
                else:
                    # check whether it is consecutive whitespce
                    if(is_space == False):
                        line_str += ch
                        # mark flag
                        is_space = True
            line = line_str
            if (line != "") and (line != " "):
                print "[LINE]", line

            # split words in the command line
            words = line.split(' ')
            #print "\r\n[DEBUG]:", words, len(words)

            # first word is the command
            if(words[0] == BASIC_WIFI_SCRIPT_CMD_SMART_CFG):
                if(len(words) != 1):
                    print BASIC_WIFI_SCRIPT_CMD_SMART_CFG, "doesn't accept any parameter"
                    self.print_script_cmd_list
                    sys.exit(1)
                else:
                    try:
                        # process input
                        self.run_smartcfg()
                    except:
                        print "ERROR: fail to execute", BASIC_WIFI_SCRIPT_CMD_SMART_CFG
                pass

            elif(words[0] == BASIC_WIFI_SCRIPT_CMD_CONNECT):
                if(len(words) != 2):
                    print BASIC_WIFI_SCRIPT_CMD_CONNECT, "only accept one parameter:"
                    self.print_script_cmd_list
                    sys.exit(1)
                else:
                    try:
                        # process input
                        self.connect(words[1])
                    except:
                        print "ERROR: fail to execute", BASIC_WIFI_SCRIPT_CMD_CONNECT
                pass

            elif(words[0] == BASIC_WIFI_SCRIPT_CMD_SOCK_OPEN):
                if(len(words) != 1):
                    print BASIC_WIFI_SCRIPT_CMD_SOCK_OPEN, "doesn't accept any parameter"
                    self.print_script_cmd_list
                else:
                    try:
                        # process input
                        self.open_sock()
                    except:
                        print "ERROR: fail to execute", BASIC_WIFI_SCRIPT_CMD_SOCK_OPEN
                pass

            elif(words[0] == BASIC_WIFI_SCRIPT_CMD_SEND_DATA):
                if(len(words) != 4):
                    print BASIC_WIFI_SCRIPT_CMD_SEND_DATA, "requires 3 parameters"
                    self.print_script_cmd_list
                else:
                    try:
                        # process input
                        self.send_data(words[1], words[2], words[3])
                    except:
                        print "ERROR: fail to execute", BASIC_WIFI_SCRIPT_CMD_SEND_DATA
                pass

            elif(words[0] == BASIC_WIFI_SCRIPT_CMD_RCV_DATA):
                if(len(words) != 1):
                    print BASIC_WIFI_SCRIPT_CMD_RCV_DATA, "doesn't accept any parameter"
                    self.print_script_cmd_list
                else:
                    try:
                        # process input
                        self.rcv_data()
                    except:
                        print "ERROR: fail to execute", BASIC_WIFI_SCRIPT_CMD_RCV_DATA
                pass

            elif(words[0] == BASIC_WIFI_SCRIPT_CMD_BIND):
                if(len(words) != 2):
                    print BASIC_WIFI_SCRIPT_CMD_BIND, "only accept one parameter:"
                    self.print_script_cmd_list
                    sys.exit(1)
                else:
                    try:
                        # process input
                        self.bind(words[1])
                    except:
                        print "ERROR: fail to execute", BASIC_WIFI_SCRIPT_CMD_BIND
                pass

            elif(words[0] == BASIC_WIFI_SCRIPT_CMD_SOCK_CLOSE):
                if(len(words) != 1):
                    print BASIC_WIFI_SCRIPT_CMD_SOCK_CLOSE, "doesn't accept any parameter"
                    self.print_script_cmd_list
                    sys.exit(1)
                else:
                    try:
                        # process input
                        self.close_sock()
                    except:
                        print "ERROR: fail to execute", BASIC_WIFI_SCRIPT_CMD_SOCK_CLOSE
                pass

            elif(words[0] == BASIC_WIFI_SCRIPT_CMD_IP_CFG):
                pass

            elif(words[0] == BASIC_WIFI_SCRIPT_CMD_DISCONNECT):
                if(len(words) != 1):
                    print BASIC_WIFI_SCRIPT_CMD_DISCONNECT, "doesn't accept any parameter"
                    self.print_script_cmd_list
                    sys.exit(1)
                else:
                    try:
                        # process input
                        self.disconnect()
                    except:
                        print "ERROR: fail to execute", BASIC_WIFI_SCRIPT_CMD_DISCONNECT
                pass

            elif(words[0] == BASIC_WIFI_SCRIPT_CMD_DEL_POLICY):
                if(len(words) != 1):
                    print BASIC_WIFI_SCRIPT_CMD_DEL_POLICY, "doesn't accept any parameter"
                    self.print_script_cmd_list
                    sys.exit(1)
                else:
                    try:
                        # process input
                        self.del_policy()
                    except:
                        print "ERROR: fail to execute", BASIC_WIFI_SCRIPT_CMD_DEL_POLICY
                pass

            elif(words[0] == BASIC_WIFI_SCRIPT_CMD_MDNS_ADV):
                if(len(words) != 1):
                    print BASIC_WIFI_SCRIPT_CMD_MDNS_ADV, "doesn't accept any parameter"
                    self.print_script_cmd_list
                    sys.exit(1)
                else:
                    try:
                        # process input
                        self.mdns_advert()
                    except:
                        print "ERROR: fail to execute", BASIC_WIFI_SCRIPT_CMD_MDNS_ADV
                pass

            elif(words[0] == BASIC_WIFI_SCRIPT_CMD_DELAY):
                try:
                    delay_time_ms = int(words[1])/1000
                    print "Sleeping for", delay_time_ms, "s"
                    time.sleep(delay_time_ms)
                except:
                    print BASIC_WIFI_SCRIPT_CMD_DELAY, "only accept one parameter:"
                    self.print_script_cmd_list
                    sys.exit(1)
                pass

            elif(words[0] == BASIC_WIFI_SCRIPT_CMD_PRINT_STATUS):
                if(len(words) != 1):
                    print BASIC_WIFI_SCRIPT_CMD_PRINT_STATUS, "doesn't accept any parameter"
                    self.print_script_cmd_list
                    sys.exit(1)
                else:
                    try:
                        # process input
                        self.print_status()
                    except:
                        print "ERROR: fail to execute", BASIC_WIFI_SCRIPT_CMD_PRINT_STATUS
                pass

            elif (words[0] != ''):
                if(words[0][0] == '/') and (words[0][1] == '/'):
                    # this is a comment line, ignore
                    pass
                else:
                    # unknown command
                    print "ERROR: unknown command"
                    self.print_script_cmd_list("");
                pass

#===============================================================================
# main script
#===============================================================================
if __name__ == '__main__':

    #parse the command line parameters using OptionParser
    parser = argparse.ArgumentParser(description='CC3000 Basic WiFi Host Script')
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-c", "--console", action="store_true", help="run console")
    group.add_argument("-f", "--file", action="store", help="input script file")
    parser.add_argument("-p", "--port", help="serial port name with name PORT",
            action="store")
    args = parser.parse_args()
    # debug
    #print args

    version_str = str(BASIC_WIFI_HOST_MAJOR_VERSION) + "." + \
                    str(BASIC_WIFI_HOST_MINOR_VERSION) + "." + \
                    str(BASIC_WIFI_HOST_BUILD_VERSION)
    print "\r\n------------------------------------------------------------"
    print " CC3000 BasicWiFi Host Script"
    print " Version:", version_str
    print "------------------------------------------------------------\r\n"

    # check mandatory parameter
    if(args.port == None):
        print "ERROR: Serial Port parameter is missing!"
        parser.print_help()
        sys.exit(1)

    # instantiate BasicWiFiHost
    host = BasicWiFiHost(args.port)

    # open serial port
    try:
        print "Opening Serial Port:", host.serial_port_name
        # 9600 8N1 is the default setting
        host.serial_port = serial.Serial(host.serial_port_name)
    except:
        print "ERROR: Failed to open serial port"
        sys.exit(1)

    # waiting for innitial message from target
    print "Waiting for initial message from target - reset target if necessary"
    line =""
    while(line.find("Example App") == -1):
        line = host.read_line_target()
        host.print_line_target(line)

    # choose run mode
    if(args.console == True):
        # run the host console
        host.run_console()
        pass

    elif (args.file != None):
        # parse input file name
        host.parse_file(args.file)
        pass

    else:
        print "ERROR: invalid parameters! Must choose between -c and -f"
        parser.print_help()
        sys.exit(1)

    pass
