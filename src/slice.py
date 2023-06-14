# imports
import os
import toml
import subprocess
import multiprocessing

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

# prepare division
n = multiprocessing.cpu_count()
size = lines // n
slices = [[i * size, (i + 1) * size] for i in range(n)]
slices[-1][1] = lines
print(f'Dividing into {n} files across an equivalent number of cores.')
print(f'Each file will contain approximately {size} lines.')
print(f'Slicing main corpus according to map: {slices}.')

# prepare artifacts dir
artifacts = os.path.join(dir, 'artifacts')
if not os.path.isdir(artifacts):
    os.mkdir(artifacts)
    print('Created artifacts directory inside main corpus.')
else:
    print('Using artifacts directory to store files.')

# write files
for slice in slices:
    with open(f'{artifacts}/part-{slice[0]}-{slice[1]}.txt', 'w+') as out:
        # `sed` starts from line 1 and is end inclusive
        lines = subprocess.check_output(
            ['sed', '-n', f'{slice[0] + 1},{slice[1]}p', txt]
        ).decode('utf-8')
        out.write(lines)
        print(f'Cached words {slice[0]}-{slice[1]}.')

print('All jobs finished.')
