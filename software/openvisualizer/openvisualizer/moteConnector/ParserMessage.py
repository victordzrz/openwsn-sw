# Copyright (c) 2010-2013, Regents of the University of California.
# All rights reserved.
#
# Released under the BSD 3-Clause license as published at the link below.
# https://openwsn.atlassian.net/wiki/display/OW/License
import logging
import sys
import time
log = logging.getLogger('ParserData')
log.setLevel(logging.DEBUG)
log.addHandler(logging.NullHandler())
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
log.addHandler(ch)

import struct

from pydispatch import dispatcher

from ParserException import ParserException
import Parser

class ParserMessage(Parser.Parser):


    def __init__(self):

        # log
        log.info("create instance")

        # initialize parent class
        Parser.Parser.__init__(self,0)

        self._asn= ['asn_4',                     # B
          'asn_2_3',                   # H
          'asn_0_1',                   # H
         ]


    #======================== public ==========================================

    def parseInput(self,input):
        # log
        if log.isEnabledFor(logging.DEBUG):
            log.debug("received data {0}".format(input))
        moteId=input[:2]
        asn=input[2:7]
        message=input[7:]
        parsingHex=False
        sMessage=''
        for c in message:
            if c==ord('%'):
                parsingHex=not parsingHex
                if parsingHex:
                    sMessage=sMessage+"0x"
            else:
                if parsingHex:
                    sMessage=sMessage+format(c,'02x')+' '
                else:
                    sMessage=sMessage+chr(c)
        #sMessage=''.join([chr(c) for c in message])
        sId=''.join([format(c,'x') for c in moteId[::-1]])
        sAsn=''.join([format(c,'x') for c in asn[::-1]])
        print time.strftime('%H:%M:%S'),"MESSAGE",sId,"[",sAsn,"]:",sMessage

        eventType='message'
        source=[0,0,0,0,0,0,0,0]
        return (eventType,(source,input))
