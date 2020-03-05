/*
A KBase module to wrap the MEGAHIT package.
*/

module MEGAHIT {

    /*
    Run MEGAHIT. Most parameters here are just passed forward to MEGAHIT

    workspace_name - the name of the workspace for input/output
    read_library_ref - the name of the PE read library (SE library support in the future)
    output_contig_set_name - the name of the output contigset

    megahit_parameter_preset -
        override a group of parameters; possible values:
        meta            '--min-count 2 --k-list 21,41,61,81,99'
                        (generic metagenomes, default)
        meta-sensitive  '--min-count 2 --k-list 21,31,41,51,61,71,81,91,99'
                        (more sensitive but slower)
        meta-large      '--min-count 2 --k-list 27,37,47,57,67,77,87'
                        (large & complex metagenomes, like soil)
        bulk            '--min-count 3 --k-list 31,51,71,91,99 --no-mercy'
                        (experimental, standard bulk sequencing with >= 30x depth)
        single-cell     '--min-count 3 --k-list 21,33,55,77,99,121 --merge_level 20,0.96'
                        (experimental, single cell data)

    min_count - minimum multiplicity for filtering (k_min+1)-mers, default 2

    k_min - minimum kmer size (<= 255), must be odd number, defaults to 21
    k_max - maximum kmer size (<= 255), must be odd number, defaults to 141
    k_step - increment of kmer size of each iteration (<= 28), must be even number, defaults to 10

    k_list - list of kmer sizes (all must be odd, in the range 15-255, increment <= 28);
             override using `--k-min', `--k-max' and `--k-step'

    min_contig_length - minimum length of contigs to output, default is 2000

    max_mem_percent - maximum memory to make available to MEGAHIT, as a percentage of
                      available system memory (optional, default = 0.9 or 90%)

    @optional megahit_parameter_preset
    @optional min_count
    @optional k_min
    @optional k_max
    @optional k_step
    @optional k_list
    @optional min_contig_length
    @optional max_mem_percent
    */
    typedef structure {
        string workspace_name;
        string read_library_ref;
        string output_contigset_name;
        string megahit_parameter_preset;
        int min_count;
        int k_min;
        int k_max;
        int k_step;
        list <int> k_list;
        int min_contig_length;
        float max_mem_percent;
    } MegaHitParams;

    typedef structure {
        string report_name;
        string report_ref;
    } MegaHitOutput;

    funcdef run_megahit(MegaHitParams params) returns (MegaHitOutput output)
        authentication required;
};
