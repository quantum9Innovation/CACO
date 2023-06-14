"""
Loads main corpus and chooses ~10k lines at random.

These will be used to form the representative sample,
which can then be used for things like frequency analysis e.g.
without loading the entire corpus into memory.

This script uses `sed` to get the correct lines and is therefore
very, very slow (only run this if you want to regenerate the sample).

This script yields non-deterministic results!
"""

# imports
import os
import toml
import numpy as np
import subprocess
from tqdm import tqdm

# get config
with open('config/main.toml', 'r') as f:
    config = toml.load(f)

# get corpus dir
dir = config['locs']['dir']
txt = os.path.join(dir, 'CACO_TEXT.txt')
print(f'Using {txt} as main corpus location.')

# get lines in corpus
output = subprocess.check_output(['wc', '-l', txt])
lines = output.decode('utf-8').split(' ')[0]
lines = int(lines)
print(f'Found {lines} lines in main corpus.')

# prepare segmentation
size = lines // 100
selected = np.random.choice(lines, size, replace=False)
selected.sort()
print(f'Using a 1% representative sample with {size} lines.')

# prepare artifacts dir
artifacts = os.path.join(dir, 'artifacts')
if not os.path.isdir(artifacts):
    os.mkdir(artifacts)
    print('Created artifacts directory inside main corpus.')
else:
    print('Using artifacts directory to store files.')

# write files
print('Generating representative sample …')
with open(f'{artifacts}/sample.txt', 'w+') as out:
    for line in tqdm(selected, total=size):
        # `sed` starts from line 1
        copied = subprocess.check_output(
            ['sed', '-n', f'{line + 1}p', txt]
        ).decode('utf-8')
        out.write(copied)

print('All jobs finished.')
