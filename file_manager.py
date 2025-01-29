
import os

def eliminate_spaces(dirname):
    # Replace spaces with underscores
    newdirname = dirname.replace(' ', '_')
    # Use mvdir to rename dirname
    mv_file(dirname.replace(' ', '\ '), newdirname, sudo=True)
    return 0

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
