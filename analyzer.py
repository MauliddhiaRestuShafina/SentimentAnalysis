#!/usr/bin/env python3


import nltk


def cformat(wordlist):

    newformat = {}
    with open(wordlist, 'r', encoding='utf-8') as words:
        for line in words:
            if line[0].isalnum():
                line = line.rstrip("\n").lower()
                thisword = line.split()[0].split('|')[0]
                POS = line.split()[0].split('|')[1]
                polarity = line.split()[1]

                try:
                    wordforms = line.split()[2].split(',')
                    for wordf in wordforms:
                        newformat[wordf] = [POS, polarity]
                except:
                    pass

                newformat[thisword] = [POS, polarity]
            if 'EOF' in line:
              break

    return newformat


def cformatENG(wordlist, pORn):

    newformat = {}
    with open(wordlist, 'r', encoding='utf-8') as words:
        for line in words:
            if line[0].isalnum():
                thisword = line.rstrip("\n").lower()
                POS = 'ENG'

                if pORn:
                    polarity = 0.1
                else:
                    polarity = -0.1

                newformat[thisword] = [POS, polarity]
            if 'EOF' in line:
              break

    return newformat

class Analyzer():
    """Implements sentiment analysis."""

    def __init__(self, positives, negatives, poENG, neENG):
        """Initialize Analyzer."""

        self.posi = {**cformat(positives), **cformatENG(poENG, True)}
        self.nega = {**cformat(negatives), **cformatENG(neENG, False)}

    def analyze(self, text):
        """Analyze text for sentiment, returning its score."""

        # Converting uppercase letters to lowercase letters and stripping whitespace.
        text = text.strip().lower()

        # Splitting sentence in words.
        tokenizer = nltk.tokenize.TweetTokenizer()
        tokens = tokenizer.tokenize(text)

        score = 0.0

        for tokenword in tokens:
            try:
                self.posi[tokenword]
                score += float(self.posi[tokenword][1])
            except:
                try:
                    self.nega[tokenword]
                    score += float(self.nega[tokenword][1])
                except:
                    score += 0

        return score
