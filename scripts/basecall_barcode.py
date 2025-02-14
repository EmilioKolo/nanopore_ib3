
import os
from scripts.file_manager import mkdir_p, get_value, open_txt, file_exists

# Important directories
INPUT_DIR = get_value('input_dir')
OUTPUT_DIR = get_value('output_dir')
ADAP_DIR = get_value('adap_dir')
THREADS = get_value('thread_n')
ADAPTERS = [ # Default picks first
    'TruSeq3-PE-3.fa',
    'TruSeq3-PE-2.fa',
    'TruSeq3-PE.fa'
    ]


def _main():
    # Open the file with open_txt
    l_files = open_txt()
    return 0


def pipeline_basecall_barcode(l_files, input_path, output_path='.'):
    return 0


if __name__=='__main__':
    _main()
