from flask import Flask, request, render_template
from app.corpus import find, analyze

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/find')
def find_word():
    word = request.args.get('word')
    n = request.args.get('n')
    if n:
        n = int(n)
        try: results = find.find_examples(word, n)
        except: results = []
    else:
        try: results = find.find_examples(word)
        except: results = []
    return render_template('find.html', word=word, results=results)

@app.route('/analyze')
def analyze_word():
    word = request.args.get('word')
    try: result = analyze.analyze_word(word)
    except:
        result = {
            'word': word,
            'POS': '?',
            'lemma': '<unknown>',
            'definitions': 'Word not found in dictionary'
        }
    return render_template('analyze.html', word=word, result=result)

# run app
if __name__ == '__main__':
    app.run('localhost', 8000, debug=True)
