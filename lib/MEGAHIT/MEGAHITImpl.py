# -*- coding: utf-8 -*-
#BEGIN_HEADER
import os
import sys
import shutil
import hashlib
import subprocess
import requests
import re
import traceback
import uuid
from datetime import datetime
from pprint import pprint, pformat

import numpy as np
from Bio import SeqIO


from kb_read_library_to_file.kb_read_library_to_fileClient import kb_read_library_to_file
from AssemblyUtil.AssemblyUtilClient import AssemblyUtil
from KBaseReport.KBaseReportClient import KBaseReport

#END_HEADER


class MEGAHIT:
    '''
    Module Name:
    MEGAHIT

    Module Description:
    A KBase module to wrap the MEGAHIT package.
    '''

    ######## WARNING FOR GEVENT USERS #######
    # Since asynchronous IO can lead to methods - even the same method -
    # interrupting each other, you must be *very* careful when using global
    # state. A method could easily clobber the state set by another while
    # the latter method is running.
    #########################################
    VERSION = "2.0.0"
    GIT_URL = "git@github.com:msneddon/kb_megahit.git"
    GIT_COMMIT_HASH = "4f86bcb007e6163dbb91454c2fbd25b881d7cf07"
    
    #BEGIN_CLASS_HEADER
    MEGAHIT = '/kb/module/megahit/megahit'

    # target is a list for collecting log messages
    def log(self, target, message):
        # we should do something better here...
        if target is not None:
            target.append(message)
        print(message)
        sys.stdout.flush()



    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
        self.workspaceURL = config['workspace-url']
        self.scratch = os.path.abspath(config['scratch'])
        self.callbackURL = os.environ['SDK_CALLBACK_URL']

        pprint(config)

        # HACK!! for issue where megahit fails on mac running docker because of 
        # silent named pipe error in the volume mounted from mac
        self.mac_mode = False
        self.host_scratch = self.scratch
        if 'mac-test-mode' in config and config['mac-test-mode']=='1':
            print('WARNING! running in mac test mode')
            self.scratch = os.path.join('/kb','module','local_scratch')
            self.mac_mode = True
        # end hack
        if not os.path.exists(self.scratch):
            os.makedirs(self.scratch)
        #END_CONSTRUCTOR
        pass
    

    def run_megahit(self, ctx, params):
        """
        :param params: instance of type "MegaHitParams" (Run MEGAHIT.  Most
           parameters here are just passed forward to MEGAHIT workspace_name
           - the name of the workspace for input/output read_library_name -
           the name of the PE read library (SE library support in the future)
           output_contig_set_name - the name of the output contigset
           megahit_parameter_preset - override a group of parameters;
           possible values: meta            '--min-count 2 --k-list
           21,41,61,81,99' (generic metagenomes, default) meta-sensitive 
           '--min-count 2 --k-list 21,31,41,51,61,71,81,91,99' (more
           sensitive but slower) meta-large      '--min-count 2 --k-list
           27,37,47,57,67,77,87' (large & complex metagenomes, like soil)
           bulk            '--min-count 3 --k-list 31,51,71,91,99 --no-mercy'
           (experimental, standard bulk sequencing with >= 30x depth)
           single-cell     '--min-count 3 --k-list 21,33,55,77,99,121
           --merge_level 20,0.96' (experimental, single cell data) min_count
           - minimum multiplicity for filtering (k_min+1)-mers, default 2
           min_k - minimum kmer size (<= 127), must be odd number, default 21
           max_k - maximum kmer size (<= 127), must be odd number, default 99
           k_step - increment of kmer size of each iteration (<= 28), must be
           even number, default 10 k_list - list of kmer size (all must be
           odd, in the range 15-127, increment <= 28); override `--k-min',
           `--k-max' and `--k-step' min_contig_length - minimum length of
           contigs to output, default 200 @optional megahit_parameter_preset
           @optional min_count @optional k_min @optional k_max @optional
           k_step @optional k_list @optional min_contig_len) -> structure:
           parameter "workspace_name" of String, parameter
           "read_library_name" of String, parameter "output_contigset_name"
           of String, parameter "megahit_parameter_preset" of String,
           parameter "min_count" of Long, parameter "k_min" of Long,
           parameter "k_max" of Long, parameter "k_step" of Long, parameter
           "k_list" of list of Long, parameter "min_contig_len" of Long
        :returns: instance of type "MegaHitOutput" -> structure: parameter
           "report_name" of String, parameter "report_ref" of String
        """
        # ctx is the context object
        # return variables are: output
        #BEGIN run_megahit

        SERVICE_VER = 'dev'

        print('Running run_megahit with params=')
        pprint(params)

        # STEP 1: basic parameter checks + parsing
        objref = ''
        if 'workspace_name' not in params:
            raise ValueError('workspace_name parameter is required')
        if 'read_library_name' not in params:
            raise ValueError('read_library_name parameter is required')
        if 'output_contigset_name' not in params:
            raise ValueError('output_contigset_name parameter is required')

        # STEP 2: get the read library as deinterleaved fastq files
        input_ref = params['workspace_name']+'/'+params['read_library_name']
        reads_params =  {
                            'read_libraries': [ input_ref ],
                            'interleaved' : 'false',
                            'gzipped': None # megahit don't care, so don't do any conversion one way or the other
                        }
        readLibClient = kb_read_library_to_file(self.callbackURL, token=ctx['token'], service_ver=SERVICE_VER)
        reads = readLibClient.convert_read_library_to_file(reads_params)['files']

        print('Input reads files:')
        fwd = reads[input_ref]['files']['fwd']
        rev = reads[input_ref]['files']['rev']
        pprint('forward: '+fwd)
        pprint('reverse: '+rev)

        # STEP 3: run megahit
        # construct the command
        megahit_cmd = [self.MEGAHIT]

        # we only support PE reads, so add that
        megahit_cmd.append('-1')
        megahit_cmd.append(fwd)
        megahit_cmd.append('-2')
        megahit_cmd.append(rev)

        # if a preset is defined, use that:
        if 'megahit_parameter_preset' in params:
            if params['megahit_parameter_preset']:
                megahit_cmd.append('--presets')
                megahit_cmd.append(params['megahit_parameter_preset'])

        if 'min_count' in params:
            if params['min_count']:
                megahit_cmd.append('--min-count')
                megahit_cmd.append(str(params['min_count']))
        if 'k_min' in params:
            if params['k_min']:
                megahit_cmd.append('--k-min')
                megahit_cmd.append(str(params['k_min']))
        if 'k_max' in params:
            if params['k_max']:
                megahit_cmd.append('--k-max')
                megahit_cmd.append(str(params['k_max']))
        if 'k_step' in params:
            if params['k_step']:
                megahit_cmd.append('--k-step')
                megahit_cmd.append(str(params['k_step']))
        if 'k_list' in params:
            if params['k_list']:
                k_list = []
                for k_val in params['k_list']:
                    k_list.append(str(k_val))
                megahit_cmd.append('--k-list')
                megahit_cmd.append(','.join(k_list))
        if 'min_contig_len' in params:
            if params['min_contig_len']:
                megahit_cmd.append('--min-contig-len')
                megahit_cmd.append(str(params['min_contig_len']))

        # set the output location
        timestamp = int((datetime.utcnow() - datetime.utcfromtimestamp(0)).total_seconds()*1000)
        output_dir = os.path.join(self.scratch,'output.'+str(timestamp))
        megahit_cmd.append('-o')
        megahit_cmd.append(output_dir)

        # run megahit
        print('running megahit:')
        print('    '+' '.join(megahit_cmd))
        p = subprocess.Popen(megahit_cmd, cwd=self.scratch, shell=False)
        retcode = p.wait()

        print('Return code: ' + str(retcode))
        if p.returncode != 0:
            raise ValueError('Error running MEGAHIT, return code: ' +
                             str(retcode) + '\n')

        output_contigs = os.path.join(output_dir, 'final.contigs.fa')
        if self.mac_mode: # on macs, we cannot run megahit in the shared host scratch space, so we need to move the file there
            shutil.move(output_contigs, os.path.join(self.host_scratch, 'final.contigs.fa'))
            output_contigs = os.path.join(self.host_scratch, 'final.contigs.fa')

        # STEP 4: save the resulting assembly
        assemblyUtil = AssemblyUtil(self.callbackURL, token=ctx['token'], service_ver=SERVICE_VER)
        output_data_ref = assemblyUtil.save_assembly_from_fasta(
                                { 
                                    'file':{'path':output_contigs},
                                    'workspace_name':params['workspace_name'],
                                    'assembly_name':params['output_contigset_name']
                                })


        # STEP 5: generate and save the report

        # compute a simple contig length distribution for the report
        lengths = []
        for seq_record in SeqIO.parse(output_contigs, 'fasta'):
            lengths.append(len(seq_record.seq))

        report = ''
        report += 'ContigSet saved to: '+params['workspace_name']+'/'+params['output_contigset_name']+'\n'
        report += 'Assembled into '+str(len(lengths)) + ' contigs.\n'
        report += 'Avg Length: '+str(sum(lengths)/float(len(lengths))) + ' bp.\n'

        bins = 10
        counts, edges = np.histogram(lengths, bins)
        report += 'Contig Length Distribution (# of contigs -- min to max basepairs):\n'
        for c in range(bins):
            report += '   '+str(counts[c]) + '\t--\t' + str(edges[c]) + ' to ' + str(edges[c+1]) + ' bp\n'

        reportObj = {
            'objects_created':[{'ref':output_data_ref, 'description':'Assembled contigs'}],
            'text_message':report
        }
        report = KBaseReport(self.callbackURL, token=ctx['token'], service_ver=SERVICE_VER)
        report_info = report.create({'report':reportObj, 'workspace_name':params['workspace_name']})

        # STEP 6: contruct the output to send back
        output = { 'report_name': report_info['name'], 'report_ref': report_info['ref'] }

        #END run_megahit

        # At some point might do deeper type checking...
        if not isinstance(output, dict):
            raise ValueError('Method run_megahit return value ' +
                             'output is not type dict as required.')
        # return the results
        return [output]

    def status(self, ctx):
        #BEGIN_STATUS
        returnVal = {'state': "OK", 'message': "", 'version': self.VERSION, 
                     'git_url': self.GIT_URL, 'git_commit_hash': self.GIT_COMMIT_HASH}
        #END_STATUS
        return [returnVal]
