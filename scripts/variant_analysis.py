
import os
import copy
from scripts.file_manager import mkdir_p

# Important directories
INPUT_DIR = '/home/promethion/minknow_outputs'
OUTPUT_DIR = '/home/promethion/Documents/nanopore_pipeline'
REF_DIR = '/home/promethion/Documents/ref_seq'
THREADS = 12
TEST_MODE = False

BASE_DIR = '/mnt/d/Descargas/cosas_minion'

def _main():
    if TEST_MODE:
        # Define a subset of data for data_dict
        data_dict = {
            'VCFs_corrida1':[
                'Barcode_1_Gen',
                'Barcode_1_Pseudogen'
                ]
            }
    else:
        # Define dict of data
        data_dict = _generate_data_dict(separated=True)
    ### Test
    #vcf_name = 'phased_merge_output' # VCFs_corrida1 / VCFs_corrida2
    vcf_name = 'variant_calls' # VCFs_corrida3
    vcf_path = f'{BASE_DIR}/VCFs_corrida3/Barcode_4_Gen'
    m_vcf = open_vcf(vcf_name, vcf_path=vcf_path)
    print(m_vcf)
    ###
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
                    if coltitles[i]=='INFO':
                        dict_line['INFO'] = process_info(cl[i])
                    elif coltitles[i]=='FORMAT':
                        pass
                    elif coltitles[i]=='SAMPLE':
                        cl_samp = cl[coltitles.index('SAMPLE')]
                        cl_format = cl[coltitles.index('FORMAT')]
                        dict_line['SAMPLE'] = process_sample(
                            cl_samp,
                            cl_format
                            )
                    else:
                        # Load most values directly to dict_line
                        dict_line[coltitles[i]] = cl[i]
                # Load dict_line to m_out
                m_out.append(copy.deepcopy(dict_line))
    return m_out


def process_info(info_str):
    """
    Processes the INFO column of a VCF file.
    """
    # Initialize output variable
    m_out = {}
    # Split info_str by semicolon
    l_info = info_str.split(';')
    # Go through l_info
    for i in l_info:
        # Split by equal sign
        l_i = i.split('=')
        # Check if l_i has two values
        if len(l_i)==2:
            # Load normally to m_out
            m_out[l_i[0]] = l_i[1]
        elif len(l_i)<2:
            # Load None to m_out
            m_out[l_i[0]] = None
        else:
            # Load to m_out but print warning
            m_out[l_i[0]] = l_i[1]
            print(f'WARNING: {l_i} has more than two values.')
    return m_out

def process_sample(sample_str, format_str):
    """
    Processes the SAMPLE column of a VCF file.
    """
    # Initialize output variable
    m_out = {}
    # Split sample_str by colon
    l_sample = sample_str.split(':')
    # Split format_str by colon
    l_format = format_str.split(':')
    # Go through l_sample
    for i in range(len(l_sample)):
        # Load to m_out
        m_out[l_format[i]] = l_sample[i]
    return m_out


def _generate_data_dict(separated=True):
    # Define dict of data
    data_dict = {}
    # Define data_dict based on available folders
    for j in [1,2]:
        curr_key = f'VCFs_corrida{j}'
        data_dict[curr_key] = []
        for i in range(1,25):
            if separated:
                data_dict[curr_key].append(f'Barcode_{i}_Gen')
                data_dict[curr_key].append(f'Barcode_{i}_Pseudogen')
            else:
                l_folders = (
                    f'Barcode_{i}_Gen',
                    f'Barcode_{i}_Pseudogen'
                    )
                data_dict[curr_key].append(l_folders)
    curr_key = 'VCFs_corrida3'
    data_dict[curr_key] = []
    for i in range(4,25):
        if separated:
            data_dict[curr_key].append(f'Barcode_{i}_Gen')
            data_dict[curr_key].append(f'Barcode_{i}_Pseudogen')
        else:
            l_folders = (
                f'Barcode_{i}_Gen',
                f'Barcode_{i}_Pseudogen'
                )
            data_dict[curr_key].append(l_folders)
    return data_dict


if __name__=='__main__':
    _main()
