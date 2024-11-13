
import os

# Important directories
INPUT_DIR = '/home/promethion/minknow_outputs'
OUTPUT_DIR = '/home/promethion/Documents/nanopore_pipeline'
REF_DIR = '/home/promethion/Documents/ref_seq'
THREADS = 12


def _main():
    # Define the list of barcodes
    l_bc = ['barcode01', 'barcode02', 'barcode03', 'barcode04',
            'barcode05', 'barcode06', 'barcode07', 'barcode08',
            'barcode09', 'barcode10', 'barcode11', 'barcode12',
            'barcode13', 'barcode14', 'barcode15', 'barcode16',
            'barcode17', 'barcode18', 'barcode19', 'barcode20',
            'barcode21', 'barcode22', 'barcode23', 'barcode24'
            ]
    # Define folders
    run_folder = 'run3'
    refname = 'hg38'
    # Run the entire pipeline
    pipeline_main(l_bc, run_folder, refname, ref_ext='.fasta')
    return 0


def pipeline_main(l_bc, run_folder, refname, ref_ext='.fasta'):
    # Define folders
    path_in = f'{INPUT_DIR}/{run_folder}'
    path_fastq = f'{OUTPUT_DIR}/{run_folder}'
    ref_dir = f'{REF_DIR}'
    path_minimap2 = f'{OUTPUT_DIR}/sam_bam'
    path_nanocall = f'{OUTPUT_DIR}/vcf_nanocall'
    path_whatshap_nc = f'{OUTPUT_DIR}/whatshap_nc'
    # Join fastq files
    join_fastq_l_bc(l_bc, path_fastq, path_in)
    # Run minimap2 on the list of barcodes
    minimap2_alignment(l_bc,
                       path_fastq,
                       ref_dir,
                       path_minimap2,
                       refname,
                       ref_ext=ref_ext
                       )
    # Move reference to path_minimap2
    ref_file = f'{ref_dir}/{refname}{ref_ext}'
    mv_ref_file = f'{path_minimap2}/{refname}{ref_ext}'
    mv_file(ref_file, mv_ref_file)
    # Run NanoCall on the list of barcodes
    variant_call_nanocall_list(l_bc,
                               path_minimap2,
                               path_nanocall,
                               refname,
                               ref_ext=ref_ext
                               )
    # Run Whatshap on the variant caller output
    whatshap_list(l_bc,
                  path_nanocall,
                  path_minimap2,
                  path_whatshap_nc,
                  refname,
                  vcf_name='variant_calls.vcf.gz',
                  ref_ext='.fasta'
                  )
    return 0


def join_fastq_l_bc(l_bc, path_out, path_in):
    # Create path_out folder if it does not exist
    mkdir_p(path_out)
    # Go through the barcode list
    for curr_bc in l_bc:
        ### Display
        print('Concatenating ' + str(curr_bc))
        # Define in/out for join_fastq
        dir_bc = f'{path_in}/{curr_bc}'
        path_conc_out = f'{path_out}/{curr_bc}_concat.fastq'
        # Run join_fastq
        join_fastq(dir_bc, path_conc_out)
    return 0

def join_fastq(bc_path, path_concat):
    """
    Joins the different .fastq files that come out of guppy/dorado. 
    Creates a single .fastq file out of the files in bc_path.
    """
    # Define path to the .fastq files within the barcode
    used_path = f'{bc_path}/*.fastq'
    # Define the script with cat
    l = 'cat'
    # Add input path
    l += f' {used_path}'
    # Add output path
    l += f' > {path_concat}'
    # Print and run the script
    print(l)
    os.system(l)
    return 0

def mkdir_p(outdir):
    l = f'mkdir -p {outdir}'
    os.system(l)
    return 0

