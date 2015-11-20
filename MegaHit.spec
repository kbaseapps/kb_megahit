/*
A KBase module: MegaHit
This sample module contains one small method - count_contigs.
*/

module MegaHit {

	/*
		@optional megahit_parameter_preset
		@optional min_count
		@optional k_min
		@optional k_max
		@optional k_step
		@optional k_list
		@optional min_contig_length
	*/
	typedef structure {
		string workspace_name;
		string read_library_name;
		string output_contigset_name;

		string megahit_parameter_preset;

		int min_count;
		int k_min;
		int k_max;
		int k_step;
		list <int> k_list;
		int min_contig_length;
	} MegaHitParams;


	typedef structure {
		list<string> console_out;
		list<string> report;
	} MegaHitOutput;

	funcdef run_megahit(MegaHitParams params) returns (MegaHitOutput output)
		authentication required;

};