"""
Loads representative sample and generates slices for multiprocessing.

These slices can be used to run analyses in parallel on all cores,
which significantly speeds up analysis time.

This performs an identical function to `slice.py`,
but for the representative sample.
"""

# imports
import os
import toml
import subprocess
import multiprocessing

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
n = multiprocessing.cpu_count()
size = lines // n
slices = [[i * size, (i + 1) * size] for i in range(n)]
slices[-1][1] = lines
print(f'Dividing into {n} files across an equivalent number of cores.')
print(f'Each file will contain approximately {size} lines.')
print(f'Slicing main corpus according to map: {slices}.')

# write files
for slice in slices:
    with open(f'{sample}/part-{slice[0]}-{slice[1]}.txt', 'w+') as out:
        # `sed` starts from line 1 and is end inclusive
        lines = subprocess.check_output(
            ['sed', '-n', f'{slice[0] + 1},{slice[1]}p', txt]
        ).decode('utf-8')
        out.write(lines)
        print(f'Cached words {slice[0]}-{slice[1]}.')

print('All jobs finished.')
