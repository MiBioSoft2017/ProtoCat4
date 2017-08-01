﻿# -*- coding: utf-8 -*-
import json
import requests

"""
    get the file from protocols.io, however that works?
"""
def load_protocols_io(message_id):
    pass

"""
    submit protocol to protocat's API in order to upload it
"""
def submit_to_protocat():
    pass

class convertor():
    def __init__(self):
        pass
    
    def convert_cat_to_io(self, cat_json):
        pass

    def convert_io_to_cat(self, io_json):
        #http://protocat.org/api/protocol/
        cat_json = {}
        if 'protocol_name' in io_json:
            cat_json['title'] = io_json['protocol_name']
        else:
            cat_json['title'] = "Untitled"

        if 'description' in io_json:
            cat_json['description'] = io_json['description']
        else:
            cat_json['description'] = "No Description provided"       
        cat_json['description'] += '<br/>Taken from https://www.protocols.io/view/' + io_json['uri']

        if 'materials' in io_json:
            cat_json['materials'] = "<br/>".join(io_json['materials'])
        else:
            cat_json['materials'] = "No Materials Provided"

        cat_json['protocol_steps'] = []
        step_number = 1
        if 'steps' in io_json:
            for step in io_json['steps']:
                cat_step = {}
                cat_step['step_number'] = step_number
                step_number += 1
                #print(step['components'],'\n####################')
                descr = ""
                for comp in step['components']:
                    if 'name' in comp and comp['name'] == "Description":
                        cat_step['action'] = comp['data']
                        descr = ""
                    elif 'name' in comp and comp['name'] == 'Duration / Timer':
                        cat_step['time'] = comp['data']
                        descr = ""
                    else:
                        try:
                            if step['components'][comp]['name'] == "Description":
                                descr += step['components'][comp]['data']
                            elif step['components'][comp]['name'] == "Protocol":
                                #print(step['components'][comp])
                                descr += " https://www.protocols.io/view/" + step['components'][comp]['source_data']['uri']
                            else:
                                raise Exception
                        except:
                            print("Unknown how to handle this",comp)
                            descr = "Error ocurred while parsing"
                        cat_step['action'] = descr
                if "title" not in cat_step:
                    cat_step['title'] = ""
                if "time" not in cat_step:
                    cat_step['time'] = None
                if "warning" not in cat_step:
                    cat_step['warning'] = ""
                if "time_scaling" not in cat_step:
                    cat_step['time_scaling'] = 2
                if "reagents" not in cat_step:
                    cat_step['reagents'] = []
                if "action" not in cat_step:
                    cat_step['action'] = ""
                if cat_step['action'][0:2] != "<p>":
                    cat_step['action'] = "<p>" + cat_step['action'] + "</p>"
                cat_json['protocol_steps'].append(cat_step)
            
        cat_json['category'] = None 
        cat_json['change-log'] = ""
        cat_json['previous_revision']: "-1"
        return cat_json

protocols_io_file_ = open("protocols_output.json", 'rb')

conv = convertor()
source = "http://localhost:8000"

protocat_auth_url = source + "/api/token"
auth_body = {}
r = requests.post(protocat_auth_url, data=auth_body)
print(r)

protocols_io_json = json.load(protocols_io_file_)
protocat_upload_url = source + "/api/protocol/"
headers = {}
if protocols_io_json:
    cat_json = conv.convert_io_to_cat(protocols_io_json)
    r = requests.post(protocat_upload_url, data=cat_json, headers=headers)
    print(r)