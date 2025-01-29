
import os
import copy
from file_manager import rmfolder

# Important directories
INPUT_DIR = '/home/promethion/minknow_outputs'
OUTPUT_DIR = '/home/promethion/Documents/nanopore_pipeline'
REF_DIR = '/home/promethion/Documents/ref_seq'
THREADS = 12


def _main():
    # Define dict of data
    data_dict = {}
    # 
    return 0


def open_vcf(vcf_name, vcf_path='.', ext='.vcf', sep='\t'):
    """
    Opens a vcf file and returns a list of genetic variants.
    """
    # Initialize the output variable
    m_out = []
    # Initialize column titles
    coltitles = []
    # Define file path
    filepath = f'{vcf_path}/{vcf_name}{ext}'
    with open(filepath, 'r') as f:
        header = False
        # Go through lines
        for line in f.readlines():
            # Check until line is the title
            if line.startswith('#CHROM'):
                if not header:
                    header = True
                    # Load column titles to coltitles
                    coltitles = line.lstrip('#').rstrip('\n').split(sep)
                else:
                    print(f'ERROR in line:\n{line}')
                    break
            elif header:
                # Define line as list of values
                cl = line.rstrip('\n').split(sep)
                # Initialize dict of values
                dict_line = {}
                # Go through values in cl
                for i in range(len(cl)):
                    # Load each value to dict_line
                    dict_line[coltitles[i]] = cl[i]
                # Load dict_line to m_out
                m_out.append(copy.deepcopy(dict_line))
    return m_out


if __name__=='__main__':
    _main()
