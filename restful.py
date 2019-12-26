#!/usr/bin/env python

# -*- coding: utf-8 -*-
# Author: Stevens Cadet <stevens@techtions.com>.
# Created on Tue Dec 24 09:10:49 2019

"""Command Line Python REST Client

Python client which is able to GET and POST data from/to an API gateway
-Note: File needs execution permission -> chmod +x restful.py

"""

import sys as _sys
import requests as _requests
import argparse as _argparse

gateway_address = 'https://jsonplaceholder.typicode.com'

class PyRestClient:
    def __init__(self, gateway_address):
        self.gateway_address = gateway_address
        
    def sendRequest(self, method, endpoint, request_data=None, output=None):
        #send request
        path = gateway_address + str(endpoint)
        
        if method == 'get':
            r = _requests.get(path)
        elif method == 'post':
            r = _requests.post(path, data = request_data)
            
        #Process response
        print ("Status Code: "+ str(r.status_code) +"\n")
        if str(r.status_code)[0] == '2':
            #success
            try:
                response_data = r.json()
            except ValueError as e:
                print ("response contains invalid JSON\n")
                print (e)
            except:
                print ("unexpected error while trying to save response data\n")
                print (_sys.exc_info()[0])
            
            #output
            if response_data:
                filename = output.name
                if filename[-4:] == '.csv':
                    response_data = self.jsonToCsv(response_data)
                    
                output.write(str(response_data))
                output.close()
            return
        
        else:
            print ("Request Failed. Check your arguments and try again!\nrun with --help for usage")
            _sys.exit(-1)
            
    def jsonToCsv(self,json_data):
        #header row reference
        if type(json_data) == list:
            headers_data = json_data[0]
            standardize_data = json_data
        elif type(json_data) == dict:
            headers_data = json_data
            standardize_data[0] = json_data
            
        if standardize_data:
            #header keys
            header_keys = []
            header_names = []
            for column_name in headers_data:
                header_keys.append(column_name)
                header_names.append('"'+ column_name +'"')
                
            #data rows
            rows = ''
            separator = ','
            for data in standardize_data:
                columns = []
                for header_key in header_keys:
                    try:
                        column_value = str(data[header_key])
                        columns.append('"'+ column_value.replace('"','').replace("\n",'') +'"')
                    except:
                        columns.append('"[DecodeError]"')
                #new row
                rows += separator.join(columns)
                rows += "\n"
                
            #header row
            header_row = separator.join(header_names);
            
            return header_row +"\n"+ rows

client = PyRestClient(gateway_address);

#Get arguments
parser = _argparse.ArgumentParser(description='Python REST client able to GET and POST to/from API.')
parser.add_argument('METHOD', choices=['get','post'], help='Request method')
parser.add_argument('ENDPOINT', metavar='endpoint', help='Request endpoint URI fragment')
parser.add_argument('-d', '--data', help='Data to send with request')
parser.add_argument('-o', '--output', nargs='?', type=_argparse.FileType('w'), default=_sys.stdout, help='Output to .json or .csv file (default: dump to stdout)')
user_arguments = vars(parser.parse_args());

if "METHOD" in user_arguments and "ENDPOINT" in user_arguments:
    client.sendRequest(user_arguments["METHOD"], user_arguments["ENDPOINT"], user_arguments["data"], user_arguments["output"])
else:
    parser.print_help()