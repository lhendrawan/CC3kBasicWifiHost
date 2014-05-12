#===============================================================================
# Copyright (c) 2014, Leo Hendrawan
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution.
# 3. Neither the name of the Leo Hendrawan nor the
# names of its contributors may be used to endorse or promote products
# derived from this software without specific prior written permission.
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
# Name: Simple UDP Server
#
# Description: Simple UDP (echo) server for testing host script for CC3000
#              Basic WiFi module example. The script will setup a UDP server
#              on the PC at UDP_PORT and waiting for any incoming UDP message
#              data, and then reply with 'R'+data to the sender
#
# Author: Leo Hendrawan
#
# Version: 0.1.0
#
# Note:
#
# Log:
# - Version 0.1 (2014.04.09) :
# Hello World! (created)
#
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import socket
import sys

HOST_IP = '192.168.1.100'
UDP_PORT = 30000

def main():
    print "\r\n------------------------"
    print "Simple UDP Echo Server"
    print "------------------------\r\n"

    # create socket
    print "Creating Socket.......",
    try :
        s = socket.socket(socket.AF_INET, # Internet
                        socket.SOCK_DGRAM) # UDP
        print "done"
    except socket.error, msg :
        print 'ERROR - Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
        sys.exit()

    # binding socket
    print "Binding Socket to port", UDP_PORT, ".......",
    try:
        s.bind((HOST_IP, UDP_PORT))
        print "done"
    except socket.error, msg:
        print 'ERROR - Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
        sys.exit()

    print "Waiting for messages from clients"

    while True:
        rcv_data = s.recvfrom(1024) # buffer size is 1024 bytes
        addr = rcv_data[1]
        data = rcv_data[0]
        print "\r\nReceived message from:", addr, " - data:", data
        print "Sending echo message back to:", addr
        s.sendto("R"+data, addr)
    pass

if __name__ == '__main__':
    main()