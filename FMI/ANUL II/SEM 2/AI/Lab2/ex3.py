import nltk
import spacy
from unidecode import unidecode
import rowordnet as rwn

# nltk.download('punkt')
# nltk.download('wordnet')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('stopwords')
# nltk.download('maxent_ne_chunker')
# nltk.download('words')


def number_of_sentences(file_path):
    """
    number_of_sentences(file_path) receives a file path and returns the number of sentences in the file.
    :param file_path: string
    :return: the number of sentences in the file
    """
    with open(file_path, 'r') as file:
        text = file.read()
        sentences = nltk.sent_tokenize(text)
        return len(sentences)


def number_of_words(file_path, different_words=False):
    """
    number_of_words(file_path, different_words) receives a file path and returns the number of words in the file.
    :param file_path: string
    :param different_words: boolean
    :return: the number of words in the file
    """
    with open(file_path, 'r') as file:
        text = file.read()
        words = nltk.word_tokenize(text)
        words = [word for word in words if word.isalpha()]
        if different_words:
            return len(set(words))
        return len(words)


def longest_and_shortest_words(file_path):
    """
    longest_and_shortest_words(file_path) receives a file path and returns the longest and shortest words in the file.
    if there are multiple words with the same length, return all of them.
    :param file_path: string
    :return: the longest and shortest words in the file
    """
    with open(file_path, 'r') as file:
        text = file.read()
        words = nltk.word_tokenize(text)
        words = [word.lower() for word in words]
        words = [word for word in words if word.isalpha()]
        words = set(words)
        words = list(words)
        words.sort(key=len)
        return words[0], words[-1]


def remove_diacritics(file_path):
    """
    remove_diacritics(file_path) receives a file path and returns the text from the file without diacritics.
    :param file_path: string
    :return: the text from the file without diacritics
    """
    with open(file_path, 'r') as file:
        text = file.read()
        return unidecode(text)


def synonyms(word):
    """
    synonyms(word) receives a word and returns its synonyms.
    :param word: string
    :return: the synonyms of the word
    """
    nlp = spacy.load("ro_core_news_sm")
    doc = nlp(word)
    wn = rwn.RoWordNet()
    synset_ids = wn.synsets(literal=doc[0].lemma_)
    rez = []
    for synset_id in synset_ids:
        synset = wn.synset(synset_id)
        rez.extend(synset.literals)
    # remove duplicates
    rez = list(set(rez))
    return rez


def ex3():
    # 1. Count the number of sentences from file data/texts.txt
    file_path = 'data/texts.txt'
    print('Number of sentences:', number_of_sentences(file_path))

    # 2. Count the number of words from file data/texts.txt
    print('Number of words:', number_of_words(file_path))

    # 3. Count the number of different words from file data/texts.txt
    print('Number of different words:', number_of_words(file_path, different_words=True))

    # 4. Show the longest and shortest word/words from file data/texts.txt
    shortest, longest = longest_and_shortest_words(file_path)
    print('Longest word:', longest)
    print('Shortest word:', shortest)

    # 5. Show the text from file data/texts.txt without diacritics
    print('Text without diacritics:', remove_diacritics(file_path))

    # 6. Show the synonyms of the longest word from file data/texts.txt
    print('Synonyms of the longest word:', synonyms(longest))
