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

import sys
import time
import asyncio
from codetiming import Timer


async def async_fib(n):
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

    await asyncio.sleep(c)
    print(c, end=",")
    return c


async def main(nfib):
    """
    This is the main function.
    Call it with any parameter you like.
    """
    with Timer(text="Total time = {:.1f}"):
        tasks = []
        for index in range(nfib):
            tasks.append(asyncio.create_task(async_fib(index)))

        await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main(int(sys.argv[1])))
