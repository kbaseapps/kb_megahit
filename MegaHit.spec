/*
A KBase module: MegaHit
This sample module contains one small method - count_contigs.
*/

module MegaHit {


	typedef structure {
		string workspace_name;
		string read_library_name;
		string megahit_parameter_preset;

		string output_contigset_name;
	} MegaHitParams;


	typedef structure {
		list<string> console_out;
		list<string> report;
	} MegaHitOutput;

	funcdef run_megahit(MegaHitParams params) returns (MegaHitOutput output)
		authentication required;

};