def minimap2_alignment(l_bc,
                       path_fq_in,
                       ref_dir,
                       path_out,
                       refname,
                       ref_ext='.fasta',
                       threads=12
                       ):
    # Make directories if they do not exist
    mkdir_p(path_out)
    # Go through barcodes
    for i in range(len(l_bc)):
        curr_bc = l_bc[i]
        # Define variables
        path_fastq = f'{path_fq_in}/{curr_bc}_concat.fastq'
        path_ref = f'{ref_dir}/{refname}{ref_ext}'
        path_sam = f'{path_out}/{refname}_{curr_bc}.sam'
        path_bam = f'{path_out}/{refname}_{curr_bc}_sorted.bam'
        # Run minimap2 and samtools
        run_minimap2_samtools(path_fastq,
                              path_sam,
                              path_bam,
                              path_ref,
                              threads
                              )
    return 0

def mv_file(path_in, path_out):
    # Start the mv script
    l = 'mv'
    # Add input
    l += f' {path_in}'
    # Add output
    l += f' {path_out}'
    # Print and run script
    print(l)
    os.system(l)
    return 0

def run_minimap2_samtools(path_fastq, path_sam, path_bam, path_ref, t):
    # Start the script
    l = 'minimap2'
    # Define type of read
    l += ' -ax map-ont'
    # Define number of threads
    l += f' -t {t}'
    # Define reference sequence
    l += f' {path_ref}'
    # Define fastq path
    l += f' {path_fastq}'
    # Define output
    l += f' > {path_sam}'
    # Print and run script
    print(l)
    os.system(l)
    # Run samtools sort and index
    run_samtools_sort_index(path_sam, path_bam)
    return 0

def run_samtools_index(path_bam):
    # Start the index script
    l = 'samtools index'
    # Define bam to index
    l += f' {path_bam}'
    # Print and run script
    print(l)
    os.system(l)
    return 0

def run_samtools_sort_index(path_sam, path_bam_sorted):
    # Start the sort script
    l = 'samtools sort'
    # Define output
    l += f' -o {path_bam_sorted}'
    # Define sam input
    l += f' {path_sam}'
    # Print and run script
    print(l)
    os.system(l)
    # Run samtools index
    run_samtools_index(path_bam_sorted)
    return 0

def variant_call_nanocall_list(l_bc,
                               path_minimap2,
                               path_nanocall,
                               refname,
                               ref_ext='.fasta'
                               ):
    # Define reference
    fasta_in = f'{refname}{ref_ext}'
    # Go through barcodes
    for bc in l_bc:
        # Define folders
        bam_in = f'{refname}_{bc}_sorted.bam'
        output_dir = f'{path_nanocall}/{bc}'
        # Make output_dir
        mkdir_p(output_dir)
        # Run nanocall on each barcode
        variant_call_nanocall_raw(THREADS,
                                  path_minimap2,
                                  output_dir,
                                  bam_in,
                                  fasta_in
                                  )
    return 0

def variant_call_nanocall_raw(n_t,
                              input_dir,
                              output_dir,
                              bam_in,
                              fasta_in,
                              out_docker='/opt/output/',
                              in_docker='/opt/input/'
                              ):
    # Define variants in os.environ[]
    # Number of threads
    os.environ['nanocall_t'] = str(n_t)
    # Directory for bam inside docker
    os.environ['nanocall_bam'] = in_docker+bam_in
    # Directory for fasta inside docker
    os.environ['nanocall_fasta'] = in_docker+fasta_in
    # Folder to be assigned to in_docker inside docker
    os.environ['nanocall_input'] = input_dir
    # Folder to be assigned to out_docker inside docker
    os.environ['nanocall_output'] = output_dir
    # Directory of input inside docker
    os.environ['nanocall_in_docker'] = in_docker
    # Directory of output inside docker
    os.environ['nanocall_out_docker'] = out_docker
    # Start the docker script
    l = 'sudo -S docker run'
    # Add input folders
    l += ' -v $nanocall_input:$nanocall_in_docker'
    # Add output folders
    l += ' -v $nanocall_output:$nanocall_out_docker'
    # Define function
    l += ' genomicslab/nanocaller:3.4.1 NanoCaller'
    # Define presets and sequencing type
    l += ' --preset ont --sequencing short_ont'
    # Define threads
    l += ' --cpu $nanocall_t'
    # Define bam folder
    l += ' --bam $nanocall_bam'
    # Define fasta folder
    l += ' --ref $nanocall_fasta'
    # Define output folder
    l += ' --output $nanocall_out_docker'
    # Add password call
    l += ' < ./pw.txt'
    # Print and run script
    print(l)
    os.system(l)
    # Start the chmod script
    l = 'sudo -S chmod'
    # Define permissions for new files
    l += ' -R 777'
    # Define the folder to change permissions
    l += f' {output_dir}'
    # Add password call
    l += ' < ./pw.txt'
    # Print and run script
    print(l)
    os.system(l)
    return 0

