import os, sys
from optparse import OptionParser

# extract simple name from fasta header
def getName(title):
    return title.split()[0][1:].strip()


# count differences
def difference(ref, seq):
    if not len(ref) == len(seq):
        raise Exception("Invalid sequences lengths")

    diffs = []
    for i in range(len(ref)):
        if not ref[i] == seq[i]:
            deffs.append(f"{ref[i]}{i+1}{seq[i]}")
    return diffs


# break fasta sequences into short lengths
def breakFasta(sequence):
    LENGTH = 60
    ln = len(sequence)

    seq = ""
    i = 0
    while i < ln:
        if i+LENGTH < ln:
            seq += f"{sequence[i:i+LENGTH]}\n"
        else:
            seq += sequence[i:]
        i += LENGTH
    return seq.strip()


# process 
def runAnalysis(ref_sequence, fasta_filename, out_dir, prefix):
    HAP_DATA = {}

    def process(title, content):
        if not title or not content:
            return
        print(f"Processing {title}...")

        name = getName(title)
        if content in HAP_DATA:
            HAP_DATA[content].append(nanme)
        else:
            HAP_DATA[content] = [name]

    # read fasta file
    with open(fasta_filename) as f:
        title = None
        content = ""

        for line in f:
            line = line.strip()
            if not line: continue

            if line.startswith(">"):
                if title is not None:
                    process(title, content)
                
                title = line
                content = ""
                continue

            content += line

        process(title, content)

    #
    hap_file = open(f"{out_dir}/{prefix}-haplotype-sequences-n-ids.tab", "w")
    hap_min_file = open(f"{out_dir}/{prefix}-haplotype-min-sequences-n-ids.tab", "w")
    hap_info = open(f"{out_dir}/{prefix}-haplotype-ids-n-info.tab", "w")
    hap_names = open(f"{out_dir}/{prefix}-haplotype-ids-n-names.tab", "w")

    hap_file.write("ID\tHAPLOTYPE\tREF_DIFF\tIS_REF\n")
    hap_min_file.write("ID\tHAPLOTYPE\tREF_DIFF\tIS_REF\n")
    hap_info.write("ID\tHAP_COUNT\tREF_DIFF\tIS_REF\n")
    hap_names.write("ID\tHAP_COUNT\tHAP_NAMES\tREF_DIFF\tIS_REF\n")

    # save
    counter = 1
    for hap in HAP_DATA:
        hap_id = f"hap_{counter}"
        names = HAP_DATA[hap]
        names_count = len(names)
        diffs = difference(ref_sequence, hap)
        diff_count = len(diffs)
        is_ref = diff_count == 0

        hap_min = ','.join(diffs)
        if is_ref:
            hap_min = "-"

        hap_file.write(f"{hap_id}\t{hap}\t{diff_count}\t{is_ref}\n")
        hap_min_file.write(f"{hap_id}\t{hap_min}\t{diff_count}\t{is_ref}\n")
        hap_info.write(f"{hap_id}\t{names_count}\t{diff_count}\t{is_ref}\n")
        hap_names.write(f"{hap_id}\t{names_count}\t{','.join(names)}\t{diff_count}\t{is_ref}\n")

        counter += 1

    hap_file.close()
    hap_min_file.close()
    hap_info.close()
    hap_names.close()

#main
def main():
    parser = OptionParser()
    parser.add_option("-f", "--fasta", dest="fasta", type=str, help="Input fasta file")
    parser.add_option("-r", "--ref", dest="ref", type=str, help="Nucleotide reference fasta sequence")
    parser.add_option("-p", "--prefix", dest="prefix", type=str, help="Output names prefix")
    parser.add_option("-o", "--output", dest="output", type=str, help="Output directory")
    (options, args) = parser.parse_args()

    if not options.fasta or not os.path.isfile(options.fasta):
        parser.print_help()
        return

    if not options.ref or not os.path.isfile(options.ref):
        parser.print_help()
        return

    if not options.output or os.path.isfile(options.output):
        parser.print_help()
        return

    if not options.prefix:
        parser.print_help()
        return

    # create results dir
    if not os.path.isdir(options.output):
        os.makedirs(options.output, exist_ok=True)

    # ref sequences
    REF = ("".join(open(options.ref).readlines()[1:])).replace("\n", "")

    # run
    runAnalysis(REF, options.fasta, options.output, options.prefix)


if __name__ == '__main__':
    main()
