# Contemporary Amharic Corpus (CACO)

This is the Contemporary Amharic Corpus (CACO) version 1.1.
CACO is collected from various sources which are proofread or edited.
The corpus contains about 24 million orthographic words.
Since it is partly a web corpus, we made some automatic spelling error corrections.
Though the corpus was originally tagged with HornMorpho v3, you'll need to download HornMorpho v4 to run the scripts in this repository (if you plan on running any custom morphological analyses).
You can download it from: <https://github.com/hltdi/HornMorpho>

## Running the web version

You can perform basic functions such as getting examples of words in context or morphological analyses from the [Flask app](./app/).
To start it, first install all dependencies with `poetry install` or equivalent.*
Then, run `gunicorn app.main:app` to start a production server.
From there, you can use the pages linked to perform basic functions.
Note that the web UI accesses a representative sample of the corpus (about 1% its size), so it won't have words that are not very frequent.

*See [installation instructions for HornMorpho](https://github.com/hltdi/HornMorpho) if you get an error installing from requirements; HornMorpho will need to be built separately but you can install the rest of the requirements as normal.

## Download

Download and extract the corpus using the link below before running any of the processing scripts in this repository.

<http://wwwiti.cs.uni-magdeburg.de/iti_dke/Datasets/Contemporary_Amharic_Corpus_(CACO)-version_1.1.zip>

### Description

The documents are provided in plain text format and XML format.
The XML documents are the tagged versions of the plain text documents.
For more details about the corpus, refer to the original publication.

## Analyses

The [download](./download/) directory houses the three main files that you'll want to extract (the result of running the scripts listed in [src](./src/)).
[`freq.csv`](./download/freq.csv) is a collection of the most frequent lemmas (not words) in the corpus and relevant statistics about their distribution.
Note that unlike the standard frequency list shipped with the corpus, this frequency list groups lemmas together, so e.g. መሆን and ነው are merged into the verb root ሆነ.
[`sample.txt`](./download/sample.txt) is a representative sample of the main corpus that is 1% of its size, which makes it ideal for running custom analyses.
It contains a random selection of lines from the main corpus, so its contents are truly representative of the entire corpus and not a specific part or source within it.
[`p-sample.txt`](./download/p-sample.txt) contains extracted lemma information from the sample, the result of analyzing it with HornMorpho.

## Conducting Custom Analyses

If you plan on reproducing the frequency analysis or performing your own custom analysis, you'll need to [download the corpus](#download), [install HornMorpho v4](https://github.com/hltdi/HornMorpho), and setup the relevant configuration for the scripts in the [`src`](./src/) directory.

Also make sure you install the required dependencies with `poetry install` or equivalent (Python 3.11 is recommended).

Create a folder in this repository called `config` and place a file `main.toml` within it.
This file should have the following structure:

```toml
[locs]
dir = "/abs/path/to/CACO"
sample = "/abs/path/to/artifacts"
```

The `dir` field should point to the folder containing the main corpus data.
The `sample` field should point to another folder for storing generated artifacts from the scripts in the [`src`](./src/) directory.

All the scripts have docstrings explaining usage instructions.
You may wish to download [the representative sample](download/sample.txt) and place it in the `sample` directory with the name `sample.txt` to avoid having to run the [`segment.py`](./src/segment.py) script, which takes a long time to run and yields non-deterministic results.
To reproduce the frequency analysis after generating or copying [`sample.txt`](./download/sample.txt), run [`divide.py`](./src/divide.py), [`process.py`](./src/process.py), [`combine.py`](./src/combine.py), and then [`freq.py`](./src/freq.py), in that order.

### Note

After installing HornMorpho, open the following script in your site packages*:

```txt
File "python3.11/site-packages/hm/morpho/language.py", line 925, in convert_phones
    self.epenthesis(phones)
```

*Line number may differ depending on installation details. Search for `self.epenthesis(phones)` in `language.py` to find the exact line number.

Then, wrap the `self.epenthesis(phones)` call in a `try` block:

```py
try: self.epenthesis(phones)
except: pass
```

This will prevent any unforeseen errors with the morphological analyzer when running it on the corpus.

## DOI

10.24352/UB.OVGU-2018-144

### Website

<http://dx.doi.org/10.24352/ub.ovgu-2018-144>

## License

All the documents in the corpus are documents which have been made publicly available in the Web.
The corpus has been obtained by crawling the Web.
In this distribution, for copyright reasons, the order of sentences are shuffled.
By downloading this corpus you agree that the corpus should only be used for research purposes.

### Citation

When using this data, please cite the original publication:

> Gezmu, Andargachew Mekonnen, Binyam Ephrem Seyoum, Michael Gasser, and Andreas Nürnberger. "Contemporary Amharic Corpus: Automatically Morpho-Syntactically Tagged Amharic Corpus." In Proceedings of the First Workshop on Linguistic Resources for Natural Language Processing, pp. 65-70. 2018. Available at: <http://www.aclweb.org/anthology/W18-3809>
