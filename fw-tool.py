#! /usr/bin/env python

"""
#   FW updater for AU9540
#   Copyright (C) 2016 daniel.kucera@vnet.eu
"""

#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License along
#   with this program; if not, see <http://www.gnu.org/licenses/>.

from smartcard.System import readers
from smartcard.pcsc.PCSCPart10 import (SCARD_SHARE_DIRECT,
    SCARD_LEAVE_CARD, FEATURE_CCID_ESC_COMMAND, getFeatureRequest, hasFeature)

import numpy as np
np.set_printoptions(formatter={'int':hex})

import sys

def main():
    """ main """
    card_connection = readers()[0].createConnection()
    card_connection.connect(mode=SCARD_SHARE_DIRECT,
        disposition=SCARD_LEAVE_CARD)

    feature_list = getFeatureRequest(card_connection)

    ccid_esc_command = hasFeature(feature_list, FEATURE_CCID_ESC_COMMAND)
    if ccid_esc_command is None:
        raise Exception("The reader does not support FEATURE_CCID_ESC_COMMAND")

    status = [0x40, 0xc2, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]

    res = card_connection.control(ccid_esc_command, status)
    print np.array(res)
    print "STATUS OK"

    if len(sys.argv) > 1:
        f = open(sys.argv[1], 'r')
	#skip first 16 bytes
	f.read(16)

        for i in range(0,12):
            print i
            addr = i*16
    
            res = card_connection.control(ccid_esc_command, status)
            print np.array(res)
    
            wr_cmd = [ 0x40, 0xc2, addr, 0x00, 0x00, 0x03, 0x10, 0x00 ]

	    data_s = f.read(16)
            data = map(ord, data_s)
    
            wr_cmd.extend(data)
            print "to_write", np.array(wr_cmd)
    
            res = card_connection.control(ccid_esc_command, wr_cmd)
            print np.array(res)

	# write serial
        if len(sys.argv) == 3:
           serial = sys.argv[2]
	   addr = 0x5e 
           wr_cmd = [ 0x40, 0xc2, addr, 0x00, 0x00, 0x03, 2*len(serial), 0x00 ]
           data = [ ]
           for ch in serial:
               data.append(0)
               data.append(ord(ch))

           wr_cmd.extend(data)
           print "to_write", np.array(wr_cmd)
    
           res = card_connection.control(ccid_esc_command, wr_cmd)
           print np.array(res)
    
    else:

        for i in range(0,29):
    
            addr = i*8
            get_data = [0x40, 0xc3, addr, 0x00, 0x00, 0x00, 0x08, 0x00]
        
            res = card_connection.control(ccid_esc_command, get_data)
            print np.array(get_data)
            print np.array(res)
    

if __name__ == "__main__":
    main()

