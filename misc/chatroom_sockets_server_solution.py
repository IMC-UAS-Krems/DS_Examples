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

import pickle
import zmq
from zmq.error import ZMQError

context = zmq.Context()
rep_socket = context.socket(zmq.REP)  # create response socket
pub_socket = context.socket(zmq.PUB)  # create a publish socket

logged_users = {} # dictionary for storeing logged-in status for connected users


def bind():
    """
    Binds sockets to ports.
    :return:
    """
    rep_socket.bind("tcp://*:7600")
    pub_socket.bind("tcp://*:7601")


def dispatch_login(message):
    if 'user' in message:
        status = False
        user = message['user']
        if user in logged_users:
            status = logged_users[user]
        if status:
            rep_socket.send_string("ERR")
        else:
            rep_socket.send_string("OK")
            logged_users[message['user']] = True


def dispatch_logout(message):
    if 'user' in message and logged_users[message['user']]:
        logged_users.pop(message['user'])
    rep_socket.send_string("ACK")


def dispatch_send_message(message):
    channel = message['channel']
    content = message['content']
    rep_socket.send_string("ACK")
    print(f'Sending message = {content} to channel {channel}')
    pub_socket.send_string(f'{channel} {content}')


def wait_for_requests():
    """
    Waits for client requests to come and processes them.
    :return:
    """
    while True:
        try:
            message = pickle.loads(rep_socket.recv())
            print("Received message: %s" % message)
            if 'command' in message:
                if message['command'] == 'login':
                    dispatch_login(message)
                elif message['command'] == 'logout':
                    dispatch_logout(message)
                elif message['command'] == 'send_message':
                    dispatch_send_message(message)
        except ZMQError as err:
            print(f"Exception: {err}")


if __name__ == "__main__":
    bind()
    print("Server started")
    wait_for_requests()
