import os
import time

def get_dir_size(path='.'):
    total = 0
    with os.scandir(path) as it:
        for entry in it:
            if entry.is_file():
                total += entry.stat().st_size
            elif entry.is_dir():
                total += get_dir_size(entry.path)
    return total

def clean_files(keep_time, max_size):
    '''
    files will be kept if they were created in the last keep_time seconds
    '''
    for f in os.listdir('video/'):
        if (os.path.isfile(os.path.join('video/', f)) and f.endswith('.mp4') and os.path.getmtime(os.path.join('video/', f)) < time.time() - keep_time):
            os.remove(os.path.join('video/', f))
            print('Deleted: ' + f)
            
    while get_dir_size('video/') > (max_size * 1024 * 1024):
        # Delete oldest files until the size is less than max_size

        # Get the oldest file
        oldest = min(['video/' + f for f in os.listdir('video/')], key=os.path.getmtime)
        os.remove(oldest)
        print('Deleted: ' + oldest)