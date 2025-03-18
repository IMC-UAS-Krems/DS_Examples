#!/usr/bin/env python
# Contributed by Markus Schüttengruber

from sys import argv
from urllib.error import URLError

from suds.client import Client, WebFault

name_to_echo = "Hello"
n = 0
if __name__ == "__main__":
    if len(argv) < 3:
        print("Not enough arguments! Usage example_client <name to echo> <fib to calculate>")
        exit(1)
    else:
        name_to_echo = argv[1]
        n = int(argv[2])
else:
    name_to_echo = "Dude"

import logging

logging.basicConfig(level=logging.INFO, filename="../log/suds.log")
logging.getLogger('suds.client').setLevel(logging.DEBUG)
logging.getLogger('suds.transport').setLevel(logging.DEBUG)

try:
    hello_client = Client('http://localhost:7789/?wsdl')
    print(hello_client.service.say_hello(name_to_echo))
    print(f'The {n}. fibonacci is: {hello_client.service.calc_fib(n)}!')

except (URLError, WebFault):
    print("""\
            Ooops! Something went wrong!
            Please make sure to start the server first
        """)