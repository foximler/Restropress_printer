# Restropress_printer
A python script to automatically print Restropress online orders to Epson TM-U220 Network Kitchen Printers

The script pulls your smtp server inbox to find new messages. 
I'd reccomend setting a custom folder. Once it gets the order email it loads it in and get the receipt url to download the receipt from the restropress website.
It then checks to see if it is logged in and pulls the website while logging in if it has to. 
It then gets rid of everything a kitchen doesnt need to see and keeps everything the front of house printer needs and prints it off to the printer.
Just run it on a watchdog on repeat with some pc on the network. I use a raspberry pi. 
This system only runs when payment is recieved by paypal and it begins processing.
