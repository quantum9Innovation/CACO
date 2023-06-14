"""
USAGE: python src/freq.py <n>
<n>: threshold for frequency

Generates a frequency list from the combined processed sample.

Only use this after processing each of the sample parts
and then combining them into `p-sample.txt`.

This script will generate a csv file with the most common terms
at the top and various frequency statistics; all lemmas which are not
found at least `n` times will be ignored
(a good value for `n` is about 5).
"""

# imports
import os
import re
import sys
import toml
import subprocess
from tqdm import tqdm

# get config
with open('config/main.toml', 'r') as f:
    config = toml.load(f)

# get sample dir
sample = config['locs']['sample']
txt = os.path.join(sample, 'p-sample.txt')
print(f'Preparing to extract frequency data from {txt}')

# get lines in sample
output = subprocess.check_output(['wc', '-l', txt])
lines = output.decode('utf-8').split(' ')[0]
lines = int(lines)
print(f'Found {lines} lines in processed sample.')

# initialize counters
freq = {}

# processor
def process(line):
    """Extract lemma from processed line."""
    lemma = line.split(': ')[1]
    if '|' not in lemma: return lemma
    else: return lemma.split('|')[0]

# parse sample
processed = 0
with open(txt, 'r') as f:
    for line in tqdm(f, total=lines):
        if line.isspace() or line == '': continue
        if ': ' not in line: continue

        lemma = process(line).strip()
        if lemma == '': continue
        processed += 1

        if lemma not in freq: freq[lemma] = 1
        else: freq[lemma] += 1
    print('Frequency data collected.')

# analyze frequency data
threshold = int(sys.argv[1])
words = sorted(freq.items(), key=lambda x: x[1], reverse=True)
per10k = lambda x: round(1e4 * x[1] / processed, 2)
inCorp = lambda x: x[1] * 100
print('Writing frequency list to file …')
with open(f'{sample}/freq.csv', 'w+') as f:
    f.write('lemma,count,per 10k,count in corpus (est)\n')
    for word in words:
        if word[1] < threshold: continue
        matches = re.findall(
            r'[።፣"፤?.)(…!\'/፦[\[\];​,]|[a-zA-Z0-9]+', word[0]
        )
        if len(matches) > 0: continue
        f.write(f'{word[0]},{word[1]},{per10k(word)},{inCorp(word)}\n')

print('All jobs finished.')
