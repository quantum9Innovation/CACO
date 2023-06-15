from . import hm

def analyze_word(word):
    """
    Generate word analysis.
    Returns dictionary with analysis.
    """
    if word is None: return
    analysis = hm.anal('amh', word)
    result = {}
    if len(analysis) == 0:
        result['word'] = word
        result['POS'] = '?'
        result['lemma'] = '<unknown>'
        result['definitions'] = 'Word not found in dictionary'
    else:
        analysis = analysis[0]
        result['word'] = word
        result['POS'] = analysis.get('POS', '?')
        result['lemma'] = analysis.get('lemma', '<unknown>')
        result['definitions'] = analysis.get('gloss', 'Word not found in dictionary')
    return result
