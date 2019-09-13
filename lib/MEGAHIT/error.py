import os

def report_megahit_error(output_dir, retcode):
    # look for the file "<output_dir>/log"
    # If present, slurp it in and look for the line(s) with "[ERROR]" at the front and
    # return them as the error
    # Also, dump the MEGAHIT log out to the job run log.
    error_str = "Error running MEGAHIT, return code: " + str(retcode)
    logfile = os.path.join(output_dir, "log")
    error_lines = list()

    ERROR_BLOCK = "[ERROR]"

    if os.path.exists(logfile):
        print("MEGAHIT RUN LOG\n===============\n")
        with open(logfile, "r") as log:
            for count, line in enumerate(log):
                print(line)  # dump to the log.
                line = line.strip()
                if line.startswith(ERROR_BLOCK):
                    error_lines.append(line.split(ERROR_BLOCK)[-1])
    else:
        error_str += "\nUnable to find MEGAHIT log."

    if error_lines:
        error_str += "\nAdditional Information\n" + "\n".join(error_lines)
    return error_str
