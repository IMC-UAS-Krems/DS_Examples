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

import zmq
import zmq.asyncio
import pickle
import asyncio
import aioconsole
import sys

context = zmq.asyncio.Context()
req_socket = context.socket(zmq.REQ)
sub_socket = context.socket(zmq.SUB)


def connect():
    """
    Starts the connections.
    :return:
    """
    req_socket.connect("tcp://localhost:7600")
    sub_socket.connect("tcp://localhost:7601")


def subscribe(channel):
    """
    Subscribes to a given channel.
    :param username:
    :return:
    """
    sub_socket.setsockopt_string(zmq.SUBSCRIBE, channel)


async def message_input():
    """
    Performs user input processing.
    :return:
    """
    while True:
        channel = await aioconsole.ainput("Which user do you want to send a message to? (empty = all users, q = quit) ")
        if channel == 'q':
            break
        if channel == '':
            channel = 'GENERAL'
        content = await aioconsole.ainput("Which message do you want to send? ")
        message = {'channel': channel, 'content': content}
        await req_socket.send(pickle.dumps(message))
        received_message = await sub_socket.recv_string()
        print(f'\nReceived message {received_message}')


async def main():
    await message_input()

if __name__ == "__main__":
    connect()
    subscribe('GENERAL')
    if len(sys.argv) > 1:
        subscribe(sys.argv[1])  # user name
    print("Client started")
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

    req_socket.close()

