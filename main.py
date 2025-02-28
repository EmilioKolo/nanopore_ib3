
from scripts.basecall_barcode import pipeline_basecall_barcode
from scripts.file_manager import open_txt, get_value
from scripts.variant_calling import pipeline_variant_call


INPUT_DIR = get_value('input_dir')
OUTPUT_DIR = get_value('output_dir')
INPUT_FILE = get_value('input_file')


def _main():
    # Open the file with open_txt
    l_files = open_txt(INPUT_FILE, INPUT_DIR, header=False, skip='#')
    # Run the pipeline
    #pipeline_basecall_barcode(l_files, INPUT_DIR, out_path=OUTPUT_DIR)
    # Define the list of barcodes
    l_bc = [i.split('/')[-1].split('.')[0] for i in l_files]
    # Define folders
    run_folder = 'trimmomatic'
    refname = 'hg38'
    # Run the entire pipeline
    pipeline_variant_call(
        l_bc,
        run_folder,
        refname,
        ref_ext='.fasta'
        )
    return 0


if __name__=='__main__':
    _main()
