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

import asyncio
from kademlia.network import Server
import sys
import logging
import aioconsole
import os

node = Server()


async def run(join_network=True, ip='0.0.0.0', port=7123, local_port=7123):
    """
    Starts a node. If join_network is True, it will try to join an existing network
    by contacting the node given as known_ip and known_port.
    If false, the node will initialize its own network.
    :param join_network: True to try to join an existing network
    :param ip: IP address of a known node of the network
    :param port: port number of a known node of the network
    :return:
    """
    # Create a node
    await node.listen(local_port)

    if join_network:
        await node.bootstrap([(ip, port)])


async def get_user_input():
    """
    Awaits user input
    :return:
    """
    pass # TO IMPLEMENT


async def main(join_network=True, ip='0.0.0.0', port=7123, local_port=7123):
    """
    Main function that gathers the result of user input and run coroutine
    :return:
    """
    try:
        await asyncio.gather(asyncio.create_task(get_user_input()),
                             asyncio.create_task(run(join_network, ip, port, local_port)))
    except asyncio.CancelledError:
        print('Quit')
        exit(0)


def print_usage():
    print('Usage: \np2pnode create (<local_port>) to initialize a network.')
    print('p2pnode join (<ip_of_known_node>) (<port_of_known_node>) (<local_port>) to join an existing network')
    print('\nPort numbers are optional and default to 7123 if not given')
    print('\nIf parameter <ip_of_known_node> not given, then the program uses the contents of the environment '
          'variable P2P_REMOTE_HOST')


def init_logging():
    log = logging.getLogger('kademlia')
    log.setLevel(logging.DEBUG)
    log.addHandler(logging.StreamHandler())


if __name__ == '__main__':
    init_logging()
    nargs = len(sys.argv)
    if nargs <= 1:
        print('Wrong number of arguments')
        print_usage()
    else:
        loop = asyncio.get_event_loop()
        command = sys.argv[1]
        nport = 7123
        if command == 'create':
            if nargs > 2:
                nport = int(sys.argv[2])
            loop.run_until_complete(main(join_network=False, port=nport))
        elif command == 'join':
            nlocal_port = 7123
            remote_ip = '127.0.0.1'
            if nargs > 2:
                remote_ip = sys.argv[2]
            if nargs > 3:
                nport = int(sys.argv[3])
            if nargs > 4:
                nlocal_port = int(sys.argv[4])
            print(f'Trying to join network via host {remote_ip} on port {nport}')
            loop.run_until_complete(main(join_network=True, port=nport, ip=remote_ip, local_port=nlocal_port))
        else:
            print('Wrong parameters')
            print_usage()

        try:
            loop.run_forever()
        except KeyboardInterrupt:
            print('\nQuitting...')
        finally:
            loop.close()
