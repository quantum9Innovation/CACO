"""
USAGE: python post/analyze.py <word>
<word>: Word to analyze
"""

# imports
import hm
import sys

# analyze
word = sys.argv[1]
analysis = hm.anal('amh', word)

# process
if len(analysis) == 0:
    print(f'\nWord: {word}')
    print('No analysis found.')
    exit()
analysis = analysis[0]
POS = analysis.get('POS', '?')
lemma = analysis.get('lemma', '<unknown>')
definitions = analysis.get('gloss', 'Word not found in dictionary')

# print
print(f'\nWord: {word}')
print(f'POS: {POS}')
print(f'Lemma: {lemma}')
print(f'Definitions: {definitions}')
print('\n===========\n')
print(f'Full analysis: {analysis}')