def whatshap_haplotag(phased_vcf,
                      unphased_bam,
                      output_bam,
                      nom_list,
                      nom_ref,
                      ploidy=2
                      ):
    # Start the whatshap script
    l = 'whatshap haplotag'
    # Define output
    l += f' -o {output_bam}'
    # Define reference
    l += f' --reference {nom_ref}'
    # Allow ignore-read-groups
    l += ' --ignore-read-groups'
    # Define output haplotag list
    l += f' --output-haplotag-list {nom_list}'
    # Define ploidy
    l += f' --ploidy {ploidy}'
    # Define output phased_vcf
    l += f' {phased_vcf}'
    # Define unphased bam
    l += f' {unphased_bam}'
    # Print and run script
    print(l)
    os.system(l)
    # Run samtools index
    run_samtools_index(output_bam)
    return 0

def whatshap_haplo_split(reads_in, reads_out, list_haplo, ext='.bam'):
    # Define variables
    reads_out_1 = reads_out + '_H1' + ext
    reads_out_2 = reads_out + '_H2' + ext
    reads_out_untag = reads_out + '_untag' + ext
    reads_in_ext = reads_in + ext
    # Start the whatshap script
    l = 'whatshap split'
    # Define outputs
    l += f' --output-h1 {reads_out_1}'
    l += f' --output-h2 {reads_out_2}'
    l += f' --output-untagged {reads_out_untag}'
    # Define reads
    l += f' {reads_in_ext}'
    # Define haplo
    l += f' {list_haplo}'
    # Print and run script
    print(l)
    os.system(l)
    # Run samtools index on generated bam files
    run_samtools_index(reads_out_1)
    run_samtools_index(reads_out_2)
    run_samtools_index(reads_out_untag)
    return 0

def whatshap_list(l_bc,
                  path_vcf,
                  path_bam,
                  path_out,
                  refname,
                  vcf_name='variant_calls.vcf.gz',
                  ref_ext='.fasta'
                  ):
    # Go through l_bc
    for i in range(len(l_bc)):
        bc = l_bc[i]
        # Define barcode output folder
        bc_folder = f'{path_out}/{bc}'
        # Make the output directory
        mkdir_p(bc_folder)
        # Define script variables
        phased_vcf = f'{path_vcf}/{bc}/{vcf_name}'
        unphased_bam = f'{path_bam}/{refname}_{bc}_sorted.bam'
        output_bam = f'{bc_folder}/phased_{refname}_{bc}.bam'
        nom_list_ht = f'{bc_folder}/phase_list_haplotag.txt'
        nom_ref = f'{REF_DIR}/{refname}{ref_ext}'
        reads_in = f'{path_bam}/{refname}_{bc}_sorted'
        reads_out = f'{bc_folder}/{refname}_{bc}'
        # Run whatshap scripts
        whatshap_haplotag(phased_vcf, unphased_bam, output_bam, nom_list_ht, nom_ref); 
        whatshap_haplo_split(reads_in, reads_out, nom_list_ht, ext='.bam'); 
    return 0


if __name__=='__main__':
    _main()