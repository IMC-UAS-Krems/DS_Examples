#!/usr/bin/env python
# Contributed by Markus Schüttengruber

from spyne.application import Application
from spyne.decorator import srpc
from spyne.protocol.soap import Soap11
from spyne.service import ServiceBase
from spyne.model.complex import Iterable
from spyne.model.primitive import Integer
from spyne.model.primitive import String
from spyne.server.wsgi import WsgiApplication


def fib(n):
    """
    Synchronous Fibonacci numbers: get the n-th Fibonacci number with a delay
    equal to the previous Fibonacci number.

    The Fibonacci numbers are 0, 1, 1, 2, 3, 5, 8, 13, 21,...

    :param n: The index of the Fibonacci number to calculate
    :return: The n-th Fibonacci number
    """
    if n == 0 or n == 1:
        return n

    a = 0
    b = 1
    c = 1
    for index in range(1, n):
        c = a + b
        a = b
        b = c
    return c


class HelloService(ServiceBase):
    """
    A simple Hello service that outputs 'Hello, <argument>'
    """

    @srpc(String, _returns=String)
    def say_hello(name):
        return "Hello, " + name + "!"

    @srpc(Integer, _returns=Integer)
    def calc_fib(n):
        return fib(n)


import logging

if __name__ == '__main__':
    from wsgiref.simple_server import make_server

    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger('spyne.protocol.xml').setLevel(logging.DEBUG)

    application = Application([HelloService], 'ds_examples.soap.hello',
                              in_protocol=Soap11(), out_protocol=Soap11())

    wsgi_app = WsgiApplication(application)

    server = make_server('0.0.0.0', 7789, wsgi_app)

    print("listening to http://127.0.0.1:7789")
    print("wsdl is at: http://localhost:7789/?wsdl")

    server.serve_forever()