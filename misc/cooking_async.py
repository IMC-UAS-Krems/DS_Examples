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

import sys
import asyncio
from codetiming import Timer


async def boil_water():
    """
    Boiling water takes 5 seconds.
    :return:
    """
    print("Boiling water", end="...")
    await asyncio.sleep(5)
    print("Done boiling water")


async def prepare_salad():
    """
    Preparing a good salad requires 10 seconds
    :return:
    """
    print("Preparing salad", end="...")
    await asyncio.sleep(10)
    print("Done preparing salad")


async def cook_spaghetti():
    """
    Spaghetti are done after 7 seconds in boiling water.
    :return:
    """
    print("Cooking spaghetti", end="...")
    await asyncio.sleep(7)
    print("Done cooking spaghetti")


async def cook_sauce():
    """
    Grandma's secret tomato sauce: 4 seconds
    :return:
    """
    print("Cooking tomato sauce", end="...")
    await asyncio.sleep(4)
    print("Done cooking sauce")


async def prepare_lunch():
    """
    Let's cook for lunch!
    :return:
    """
    with Timer(text="Total elapsed time {:.1f}"):
        await boil_water()
        await prepare_salad()
        await cook_spaghetti()
        await cook_sauce()
        
        print("Ready for lunch!")


if __name__ == "__main__":
    asyncio.run(prepare_lunch())