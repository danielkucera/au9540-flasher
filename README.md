This tool can be used for flashing AU9540 smart card reader firmware under linux

# Hardware

If your device came without flash (as mine), you can solder standard serial EEPROM 24C02 to your reader to be able to write serial to the device.
See pictures folder.

# Install

- sudo pip install pyscard
- edit /usr/lib/pcsc/drivers/ifd-ccid.bundle/Contents/Info.plist:

<pre>
    &lt;key&gt;ifdDriverOptions&lt;/key&gt;
    &lt;string&gt;0x0001&lt;/string&gt; 
</pre>

# Usage

- prepare bin using original firmware utility or use vnet001.bin in this git
- read flash: ./fw-tool.py
- write flash: ./fw-tool.py vnet001.bin
- write flash and change serial to vnet010: ./fw-tool.py vnet001.bin vnet010

# Links

- http://ludovicrousseau.blogspot.sk/2011/10/featureccidesccommand.html
- https://militarycac.com/iogear.htm
- http://h20564.www2.hp.com/hpsc/swd/public/detail?swItemId=ob_138524_1&swEnvOid=4158
- http://www.gme.sk/at24c02c-sshm-so8-atmel-reel-p943-083
- http://www.streamboard.tv/oscam/ticket/4466

