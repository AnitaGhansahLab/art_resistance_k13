import os
from optparse import OptionParser

def get_name(title):
    """
    Extracts the simple name from a FASTA header.

    Args:
        title (str): The header of a FASTA sequence.

    Returns:
        str: The simple name extracted from the header.
    """
    return title.split()[0][1:].strip()

def count_differences(ref, seq):
    """
    Counts the differences between a reference sequence and another sequence.

    Args:
        ref (str): The reference nucleotide sequence.
        seq (str): The nucleotide sequence to compare.

    Returns:
        list: A list of differences formatted as "ref_basepositionalt_base".

    Raises:
        Exception: If the sequences are not of the same length.
    """
    if len(ref) != len(seq):
        raise Exception("Invalid sequence lengths, sequences must be of equal length.")

    diffs = []
    for i in range(len(ref)):
        if ref[i] != seq[i]:
            diffs.append(f"{ref[i]}{i+1}{seq[i]}")
    return diffs

def break_fasta(sequence, length=60):
    """
    Breaks a sequence into shorter lines of specified length for formatting purposes.

    Args:
        sequence (str): The nucleotide sequence.
        length (int, optional): The maximum length of each line. Default is 60.

    Returns:
        str: The formatted sequence with line breaks.
    """
    return "\n".join([sequence[i:i+length] for i in range(0, len(sequence), length)])

def run_analysis(ref_sequence, fasta_filename, output_dir, prefix):
    """
    Analyzes a FASTA file, comparing each sequence to a reference sequence,
    and writes results to output files.

    Args:
        ref_sequence (str): The reference nucleotide sequence.
        fasta_filename (str): The path to the input FASTA file.
        output_dir (str): The directory where output files will be saved.
        prefix (str): The prefix for the output filenames.
    """
    hap_data = {}

    def process(title, content):
        """
        Processes each FASTA entry, adding sequences and their identifiers to the haplotype data.

        Args:
            title (str): The FASTA header.
            content (str): The corresponding nucleotide sequence.
        """
        if not title or not content:
            return
        print(f"Processing {title}...")

        name = get_name(title)
        if content in hap_data:
            hap_data[content].append(name)
        else:
            hap_data[content] = [name]

    # Read and process the FASTA file
    with open(fasta_filename) as fasta_file:
        title, content = None, ""
        for line in fasta_file:
            line = line.strip()
            if not line:
                continue

            if line.startswith(">"):
                if title is not None:
                    process(title, content)
                title, content = line, ""
            else:
                content += line
        process(title, content)  # Process the last entry

    # Write haplotype data to output files
    with open(os.path.join(output_dir, f"{prefix}-haplotype-sequences-n-ids.tab"), "w") as hap_file, \
         open(os.path.join(output_dir, f"{prefix}-haplotype-min-sequences-n-ids.tab"), "w") as hap_min_file, \
         open(os.path.join(output_dir, f"{prefix}-haplotype-ids-n-info.tab"), "w") as hap_info_file, \
         open(os.path.join(output_dir, f"{prefix}-haplotype-ids-n-names.tab"), "w") as hap_names_file:

        hap_file.write("ID\tHAPLOTYPE\tREF_DIFF\tIS_REF\n")
        hap_min_file.write("ID\tHAPLOTYPE\tREF_DIFF\tIS_REF\n")
        hap_info_file.write("ID\tHAP_COUNT\tREF_DIFF\tIS_REF\n")
        hap_names_file.write("ID\tHAP_COUNT\tHAP_NAMES\tREF_DIFF\tIS_REF\n")

        counter = 1
        for hap, names in hap_data.items():
            hap_id = f"hap_{counter}"
            name_count = len(names)
            diffs = count_differences(ref_sequence, hap)
            diff_count = len(diffs)
            is_ref = diff_count == 0

            hap_min = ",".join(diffs) if diffs else "-"
            hap_file.write(f"{hap_id}\t{hap}\t{diff_count}\t{is_ref}\n")
            hap_min_file.write(f"{hap_id}\t{hap_min}\t{diff_count}\t{is_ref}\n")
            hap_info_file.write(f"{hap_id}\t{name_count}\t{diff_count}\t{is_ref}\n")
            hap_names_file.write(f"{hap_id}\t{name_count}\t{','.join(names)}\t{diff_count}\t{is_ref}\n")

            counter += 1

def main():
    """
    The main function that parses command-line options and initiates the analysis.
    """
    parser = OptionParser()
    parser.add_option("-f", "--fasta", dest="fasta", type="str", help="Input FASTA file path")
    parser.add_option("-r", "--ref", dest="ref", type="str", help="Reference nucleotide sequence file path")
    parser.add_option("-p", "--prefix", dest="prefix", type="str", help="Prefix for output filenames")
    parser.add_option("-o", "--output", dest="output", type="str", help="Output directory")

    (options, _) = parser.parse_args()

    if not options.fasta or not os.path.isfile(options.fasta):
        parser.error("Input FASTA file is required and must be a valid file path.")
    if not options.ref or not os.path.isfile(options.ref):
        parser.error("Reference nucleotide sequence file is required and must be a valid file path.")
    if not options.output or os.path.isfile(options.output):
        parser.error("Output directory is required and should not be a file.")
    if not options.prefix:
        parser.error("Prefix for output filenames is required.")

    # Create the output directory if it does not exist
    os.makedirs(options.output, exist_ok=True)

    # Read the reference sequence
    with open(options.ref) as ref_file:
        ref_sequence = "".join(ref_file.readlines()[1:]).replace("\n", "")

    # Run the analysis
    run_analysis(ref_sequence, options.fasta, options.output, options.prefix)

if __name__ == "__main__":
    main()
