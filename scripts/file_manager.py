
import os


def eliminate_spaces(dirname, dir_path, is_folder=True):
    """
    Eliminates spaces from a file or directory name.
    """
    # Replace spaces with underscores
    newdirname = dirname.replace(' ', '_')
    # Define temp_dirpath
    temp_dirpath = f'/tmp/{newdirname}'
    # Define old and new filepaths
    old_filepath = f'{dir_path}/{dirname.replace(' ', '\ ')}'
    new_filepath = f'{dir_path}/{newdirname}'
    # Change execution if dirname is a folder
    if is_folder:
        # Make new and temp directories
        mkdir_p(temp_dirpath)
        mkdir_p(new_filepath)
        # Use mvdir to rename dirname
        mv_file(old_filepath+'/*', temp_dirpath)
        mv_file(temp_dirpath+'/*', new_filepath)
        # Remove old and temp directories
        rmfolder(old_filepath, safety=False)
        rmfolder(temp_dirpath, safety=False)
    else:
        # Use mvdir to rename dirname
        mv_file(old_filepath, temp_dirpath)
        mv_file(temp_dirpath, new_filepath)
    return 0

def file_exists(filepath):
    return os.path.isfile(filepath)

def get_value(
        valname,
        sourcefile='variables',
        source_path='',
        ext='.txt'
        ):
    """
    Gets the value valname from sourcefile.
    """
    # Initialize value that is returned
    val = ''
    # Define full path to sourcefile
    if source_path=='':
        source_dir = os.path.dirname(os.path.realpath(__file__))
        srcf = f'{source_dir}/../{sourcefile}{ext}'
    else:
        srcf = f'{source_path}/{sourcefile}{ext}'
    # Open sourcefile
    with open(srcf, 'r') as f_src:
        # Go through lines in sourcefile
        for line in f_src.readlines():
            # If valname is in line
            if line.startswith(valname):
                # Split line by '='
                l_line = line.split('=')
                # Get the value and remove spaces and endline
                val = l_line[1].rstrip('\n').strip(' ')
                # Replace spaces with underscores
                val = val.replace(' ', '_')
    # Check if value was found
    if val=='':
        print(f'Value {valname} not found in {sourcefile}{ext}.')
    return val.replace('~', os.getenv("HOME"))

def mkdir_p(dirname):
    l = f'mkdir -p {dirname}'
    os.system(l)
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

def open_txt(
        filename,
        path='',
        ext='.txt',
        sep='',
        header=True,
        skip=''
        ):
    """
    Function to open a txt or csv file and return a list/matrix.

    If sep=='', it does not split lines into lists.

    If a line starts with str(skip), it is skipped. 
    If skip=='', skip is ignored.
    """
    # Define file path
    filepath = f'{path}/{filename}{ext}'
    # Initialise output
    l_out = []
    # Open file
    with open(filepath, 'r') as f:
        # Start header line
        head = header
        # Go through lines
        for line in f.readlines():
            # Skip line if it starts with skip
            if skip!='' and line.startswith(skip):
                pass
            else:
                # If sep is specified, separate line
                if sep!='':
                    cl = line.rstrip('\n').split(sep)
                # If sep is not specified, keep line as str
                else:
                    cl = line.rstrip('\n')
                # Add cl to l_out if it is not the first line
                if head:
                    head = False
                else:
                    l_out.append(cl)
    return l_out

def rmfolder(fpath, safety=True):
    l = f'rm -r {fpath}'
    if safety:
        warn = '### WARNING: About to execute following command:\n'
        warn += l + '\n'
        warn += 'Are you sure? y / N\n'
        ok = input(warn)
        if ok.lower()=='y':
            os.system(l)
        else:
            print('Command not executed.')
    else:
        os.system(l)
    return 0
