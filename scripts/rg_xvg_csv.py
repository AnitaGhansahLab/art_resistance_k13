import os
import argparse

# Set up argument parser
parser = argparse.ArgumentParser(description='Process .xvg files.')
parser.add_argument('directory', type=str, help='The directory containing .xvg files')

# Parse the command-line argument
args = parser.parse_args()

# List files in the specified directory
xvg_files = os.listdir(args.directory)

# Process each file
for i in xvg_files:
    if ".xvg" in i:
        xvg_name = i[:-4]  # Fix the slicing to remove ".xvg" correctly
        os.system(f"cat {os.path.join(args.directory, i)} | tail -n+28 | awk '{{print $2}}' > {os.path.join(args.directory, xvg_name)}.csv")
    else:
        pass
