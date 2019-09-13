import unittest
import os
import time
import shutil

from os import environ
from configparser import ConfigParser
from pprint import pprint

from installed_clients.WorkspaceClient import Workspace as workspaceService
from MEGAHIT.MEGAHITImpl import MEGAHIT
from installed_clients.ReadsUtilsClient import ReadsUtils


class MegaHitTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        token = environ.get('KB_AUTH_TOKEN', None)
        cls.ctx = {'token': token}
        cls.token = token
        config_file = environ.get('KB_DEPLOYMENT_CONFIG', None)
        cls.cfg = {}
        config = ConfigParser()
        config.read(config_file)
        for nameval in config.items('MEGAHIT'):
            print(nameval[0] + '=' + nameval[1])
            cls.cfg[nameval[0]] = nameval[1]
        cls.wsURL = cls.cfg['workspace-url']
        cls.ws = workspaceService(cls.wsURL, token=token)
        cls.serviceImpl = MEGAHIT(cls.cfg)

        cls.shockURL = cls.cfg['shock-url']
        cls.handleURL = cls.cfg['handle-service-url']

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'wsName'):
            cls.ws.delete_workspace({'workspace': cls.wsName})
            print('Test workspace was deleted')

    def getWsClient(self):
        return self.__class__.ws

    def getWsName(self):
        if hasattr(self.__class__, 'wsName'):
            return self.__class__.wsName
        suffix = int(time.time() * 1000)
        wsName = "temp_test_MegaHit_" + str(suffix)
        self.ws.create_workspace({'workspace': wsName})
        self.__class__.wsName = wsName
        return wsName

    # call this method to get the WS object info of a Paired End Library (will
    # upload the example data if this is the first time the method is called during tests)
    def getPairedEndLibInfo(self):
        if hasattr(self.__class__, 'pairedEndLibInfo'):
            return self.__class__.pairedEndLibInfo
        # 1) upload files to shock
        shared_dir = "/kb/module/work/tmp"
        forward_data_file = 'data/small.forward.fq'
        forward_file = os.path.join(shared_dir, os.path.basename(forward_data_file))
        shutil.copy(forward_data_file, forward_file)
        reverse_data_file = 'data/small.reverse.fq'
        reverse_file = os.path.join(shared_dir, os.path.basename(reverse_data_file))
        shutil.copy(reverse_data_file, reverse_file)

        ru = ReadsUtils(os.environ['SDK_CALLBACK_URL'])
        paired_end_ref = ru.upload_reads({'fwd_file': forward_file, 'rev_file': reverse_file,
                                          'sequencing_tech': 'artificial reads',
                                          'interleaved': 0, 'wsname': self.getWsName(),
                                          'name': 'test.pe.reads'})['obj_ref']

        new_obj_info = self.ws.get_object_info_new({'objects': [{'ref': paired_end_ref}]})
        self.__class__.pairedEndLibInfo = new_obj_info[0]
        return new_obj_info[0]

    def getImpl(self):
        return self.__class__.serviceImpl

    def getContext(self):
        return self.__class__.ctx

    def test_run_megahit(self):

        # figure out where the test data lives
        pe_lib_info = self.getPairedEndLibInfo()
        pprint(pe_lib_info)

        # Object Info Contents
        # 0 - obj_id objid
        # 1 - obj_name name
        # 2 - type_string type
        # 3 - timestamp save_date
        # 4 - int version
        # 5 - username saved_by
        # 6 - ws_id wsid
        # 7 - ws_name workspace
        # 8 - string chsum
        # 9 - int size
        # 10 - usermeta meta

        # run megahit
        params = {
            'workspace_name': pe_lib_info[7],
            'read_library_ref': pe_lib_info[7] + '/' + pe_lib_info[1],
            'megahit_parameter_preset': 'meta-sensitive',
            'output_contigset_name': 'output.contigset',
            # 'min_count':2,
            # 'k_min':31,
            # 'k_max':51,
            # 'k_step':10,
            # 'k_list':[31,41],
            # 'min_contig_length':199
        }

        result = self.getImpl().run_megahit(self.getContext(), params)
        print('RESULT:')
        pprint(result)

        # check the output
        info_list = self.ws.get_object_info([{'ref': pe_lib_info[7] + '/output.contigset'}], 1)
        self.assertEqual(len(info_list), 1)
        contigset_info = info_list[0]
        self.assertEqual(contigset_info[1], 'output.contigset')
        self.assertEqual(contigset_info[2].split('-')[0], 'KBaseGenomeAnnotations.Assembly')

        # check the report. We assume that kb_quast and KBaseReport do what they're supposed to do
        rep = self.ws.get_objects2({'objects': [{'ref': result[0]['report_ref']}]})['data'][0]
        print('REPORT object:')
        pprint(rep)

        self.assertEqual(rep['info'][1].rsplit('_', 1)[0], 'kb_megahit_report')
        self.assertEqual(rep['info'][2].split('-', 1)[0], 'KBaseReport.Report')
        self.assertEqual(rep['info'][7].rsplit('_', 1)[0], 'temp_test_MegaHit')
        d = rep['data']
        self.assertEqual(d['direct_html_link_index'], 0)
        self.assertEqual(len(d['html_links']), 1)
        ht = d['html_links'][0]
        self.assertEqual(ht['URL'].split('/node')[0], self.shockURL)
        self.assertEqual(ht['handle'].split('_', 1)[0], 'KBH')
        self.assertEqual(ht['label'], 'QUAST report')
        self.assertEqual(ht['name'], 'report.html')

    def test_run_megahit_with_min_contig_length(self):
        # figure out where the test data lives
        pe_lib_info = self.getPairedEndLibInfo()

        # run megahit
        params = {
            'workspace_name': pe_lib_info[7],
            'read_library_ref': pe_lib_info[7] + '/' + pe_lib_info[1],
            'output_contigset_name': 'trimmed.output.contigset',
            'min_contig_length': 63000
        }

        result = self.getImpl().run_megahit(self.getContext(), params)
        print('RESULT:')
        pprint(result)

        # check the output
        info_list = self.ws.get_object_info([{'ref': pe_lib_info[7] + '/trimmed.output.contigset'}], 1)
        self.assertEqual(len(info_list), 1)
        contigset_info = info_list[0]
        self.assertEqual(contigset_info[1], 'trimmed.output.contigset')
        self.assertEqual(contigset_info[2].split('-')[0], 'KBaseGenomeAnnotations.Assembly')
        self.assertEqual(contigset_info[10]['Size'], '64794')

    @unittest.skip("Skipping OOM test")
    def test_run_megahit_oom_error(self):
        # force MEGAHIT to use waaaay less than enough memory to trigger the error

        pe_lib_info = self.getPairedEndLibInfo()
        # run megahit
        params = {
            'workspace_name': pe_lib_info[7],
            'read_library_ref': pe_lib_info[7] + '/' + pe_lib_info[1],
            'megahit_parameter_preset': 'meta-sensitive',
            'output_contigset_name': 'output.contigset',
            'max_mem_percent': 2
        }

        with self.assertRaises(RuntimeError) as e:
            self.getImpl().run_megahit(self.getContext(), params)

        err_str = str(e.exception)
        print("Successfully triggered OOM error!\n" + err_str)
        self.assertIn("Error running MEGAHIT, return code", err_str)
        self.assertIn("Additional Information", err_str)
        self.assertIn("please set -m parameter to at least", err_str)
