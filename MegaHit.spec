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
		string console_out;
	} MegaHitOutput;

	funcdef run_megahit(MegaHitParams params) returns (MegaHitOutput output)
		authentication required;




	/*
	A string representing a ContigSet id.
	*/
	typedef string contigset_id;
	
	/*
	A string representing a workspace name.
	*/
	typedef string workspace_name;
	
	typedef structure {
	    int contig_count;
	} CountContigsResults;
	
	/*
	Count contigs in a ContigSet
	contigset_id - the ContigSet to count.
	*/
	funcdef count_contigs(workspace_name,contigset_id) returns (CountContigsResults) authentication required;
};