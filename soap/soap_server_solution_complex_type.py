#!/usr/bin/env python
# !/usr/bin/env python
# encoding: utf8
#
# Copyright © Ruben Ruiz Torrubiano <ruben.ruiz at fh-krems dot ac dot at>,
#
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#    1. Redistributions of source code must retain the above copyright notice,
#       this list of conditions and the following disclaimer.
#    2. Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#    3. Neither the name of the owner nor the names of its contributors may be
#       used to endorse or promote products derived from this software without
#       specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER BE LIABLE FOR ANY DIRECT,
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY
# OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
# EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


from spyne.application import Application
from spyne.decorator import srpc
from spyne.protocol.soap import Soap11
from spyne.service import ServiceBase
from spyne.model.complex import ComplexModel
from spyne.model.primitive import Integer
from spyne.model.primitive import String
from spyne.model.primitive import Unicode
from spyne.model.primitive import Boolean
from spyne.server.wsgi import WsgiApplication
import logging


class Person(ComplexModel):
    forename = Unicode
    surname = Unicode
    ssn = Integer


class HelloService(ServiceBase):
    """
    A simple Hello service that outputs 'Hello, <argument>'
    """

    @srpc(String, _returns=String)
    def say_hello(name):
        return "Hello, " + name + "!"

    @srpc(Person, _returns=Boolean)
    def calculate_ssn_parity(person):
        if person.ssn % 2 == 0:
            return True
        return False


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
