
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
# File with list of file/folder names, one per line
# Located in INPUT_DIR
INPUT_FILE = 'input_names'
# Guppy values
GUPPY_PATH = '/opt/ont/guppy/data/'
GUPPY_CONF = get_value('guppy_conf') # Basecalling conf file
BC_KIT = get_value('barcode_kit') # Barcode kit
# Trimmomatic values
BORDER_SC = 20
SLIDING_W = '4:20' # window size 4, quality limit 20
MIN_LEN = 50
AVG_QUAL = 30


def _main():
    # Open the file with open_txt
    l_files = open_txt(INPUT_FILE, INPUT_DIR, header=False, skip='#')
    # Run the pipeline
    pipeline_basecall_barcode(l_files, INPUT_DIR, out_path=OUTPUT_DIR)
    return 0


def pipeline_basecall_barcode(l_files, input_path, out_path='.'):
    # Go through files in l_files
    for i in range(len(l_files)):
        curr_file = l_files[i]
        basecall_barcode_one(curr_file, input_path, out_path=out_path)
    return 0


def basecall_barcode_one(filename, input_path, out_path='.'):
    # Define guppy inputs and outputs
    path_guppy = f'{input_path}/guppy'
    mkdir_p(path_guppy)
    input_file = f'{input_file}/{filename}'
    conf_file = f'{GUPPY_PATH}/{GUPPY_CONF}'
    # Run guppy
    run_guppy(input_file, path_guppy, conf_file, THREADS)
    # Define trimmomatic inputs and outputs
    fastq_in = f'{path_guppy}/barcode'
    in_1 = f'{fastq_in}/{filename}_1.fastq.gz'
    in_2 = f'{fastq_in}/{filename}_2.fastq.gz'
    path_trimm = f'{input_path}/trimmomatic/{filename}'
    adap = define_adapter()
    if adap=='':
        print('# WARNING: Not checking to trim adapters.')
    run_trimmomatic(in_1, in_2, path_trimm, adapters=adap)
    return 0

def define_adapter():
    adap = ''
    i = 0
    keep_while = True
    while i<len(ADAPTERS) and keep_while:
        adap_check = f'{ADAP_DIR}/{ADAPTERS[i]}'
        if file_exists(adap_check) and ADAPTERS[i]!='':
            keep_while = False
            adap = adap_check
        else:
            i+=1
    if i==len(ADAPTERS):
        print(f'### ERROR: Adapter not found. Check {ADAP_DIR}.')
    return adap

def run_barcode(input_file, output_demulti, threads):
    # Initialise guppy barcoder function
    l = 'guppy_barcoder'
    # Define threads
    l += f' -t {threads}'
    # Define input
    l += f' -i {input_file}'
    # Define output
    mkdir_p(output_demulti)
    l += f' -s {output_demulti}'
    # Add --trim_adapters
    l += ' --trim_adapters'
    # Define barcode kits
    l += f' --barcode_kits "{BC_KIT}"'
    # Print and run script
    print(l)
    os.system(l)
    return 0

def run_basecall(path_pod5, path_basecall, conf_file, callers, runners):
    # Initialise guppy basecaller function
    l = 'guppy_basecaller'
    # Define input as recursive
    l += ' -r'
    # Define input
    l += f' -i {path_pod5}'
    # Define output
    mkdir_p(path_basecall)
    l += f' -s {path_basecall}'
    # Define config_file
    l += f' -c {conf_file}'
    # Define graphics configuration
    l += ' -x auto'
    # Define number of callers
    l += f' --num_callers {callers}'
    # Define number of GPU runners
    l += f' --gpu_runners_per_device {runners}'
    # Print and run script
    print(l)
    os.system(l)
    return 0

def run_dorado(path_in, path_out, conf_file):
    # Initialise dorado basecaller function
    l = 'dorado basecaller'
    # Define graphics configuration
    l += ' -x cuda:all'
    # Define input as recursive
    l += ' -r'
    # Define files to be emitted
    l += ' --emit-sam --emit-fastq'
    # Define barcode kits
    l += f' --kit-name "{BC_KIT}"'
    # Define config file
    l += f' {conf_file}'
    # Define input
    l += f' {path_in}'
    # Define output
    mkdir_p(path_out)
    l += f' > {path_out}'
    # Print and run script
    print(l)
    os.system(l)
    return 0

def run_guppy(path_in, path_out, conf_file, threads):
    # Define basecall variables
    path_pod5 = f'{path_in}'
    path_basecall = f'{path_out}/basecall'
    callers = int(threads/2.0)
    runners = int(threads/2.0)
    # Run basecalling
    run_basecall(path_pod5, path_basecall, conf_file, callers, runners)
    # Define barcoding variables
    basecalled_files = f'{path_basecall}/*.fastq*'
    path_demult = f'{path_out}/barcode'
    # Run barcoding
    run_barcode(basecalled_files, path_demult, threads)
    return 0

def run_trimmomatic(in1, in2, out_base, adapters=''):
    # Define variables from global constants
    border_score = BORDER_SC
    sliding_w = SLIDING_W
    minlen = MIN_LEN
    avgqual = AVG_QUAL
    # Define input
    l = f'TrimmomaticPE -phred33 {in1} {in2}'
    # Define outputs
    l += f' {out_base}_forward_paired.fastq.gz'
    l += f' {out_base}_forward_unpaired.fastq.gz'
    l += f' {out_base}_reverse_paired.fastq.gz'
    l += f' {out_base}_reverse_unpaired.fastq.gz'
    # Define adapters
    if adapters!='':
        l += f' ILLUMINACLIP:{adapters}:2:30:10'
    # Define score tresholds
    l += f' LEADING:{border_score}'
    l += f' TRAILING:{border_score}'
    l += f' SLIDINGWINDOW:{sliding_w}'
    l += f' MINLEN:{minlen}'
    l += f' AVGQUAL:{avgqual}'
    # Print and run script
    print(l)
    os.system(l)
    return 0


if __name__=='__main__':
    _main()
