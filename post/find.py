"""
USAGE: python post/find.py <lemma> <n>?
<lemma>: Lemma to find in sample
<n>: Max examples to show
"""

# imports
import os
import sys
import random
import subprocess
from tqdm import tqdm

# get download dir
download = './download'
processed = os.path.join(download, 'p-sample.txt')
sample = os.path.join(download, 'sample.txt')
print(f'Looking for lemma forms in {processed}.')
print(f'Finding lemma in {sample}.')

# get lines in processed sample
output = subprocess.check_output(['wc', '-l', processed])
lines = output.decode('utf-8').split(' ')[0]
lines = int(lines)
print(f'Found {lines} lines in processed sample.')

# initialize counters
lemma = sys.argv[1]
truncate = False
n = 0
if len(sys.argv) > 2:
    truncate = True
    n = int(sys.argv[2])
forms = [lemma]

# processors
def original(line):
    """Extract original word from processed line."""
    return line.split(': ')[0]

def process(line):
    """Extract lemma from processed line."""
    p_lemma = line.split(': ')[1]
    if '|' not in p_lemma: return p_lemma
    else: return p_lemma.split('|')[0]

# process sample
with open(processed, 'r') as f:
    for line in tqdm(f, total=lines):
        if line.isspace() or line == '': continue
        if ': ' not in line: continue

        p_lemma = process(line).strip()
        if p_lemma == '': continue

        if lemma == p_lemma and p_lemma not in forms:
            form = original(line).strip()
            if form == '': continue
            forms.append(form)
    print('Word forms identified.')

# get lines in sample
out_sample = subprocess.check_output(['wc', '-l', sample])
ln_sample = out_sample.decode('utf-8').split(' ')[0]
ln_sample = int(ln_sample)
print(f'Found {ln_sample} lines in processed sample.')

# find lemma in corpus
matches = []
with open(sample, 'r') as f:
    for line in tqdm(f, total=ln_sample):
        if line.isspace() or line == '': continue
        for form in forms:
            if form in line: matches.append(line)
    if len(matches) > 1: print(f'{len(matches)} matches found.')
    elif len(matches) == 1: print('1 match found.')
    else:
        print('No matches found.')
        exit()

# process matches
if truncate:
    random.shuffle(matches)
    matches = matches[:n]

# print matches
print('\n==============\n')
for match in matches: print(match)
print('\n==============\n')

print('All jobs finished.')
