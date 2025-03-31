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
#

import grpc
import example_solution_pb2
import example_solution_pb2_grpc
from concurrent import futures
import logging


class CustomerService(example_solution_pb2_grpc.CustomerServiceServicer):
    customers = {}
    current_id = 1

    def AddCustomer(self, request, context):
        """
        Implementation of the AddCustomer service method. Adds a customer to the internal
        customers list. If there is no id, the next highest id will be assigned to the new customer.
        If there is a customer with the same id, the request will be rejected.
        :param request: the request to process.
        :param context: grpc context object
        :return: a CustomerServiceResponse object
        """
        if request.id == 0:
            request.id = self.current_id
            self.current_id += 1

        if request.id in self.customers:
            return example_solution_pb2.CustomerServiceResponse(success=False, error_message='Customer already present')

        self.customers[request.id] = {'purchased_amount': 0.0, 'customer': request}
        print(f'Added new customer with id = {request.id} and name {request.forename} {request.surname}')
        return example_solution_pb2.CustomerServiceResponse(success=True, error_message='', customers=[request])

    def SendPurchases(self, request_iterator, context):
        """
        Implementation of the SendPurchases service method. It reads one request from the stream at a time
        and attaches a purchase to an existing customer.
        :param request_iterator: stream of purchases
        :param context: grpc context object
        :return: a CustomerServiceResponse object
        """
        for request in request_iterator:
            if request.customer_id not in self.customers:
                pass
            customer = self.customers[request.customer_id]
            print(f'Added new purchase for customer {request.customer_id} with total value {request.total_price}')
            customer['purchased_amount'] = customer['purchased_amount'] + request.total_price
            yield example_solution_pb2.PurchaseResponse(success=True, error_message='', customer=customer['customer'])

    def GetCustomersWithMorePurchases(self, request, context):
        """
        Implementation of the GetCustomersWithMorePurchases method
        :param request: The request with the excess amount
        :param context: grpc context object
        :return: a stream of customers that satisfy the condition
        """
        for customer_id in self.customers:
            customer = self.customers[customer_id]
            if customer['purchased_amount'] >= request.amount:
                yield customer['customer']


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    example_solution_pb2_grpc.add_CustomerServiceServicer_to_server(CustomerService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
