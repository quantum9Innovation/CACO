from . import os
from . import random

def find_examples(lemma, n=None):
    """
    Find examples of a given lemma in a corpus.
    Returns a list of example strings.
    """
    if lemma is None: return
    download = './download'
    processed = os.path.join(download, 'p-sample.txt')
    sample = os.path.join(download, 'sample.txt')

    # initialize counters
    forms = [lemma]

    # processors
    def original(line):
        """Extract original word from processed line."""
        return line.split(': ')[0]

    def process(line):
        """Extract lemma from processed line."""
        p_lemma = line.split(': ')[1]
        if '|' not in p_lemma:
            return p_lemma
        else:
            return p_lemma.split('|')[0]

    # process sample
    with open(processed, 'r') as f:
        for line in f:
            if line.isspace() or line == '':
                continue
            if ': ' not in line:
                continue

            p_lemma = process(line).strip()
            if p_lemma == '':
                continue
            
            form = original(line).strip()
            if form == '' or form is None:
                continue
            
            if lemma == p_lemma and form not in forms:
                forms.append(form)

    # find lemma in corpus
    matches = []
    with open(sample, 'r') as f:
        for line in f:
            if line.isspace() or line == '':
                continue
            for form in forms:
                if form in line.split():
                    line = line.replace(form, f':HIGHLIGHT:{form}:HIGHLIGHT:')
                    matches.append(line)
        if len(matches) == 0:
            return []
        
    # process matches
    if n is not None:
        random.shuffle(matches)
        matches = matches[:n]

    # return matches
    return matches
