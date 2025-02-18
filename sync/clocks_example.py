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

from multiprocessing import Process, Pipe
from clocks_exercise import LamportClock, VectorClock

use_vector_clocks = False


def create_clock(iproc, nproc):
    if use_vector_clocks:
        return VectorClock(iproc, nproc)
    else:
        return LamportClock()


def sendto(pipe, processfrom, processto, message, clock):
    clock.increment_internal()
    pipe.send((message, processfrom, processto, clock.get_internal_count()))
    print(f'[{processfrom}]: Sent message = \'{message}\' to {processto}, clock value = {clock.to_string()}')


def internal_event(process, message, clock):
    clock.increment_internal()
    print(f'[{process}]: Internal event happened = \'{message}\', clock value = {clock.to_string()}')


def receivefrom(pipe, process, clock):
    message, processfrom, processto, counter = pipe.recv()
    clock.increment_received(counter)
    print(f'[{process}]: Received message = \'{message}\' from {processfrom}, clock value = {clock.to_string()}')
    return message


def processA(pipeAB):
    print('Starting process A')
    clock = create_clock(0, 3)
    internal_event('A', 'Internal event', clock)
    sendto(pipeAB, 'A', 'B', 'Message 1', clock)
    internal_event('A', 'Internal event', clock)
    receivefrom(pipeAB, 'A', clock)
    internal_event('A', 'Internal event', clock)


def processB(pipeBA, pipeBC):
    print('Starting process B')
    clock = create_clock(1, 3)
    receivefrom(pipeBA, 'B', clock)
    sendto(pipeBA, 'B', 'A', 'Message 2', clock)
    sendto(pipeBC, 'B', 'C', 'Message 3', clock)
    receivefrom(pipeBC, 'B', clock)


def processC(pipeCB):
    print('Starting process C')
    clock = create_clock(2, 3)
    receivefrom(pipeCB, 'C', clock)
    sendto(pipeCB, 'C', 'B', 'Message 4', clock)


def create_and_run(use_vector_clocks=False):
    pipeAB, pipeBA = Pipe()
    pipeBC, pipeCB = Pipe()

    procA = Process(target=processA, args=(pipeAB,))
    procB = Process(target=processB, args=(pipeBA, pipeBC))
    procC = Process(target=processC, args=(pipeCB,))

    procA.start()
    procB.start()
    procC.start()

    procA.join()
    procB.join()
    procC.join()


if __name__ == '__main__':
    create_and_run()
