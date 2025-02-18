#!/usr/bin/env python
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

import unittest
import zmq
import pickle
from concurrent.futures import ThreadPoolExecutor
import time


class MyRpcTests(unittest.TestCase):
    context = zmq.Context()

    def sendMessage(self, rpc):
        """
        Convenience method for sending a message via socket
        :return:
        """
        self.socket.send(pickle.dumps(rpc))
        response = pickle.loads(self.socket.recv())
        return response

    def setUp(self) -> None:
        """
        Setup test cases
        :return:
        """
        self.socket = self.context.socket(zmq.REQ)
        self.socket.connect("tcp://localhost:7600")

    def tearDown(self) -> None:
        """
        Closes the socket connection
        :return:
        """
        self.socket.close()

    def test_general(self):
        rpc_call = {''}
        response = self.sendMessage(rpc_call)
        self.assertEqual(response['error'], 'Error: No procedure name given')

        rpc_call = {'procedure': 'xy'}
        response = self.sendMessage(rpc_call)
        self.assertEqual(response['error'], 'Error: Unknown method: \'xy\'')

    def test_divide(self):
        rpc_call = {'procedure': 'divide', 'numerator': 1, 'denominator': 2}
        response = self.sendMessage(rpc_call)
        self.assertEqual(response['result'], 0.5)

        rpc_call = {'procedure': 'divide', 'numerator': 14, 'denominator': 2}
        response = self.sendMessage(rpc_call)
        self.assertEqual(response['result'], 7)

        rpc_call = {'procedure': 'divide', 'numerator': 1, 'denominator': 0}
        response = self.sendMessage(rpc_call)
        self.assertEqual(response['error'], 'Error: Division by Zero')

        rpc_call = {'procedure': 'divide', 'numerator': 1}
        response = self.sendMessage(rpc_call)
        self.assertEqual(response['error'], 'Error: Missing parameters: \'denominator\'')

        rpc_call = {'procedure': 'divide', 'denominator': 1}
        response = self.sendMessage(rpc_call)
        self.assertEqual(response['error'], 'Error: Missing parameters: \'numerator\'')

        rpc_call = {'procedure': 'divide'}
        response = self.sendMessage(rpc_call)
        self.assertEqual(response['error'], 'Error: Missing parameters: \'numerator\', \'denominator\'')

    def send_one_request(self, numerator):
        rpc_call = {'procedure': 'divide', 'numerator': numerator, 'denominator': 2}
        req_socket = self.context.socket(zmq.REQ)
        req_socket.connect("tcp://localhost:7600")
        req_socket.send(pickle.dumps(rpc_call))
        response = pickle.loads(req_socket.recv())
        req_socket.close()

    def test_load(self):
        t_0 = time.perf_counter()
        with ThreadPoolExecutor(max_workers=15) as executor:
            executor.map(self.send_one_request, range(1000))
        t_f = time.perf_counter()
        elapsed_time = t_f - t_0
        print(f'Total elapsed time: {t_f-t_0:0.4f} seconds')
        self.assertEqual(True, elapsed_time < 1)


if __name__ == '__main__':
    unittest.main()
