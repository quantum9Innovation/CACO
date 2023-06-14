"""
USAGE: python src/combine.py <n>
<n>: number of files to merge*

*must have been generated with `divide.py`

Combines processed sample parts into one combined processed sample file.

Only use this after processing each of the sample parts,
so that you have a `p-` prefix in front of each filename.

This script will generate a file equivalent to processing the
entire sample, but allows you to use a multithreaded process
(see `process.py`) to process distinct chunks of the file instead,
and then stich them back together.
"""

# imports
import os
import sys
import toml
import subprocess

# get config
with open('config/main.toml', 'r') as f:
    config = toml.load(f)

# get sample dir
sample = config['locs']['sample']
txt = os.path.join(sample, 'sample.txt')
print(f'Using {txt} as representative sample.')

# get lines in sample
output = subprocess.check_output(['wc', '-l', txt])
lines = output.decode('utf-8').split(' ')[0]
lines = int(lines)
print(f'Found {lines} lines in representative sample.')

# prepare division
n = int(sys.argv[1])
size = lines // n
slices = [[i * size, (i + 1) * size] for i in range(n)]
slices[-1][1] = lines
names = [f'{sample}/p-part-{slice[0]}-{slice[1]}.txt' for slice in slices]
print(f'Expecting {n} processed files.')
print(f'Looking for p-part files: {slices}.')

# combine files
print('Combining files …')
with open(f'{sample}/p-sample.txt', 'w+') as out:
    for name in names:
        with open(name, 'r') as f:
            out.write(f.read())

print('All jobs finished.')
