# -*- coding: utf-8 -*-
#BEGIN_HEADER
import os
import shutil
import subprocess
from datetime import datetime
from pprint import pprint
import uuid
import multiprocessing

import numpy as np
from Bio import SeqIO

from installed_clients.ReadsUtilsClient import ReadsUtils
from installed_clients.AssemblyUtilClient import AssemblyUtil
from installed_clients.KBaseReportClient import KBaseReport
from installed_clients.baseclient import ServerError
from installed_clients.kb_quastClient import kb_quast

from .error import report_megahit_error

DEFAULT_MIN_CONTIG_LENGTH = 2000
MINIMUM_MIN_CONTIG_LENGTH = 50  # Per KBase SME consensus on Slack

#END_HEADER


class MEGAHIT:
    '''
    Module Name:
    MEGAHIT

    Module Description:
    A KBase module to wrap the MEGAHIT package.
    '''

    ######## WARNING FOR GEVENT USERS ####### noqa
    # Since asynchronous IO can lead to methods - even the same method -
    # interrupting each other, you must be *very* careful when using global
    # state. A method could easily clobber the state set by another while
    # the latter method is running.
    ######################################### noqa
    VERSION = "2.4.2"
    GIT_URL = "https://github.com/kbaseapps/kb_megahit"
    GIT_COMMIT_HASH = "dfbd3ad0467892b2b998796a02d4259fe7cc742f"

    #BEGIN_CLASS_HEADER
    MEGAHIT = '/usr/bin/megahit'
    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
        self.workspaceURL = config['workspace-url']
        self.scratch = os.path.abspath(config['scratch'])
        self.callbackURL = os.environ['SDK_CALLBACK_URL']

        # HACK!! for issue where megahit fails on mac running docker because of
        # silent named pipe error in the volume mounted from mac
        self.mac_mode = False
        self.host_scratch = self.scratch
        if 'mac-test-mode' in config and config['mac-test-mode'] == '1':
            print('WARNING! running in mac test mode')
            self.scratch = os.path.join('/kb', 'module', 'local_scratch')
            self.mac_mode = True
        # end hack
        if not os.path.exists(self.scratch):
            os.makedirs(self.scratch)
        #END_CONSTRUCTOR
        pass


    def run_megahit(self, ctx, params):
        """
        :param params: instance of type "MegaHitParams" (Run MEGAHIT. Most
           parameters here are just passed forward to MEGAHIT workspace_name
           - the name of the workspace for input/output read_library_ref -
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
           k_min - minimum kmer size (<= 255), must be odd number, defaults
           to 21 k_max - maximum kmer size (<= 255), must be odd number,
           defaults to 141 k_step - increment of kmer size of each iteration
           (<= 28), must be even number, defaults to 10 k_list - list of kmer
           sizes (all must be odd, in the range 15-255, increment <= 28);
           override using `--k-min', `--k-max' and `--k-step'
           min_contig_length - minimum length of contigs to output, default
           is 2000 max_mem_percent - maximum memory to make available to
           MEGAHIT, as a percentage of available system memory (optional,
           default = 0.9 or 90%) @optional megahit_parameter_preset @optional
           min_count @optional k_min @optional k_max @optional k_step
           @optional k_list @optional min_contig_length @optional
           max_mem_percent) -> structure: parameter "workspace_name" of
           String, parameter "read_library_ref" of String, parameter
           "output_contigset_name" of String, parameter
           "megahit_parameter_preset" of String, parameter "min_count" of
           Long, parameter "k_min" of Long, parameter "k_max" of Long,
           parameter "k_step" of Long, parameter "k_list" of list of Long,
           parameter "min_contig_length" of Long, parameter "max_mem_percent"
           of Double
        :returns: instance of type "MegaHitOutput" -> structure: parameter
           "report_name" of String, parameter "report_ref" of String
        """
        # ctx is the context object
        # return variables are: output
        #BEGIN run_megahit
        print('Running run_megahit with params=')
        pprint(params)

        # STEP 1: basic parameter checks + parsing
        if 'workspace_name' not in params:
            raise ValueError('workspace_name parameter is required')
        if 'read_library_ref' not in params:
            raise ValueError('read_library_ref parameter is required')
        if 'output_contigset_name' not in params:
            raise ValueError('output_contigset_name parameter is required')

        min_contig_length = DEFAULT_MIN_CONTIG_LENGTH
        if params.get('min_contig_length') is not None:
            try:
                min_contig_length = int(params['min_contig_length'])
            except ValueError:
                raise ValueError('min_contig_length parameter must be an integer >= '
                                 + str(MINIMUM_MIN_CONTIG_LENGTH))
            if min_contig_length < MINIMUM_MIN_CONTIG_LENGTH:
                raise ValueError('min_contig_length parameter must be an integer >= '
                                 + str(MINIMUM_MIN_CONTIG_LENGTH))

        # STEP 2: get the read library as deinterleaved fastq files
        input_ref = params['read_library_ref']
        reads_params = {'read_libraries': [input_ref],
                        'interleaved': 'false',
                        'gzipped': None
                        }
        ru = ReadsUtils(self.callbackURL)
        reads = ru.download_reads(reads_params)['files']

        print('Input reads files:')
        fwd = reads[input_ref]['files']['fwd']
        rev = reads[input_ref]['files']['rev']
        pprint('forward: ' + fwd)
        pprint('reverse: ' + rev)

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

        megahit_cmd.append('--min-contig-len')
        megahit_cmd.append(str(min_contig_length))

        # Set the number of CPUs to the number of cores minus 1
        megahit_cmd.append('--num-cpu-threads')
        megahit_cmd.append(str(max([(multiprocessing.cpu_count() - 1), 1])))

        # set mem usage
        # Note: this just sets the default value - 90% of available system memory allocated
        # to the container. Exposing it here as a place to later expose as a parameter.
        max_mem_percent = params.get('max_mem_percent', 0.9)
        megahit_cmd.append('-m')
        megahit_cmd.append(str(max_mem_percent))

        # set the output location
        timestamp = int((datetime.utcnow() - datetime.utcfromtimestamp(0)).total_seconds() * 1000)
        output_dir = os.path.join(self.scratch, 'output.' + str(timestamp))
        megahit_cmd.append('-o')
        megahit_cmd.append(output_dir)

        # run megahit
        print('running megahit:')
        print('    ' + ' '.join(megahit_cmd))
        p = subprocess.Popen(megahit_cmd, cwd=self.scratch, shell=False)
        retcode = p.wait()

        print('Return code: ' + str(retcode))
        if p.returncode != 0:
            error_str = report_megahit_error(output_dir, retcode)
            raise RuntimeError(error_str)

        output_contigs = os.path.join(output_dir, 'final.contigs.fa')

        # on macs, we cannot run megahit in the shared host scratch space, so we need to move the file there
        if self.mac_mode:
            shutil.move(output_contigs, os.path.join(self.host_scratch, 'final.contigs.fa'))
            output_contigs = os.path.join(self.host_scratch, 'final.contigs.fa')

        # STEP 4: save the resulting assembly
        assemblyUtil = AssemblyUtil(self.callbackURL)
        output_data_ref = assemblyUtil.save_assembly_from_fasta({
                                                                'file': {'path': output_contigs},
                                                                'workspace_name': params['workspace_name'],
                                                                'assembly_name': params['output_contigset_name']
                                                                })


        # STEP 5: generate and save the report

        # compute a simple contig length distribution for the report
        lengths = []
        for seq_record in SeqIO.parse(output_contigs, 'fasta'):
            lengths.append(len(seq_record.seq))

        report = ''
        report += 'ContigSet saved to: ' + params['workspace_name'] + '/' + params['output_contigset_name'] + '\n'
        report += 'Assembled into ' + str(len(lengths)) + ' contigs.\n'
        report += 'Avg Length: ' + str(sum(lengths) / float(len(lengths))) + ' bp.\n'

        bins = 10
        counts, edges = np.histogram(lengths, bins)
        report += 'Contig Length Distribution (# of contigs -- min to max basepairs):\n'
        for c in range(bins):
            report += '   ' + str(counts[c]) + '\t--\t' + str(edges[c]) + ' to ' + str(edges[c + 1]) + ' bp\n'

        print('Running QUAST')
        kbq = kb_quast(self.callbackURL)
        try:
            quastret = kbq.run_QUAST({'files': [{'path': output_contigs,
                                                 'label': params['output_contigset_name']}],
                                      'min_contig_length': min_contig_length})
        except ServerError as qe:
            # not really any way to test this, all inputs have been checked earlier and should be
            # ok
            print('Logging exception from running QUAST')
            print(str(qe))
            # TODO delete shock node
            raise

        print('Saving report')
        kbr = KBaseReport(self.callbackURL)
        try:
            report_info = kbr.create_extended_report(
                {'message': report,
                 'objects_created': [{'ref': output_data_ref, 'description': 'Assembled contigs'}],
                 'direct_html_link_index': 0,
                 'html_links': [{'shock_id': quastret['shock_id'],
                                 'name': 'report.html',
                                 'label': 'QUAST report'}
                                ],
                 'report_object_name': 'kb_megahit_report_' + str(uuid.uuid4()),
                 'workspace_name': params['workspace_name']
                 })
        except ServerError as re:
            # not really any way to test this, all inputs have been checked earlier and should be
            # ok
            print('Logging exception from creating report object')
            print(str(re))
            # TODO delete shock node
            raise

        # STEP 6: contruct the output to send back
        output = {'report_name': report_info['name'], 'report_ref': report_info['ref']}

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
