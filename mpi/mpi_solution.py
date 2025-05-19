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

import json
from mpi4py import MPI

comm = MPI.COMM_WORLD
scatter_tasks = None
if comm.rank == 0:
    tasks = [
        json.dumps({'parameter1': 1, 'parameter2': 2, 'parameter3': 3, 'operation': 'ADD'}),
        json.dumps({'parameter1': 3, 'parameter2': 1, 'parameter3': 2, 'operation': 'SUB'}),
        json.dumps({'parameter1': 2, 'parameter2': 3, 'parameter3': 1, 'operation': 'POW'}),
        json.dumps({'parameter1': 4, 'parameter2': 2, 'parameter3': 3, 'operation': 'ADD'}),
        json.dumps({'parameter1': 1, 'parameter2': 2, 'parameter3': 3, 'operation': 'ADD'}),
        json.dumps({'parameter1': 3, 'parameter2': 1, 'parameter3': 2, 'operation': 'SUB'}),
        json.dumps({'parameter1': 2, 'parameter2': 3, 'parameter3': 1, 'operation': 'POW'}),
        json.dumps({'parameter1': 4, 'parameter2': 2, 'parameter3': 3, 'operation': 'ADD'})
    ]
    scatter_tasks = [None]*comm.size
    current_proc = 0
    for task in tasks:
        if scatter_tasks[current_proc] is None:
            scatter_tasks[current_proc] = []
        scatter_tasks[current_proc].append(task)
        current_proc = (current_proc + 1) % comm.size
else:
    tasks = None


# Scatter parameters arrays
units = comm.scatter(scatter_tasks, root=0)
calcs = []
if units is not None:
    for unit in units:
        p = json.loads(unit)
        print(f'[{comm.rank}]: parameters {p}')

        if p['operation'] == 'ADD':
            calc = p['parameter1'] + p['parameter2'] + p['parameter3']
        elif p['operation'] == 'SUB':
            calc = p['parameter1'] - p['parameter2'] - p['parameter3']
        elif p['operation'] == 'POW':
            calc = (p['parameter1'] + p['parameter2'])**p['parameter3']
        else:
            calc = 'UNKNOWN'

        calc = [calc, comm.rank]
        calcs.append(calc)


# gather results
result = comm.gather(calcs, root=0)

if comm.rank == 0:
    print("[root]: Results are ", result)
    