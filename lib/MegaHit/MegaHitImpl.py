#BEGIN_HEADER
import sys
import subprocess
from pprint import pprint

from biokbase.workspace.client import Workspace as workspaceService
#END_HEADER


class MegaHit:
    '''
    Module Name:
    MegaHit

    Module Description:
    A KBase module: MegaHit
This sample module contains one small method - count_contigs.
    '''

    ######## WARNING FOR GEVENT USERS #######
    # Since asynchronous IO can lead to methods - even the same method -
    # interrupting each other, you must be *very* careful when using global
    # state. A method could easily clobber the state set by another while
    # the latter method is running.
    #########################################
    #BEGIN_CLASS_HEADER
    workspaceURL = None
    MEGAHIT = '/kb/module/megahit/megahit'
    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
        self.workspaceURL = config['workspace-url']
        #END_CONSTRUCTOR
        pass

    def run_megahit(self, ctx, params):
        # ctx is the context object
        # return variables are: output
        #BEGIN run_megahit

        # do some basic checks
        objref = ''
        if 'workspace_name' not in params:
            raise ValueError('workspace_name parameter is required')
        if 'read_library_name' not in params:
            raise ValueError('read_library_name parameter is required')
        if 'output_contigset_name' not in params:
            raise ValueError('output_contigset_name parameter is required')

        # get the ws object, just to check that it is the correct type, etc.

        ws = workspaceService(self.workspaceURL, token=ctx['token'])
        objects = ws.get_objects([{'ref': params['workspace_name']+'/'+params['read_library_name']}])
        data = objects[0]['data']
        info = objects[0]['info']
        pprint(data)
        pprint(info)


        # construct the command

        # run megahit, capture output as it happens
        p = subprocess.Popen([self.MEGAHIT],
                    stdout = subprocess.PIPE, 
                    stderr = subprocess.STDOUT, shell = False)

        console_out = ''
        while True:
            line = p.stdout.readline()
            if not line: break
            print line.replace('\n', '')
            console_out += line + '\n'

        p.stdout.close()
        p.wait()

        output = {'console_out':console_out }

        #END run_megahit

        # At some point might do deeper type checking...
        if not isinstance(output, dict):
            raise ValueError('Method run_megahit return value ' +
                             'output is not type dict as required.')
        # return the results
        return [output]

    def count_contigs(self, ctx, workspace_name, contigset_id):
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN count_contigs
        token = ctx['token']
        wsClient = workspaceService(self.workspaceURL, token=token)
        contigSet = wsClient.get_objects([{'ref': workspace_name+'/'+contigset_id}])[0]['data']
        returnVal = {'contig_count': len(contigSet['contigs'])}
        #END count_contigs

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method count_contigs return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]
