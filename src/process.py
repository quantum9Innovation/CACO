"""
Runs a pool of workers to analyze all parts of the sample.

Depending on the number of cores you have, this script may take
different amounts of time to run (expect anywhere from 30-180 min).

Each analyzed file will be stored in a new document with a p- prefix
in front of the original filename.
"""

# imports
import os
import hm
import toml
import glob
import multiprocessing

# get config
with open('config/main.toml', 'r') as f:
    config = toml.load(f)

# get sample dir
sample = config['locs']['sample']
txt = os.path.join(sample, 'sample.txt')
print(f'Using {txt} as main corpus location.')

# get parts
os.chdir(sample)
parts = glob.glob('part-*.txt')
processes = len(parts)
print(f'Found {processes} files to process.')

# worker thread
def process(f):
    """Process a single file."""
    print(f'Processing {f}.')
    hm.anal_file('amh', f, f'p-{f}', lemma_only=True)
    print(f'Processed {f}.')

# multiprocessing
pool = multiprocessing.Pool(processes)
pool.map(process, parts)
pool.close()
pool.join()

print('All jobs finished.')
