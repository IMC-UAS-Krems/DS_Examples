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
from asyncio.exceptions import CancelledError
import aioconsole
import sys

context = zmq.asyncio.Context()
req_socket = context.socket(zmq.REQ)
sub_socket = context.socket(zmq.SUB)


def connect():
    """

    :return:
    """
    req_socket.connect("tcp://localhost:7600")
    sub_socket.connect("tcp://localhost:7601")


def subscribe(channel):
    """

    :param username:
    :return:
    """
    sub_socket.setsockopt_string(zmq.SUBSCRIBE, channel)


async def wait_for_sub_messages():
    while True:
        received_message = await sub_socket.recv_string()
        print(f'\nReceived message {received_message}')


async def shutdown():
    for task in asyncio.all_tasks():
        task.cancel()


async def message_input():
    while True:
        channel = await aioconsole.ainput("Which user do you want to send a message to? (empty = all users, q = quit) ")
        if channel == 'q':
            await shutdown()
            return
        if channel == '':
            channel = 'GENERAL'
        content = await aioconsole.ainput("Which message do you want to send? ")
        message = {'command': 'send_message', 'channel': channel, 'content': content}
        req_socket.send(pickle.dumps(message))
        response = await req_socket.recv_string()
        if response == 'ACK':
            print('Message sent')


async def logout(user):
    message = {'command': 'logout', 'user': user}
    req_socket.send(pickle.dumps(message))


async def login(user) -> bool:
    """
    Performs the login operation.
    :param user: The username to log in
    :return: True if successfull, False otherwise
    """
    message = {'command': 'login', 'user': user}
    req_socket.send(pickle.dumps(message))
    response = await req_socket.recv_string()
    if response == 'OK':
        return True
    return False


async def main(user):
    rc = await login(user)
    if not rc:
        print('Error: login not successful')
    else:
        try:
            await asyncio.gather(asyncio.create_task(message_input()),
                                 asyncio.create_task(wait_for_sub_messages()))
        except CancelledError:
            await logout(user)
            print(f'Exiting...')

if __name__ == "__main__":
    connect()
    subscribe('GENERAL')
    if len(sys.argv) > 1:
        username = sys.argv[1]
        subscribe(username)  # user name
        print("Client started")
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main(username))

    req_socket.close()
