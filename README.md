# CO2-Monitor-Respirator

### This is a respirator setup that I made after some coments online that while sites like Etsy have very stylish 'cyberpunk' respirators, none are very functional. This is the first iteration, with future ones planned.

What you'll need to recreate this version and can give you a jumping off point if you want to create your own.

**WARNING** I am not a developer or designer, just some guy that threw a bunch of parts together and happened to have it all worked out, And since actually completing this project from inspiration to design to build am not going to have many excuses for my wife as to why I don't get more done around the house. Share and enjoy!

I created the code by splicing together a lot of other code around the Adafruit and Circuitpython websites and am still tinkering with it. Currently the smilies.bmp file is specific to the DEF CON security conference and will be updated in a future release (maybe, if I get around to it...)

1. A Dentec Comfort-Air NX respirator
2. Adafruit Feather Wing OLED 128x64
3. 2000mAh Lipo battery
4. STEMMA QT 4-pin cable
5. Adafruit SCD-30 NDIR CO2 Sensor
6. Adafruit Feather (The custom Circuitpython in this repo is made for the M4 Express, if you want to use another controller you'll need to re-compile your own per this discussion https://github.com/adafruit/circuitpython/issues/1760)
7. 2 NeoPixel 24 rings
8. A 2.0" 320x240 display
9. A Feather Wing proto board
10. Male, female, and stacking headers for the feather boards
11. The STLs in this repo printed, if you just want a badge that is also a CO2 monitor without a mask you can just print the allinonebadge stl and skip the Neopixels.
12. The custom version of circuitpython from this repo

Once you've gathered everything together, load the custom boot loader, code and bitmaps, make sure you grab the adafruit circuitpython libraries and put the apropriate ones on the controler. 

Solder the headers onto the controller protoboard and display board

Solder the neopixels to ground, battery out and a digital pin on the proto board and solder the display wires to the proto board. Load up the code and libraries and you should be good to go!

**A note about this, if you want to program the buttons to do things, use pins 9, 10, 11, & 12 for the TFT display and neopixels!**

If you want to make changes to the mounting plate, like add a logo or your social media handles you can access the original in TinkerCad, just dupicate it and modify to your heart's content https://www.tinkercad.com/things/aItuTWLHWLe-co2-monitor-respirator-mounting-plate
