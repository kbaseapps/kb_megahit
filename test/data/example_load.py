

import sys
import os

import requests
from requests_toolbelt import MultipartEncoder

from pprint import pprint

from biokbase.AbstractHandle.Client import AbstractHandle as HandleService
from biokbase.workspace.client import Workspace


# Helper script borrowed from the transform service
def upload_file_to_shock(shock_service_url = None,
                         filePath = None,
                         ssl_verify = True,
                         token = None):
    """
    Use HTTP multi-part POST to save a file to a SHOCK instance.
    """

    if token is None:
        raise Exception("Authentication token required!")
    
    #build the header
    header = dict()
    header["Authorization"] = "Oauth {0}".format(token)

    if filePath is None:
        raise Exception("No file given for upload to SHOCK!")

    dataFile = open(os.path.abspath(filePath), 'rb')
    m = MultipartEncoder(fields={'upload': (os.path.split(filePath)[-1], dataFile)})
    header['Content-Type'] = m.content_type

    #logger.info("Sending {0} to {1}".format(filePath,shock_service_url))
    try:
        response = requests.post(shock_service_url + "/node", headers=header, data=m, allow_redirects=True, verify=ssl_verify)
        dataFile.close()
    except:
        dataFile.close()
        raise    

    if not response.ok:
        response.raise_for_status()

    result = response.json()

    if result['error']:            
        raise Exception(result['error'][0])
    else:
        return result["data"]    


HANDLE_URL='https://ci.kbase.us/services/handle_service'
SHOCK_URL='https://ci.kbase.us/services/shock-api'
WORKSPACE_URL='https://ci.kbase.us/services/ws'
token = 'TOKEN_HERE'


# 1) upload files to shock
forward_shock_file = upload_file_to_shock(
    shock_service_url = 'https://ci.kbase.us/services/shock-api',
    filePath = 'small.forward.fq',
    token = token
    )
reverse_shock_file = upload_file_to_shock(
    shock_service_url = 'https://ci.kbase.us/services/shock-api',
    filePath = 'small.reverse.fq',
    token = token
    )
pprint(forward_shock_file)
pprint(reverse_shock_file)


# 2) create handle
hs = HandleService(url=HANDLE_URL, token=token)
forward_handle = hs.persist_handle({
                                'id' : forward_shock_file['id'], 
                                'type' : 'shock',
                                'url' : SHOCK_URL,
                                'file_name': forward_shock_file['file']['name'],
                                'remote_md5': forward_shock_file['file']['checksum']['md5']})

reverse_handle = hs.persist_handle({
                                'id' : reverse_shock_file['id'], 
                                'type' : 'shock',
                                'url' : SHOCK_URL,
                                'file_name': reverse_shock_file['file']['name'],
                                'remote_md5': reverse_shock_file['file']['checksum']['md5']})
pprint(forward_handle)
pprint(reverse_handle)


# 3) save to WS
        # Warning: this reads everything into memory!  Will not work if 
        # the contigset is very large!

paired_end_library = {
    'lib1': {
        'file': {
            'hid':forward_handle,
            'file_name': forward_shock_file['file']['name'],
            'id': forward_shock_file['id'],
            'url': SHOCK_URL,
            'type':'shock',
            'remote_md5':forward_shock_file['file']['checksum']['md5']
        },
        'encoding':'UTF8',
        'type':'fastq',
        'size':forward_shock_file['file']['size']
    },
    'lib2': {
        'file': {
            'hid':reverse_handle,
            'file_name': reverse_shock_file['file']['name'],
            'id': reverse_shock_file['id'],
            'url': SHOCK_URL,
            'type':'shock',
            'remote_md5':reverse_shock_file['file']['checksum']['md5']
        },
        'encoding':'UTF8',
        'type':'fastq',
        'size':reverse_shock_file['file']['size']

    },
    'interleaved':0,
    'sequencing_tech':'artificial reads'
}

ws = Workspace(WORKSPACE_URL, token=token)
new_obj_info = ws.save_objects({
                'workspace':'msneddon:1448037540898',
                'objects':[
                    {
                        'type':'KBaseFile.PairedEndLibrary',
                        'data':paired_end_library,
                        'name':'test.reads',
                        'meta':{},
                        'provenance':[
                            {
                                'service':'MegaHit',
                                'method':'test_megahit'
                            }
                        ]
                    }]
                })
pprint(new_obj_info)

