
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

import aiohttp
from aiohttp.client_exceptions import ClientConnectionError, ServerConnectionError, InvalidUrlClientError, ClientError
import asyncio
import sys


def check_http_code(code):
    """
    Check if the given code is a valid HTTP return code
    :param code: the candidate http error code
    :return:
    """
    if code < 100 or code > 599:
        return False
    return True


async def send_get(url):
    """
    Send a get request to a given URL
    :param url: The URL to send the request to.
    :return:
    """
    timeout = aiohttp.ClientTimeout(total=10)
    try:
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(url) as response:
                if check_http_code(response.status) is False:
                    print("Status not valid ", response.status)
                    return
                print("Status:", response.status)
                for key in response.headers:
                    print("Header: ", key)
                    print("Value:", response.headers[key])

                html = await response.text()
                print("Body:", html[:150], "...")
    except ServerConnectionError as err:
        print("Server connection error: ", err)
    except ClientConnectionError as err:
        print("Client connection error: ", err)
    except InvalidUrlClientError as err:
        print("Invalid URL: ", err)
    except ClientError as err:
        print("Unspecified error: ", err)
    except asyncio.TimeoutError:
        print("Timeout error")


if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print('Not enough arguments')
        exit(1)
    
    url = sys.argv[1]
    loop = asyncio.get_event_loop()
    loop.run_until_complete(send_get(url))
