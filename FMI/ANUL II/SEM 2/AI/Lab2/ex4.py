import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from PIL import Image
from scipy import stats
from sklearn.preprocessing import MinMaxScaler
import nltk
from nltk.tokenize import word_tokenize
from collections import Counter


def clipped_histogram(data, column=None, clip_min=None, clip_max=None):
    """
    clipped_histogram(data, column, clip_min=None, clip_max=None)
        Plot a histogram of the data from a column, after clipping the data
    :param data: DataFrame
    :param column: string
    :param clip_min: int
    :param clip_max: int
    :return: void
    """
    # Clip the data
    if column is None:
        rez = data.copy()
    else:
        rez = data[column].copy()
    if clip_min is not None:
        rez = rez.clip(lower=clip_min)
    if clip_max is not None:
        rez = rez.clip(upper=clip_max)
    # Plot the histogram
    plt.hist(rez, edgecolor='black')
    if column is None:
        plt.title('clipped')
    else:
        plt.title(column + ' clipped')
    plt.show()


def zscore_histogram(data, column=None):
    """
    zscore_histogram(data, column)
        Plot a histogram of the zscore of the data from a column
    :param data: DataFrame
    :param column: string
    :return: void
    """
    # Calculate the zscore
    if column is None:
        zscore = np.abs(stats.zscore(data))
    else:
        zscore = np.abs(stats.zscore(data[column]))
    # Plot the histogram
    plt.hist(zscore, edgecolor='black')
    if column is None:
        plt.title('zscore')
    else:
        plt.title(column + ' zscore')
    plt.show()


def min_max_histogram(data, column=None):
    """
    min_max_histogram(data, column)
        Plot a histogram of the min-max normalized data from a column
    :param data: DataFrame
    :param column: string
    :return: void
    """
    # Normalize the data
    if column is None:
        rez = (data - data.min()) / (data.max() - data.min())
    else:
        rez = (data[column] - data[column].min()) / (data[column].max() - data[column].min())
    # Plot the histogram
    plt.hist(rez, edgecolor='black')
    if column is None:
        plt.title('min-max')
    else:
        plt.title(column + ' min-max')
    plt.show()


def log_histogram(data, column=None):
    """
    log_histogram(data, column)
        Plot a histogram of the log normalized data from a column
    :param data: DataFrame
    :param column: string
    :return: void
    """
    # Normalize the data
    if column is None:
        rez = np.array(data) + 1e-6
    else:
        rez = np.array(data[column]) + 1e-6
    rez = np.log(rez)
    # Plot the histogram
    plt.hist(rez, edgecolor='black')
    if column is None:
        plt.title('log')
    else:
        plt.title(column + ' log')
    plt.show()


def pixels_histogram(image):
    """
    pixels_histogram(image)
        Plot a histogram of the pixels of an image
    :param image: string
    :return: void
    """
    # Plot the histogram
    im = Image.open(image)
    np_image = np.array(im)
    plt.hist(np_image.ravel(), density=True)
    plt.xlabel('Pixel value')
    plt.ylabel('relative frequency')
    plt.title(image)
    plt.show()


def clipped_histogram_image(image, clip_min=None, clip_max=None):
    """
    clipped_histogram_image(image, clip_min=None, clip_max=None)
        Plot a histogram of the pixels of an image, after clipping the data
    :param image: string
    :param clip_min: int
    :param clip_max: int
    :return: void
    """
    # Clip the data
    im = Image.open(image)
    np_image = np.array(im)
    if clip_min is not None:
        np_image = np_image.clip(min=clip_min)
    if clip_max is not None:
        np_image = np_image.clip(max=clip_max)
    # Plot the histogram
    plt.hist(np_image.ravel(), density=True, edgecolor='black')
    plt.xlabel('Pixel value')
    plt.ylabel('relative frequency')
    plt.title('Image ' + image + ' clipped')
    plt.show()


def zscore_histogram_image(image):
    """
    zscore_histogram_image(image)
        Plot a histogram of the zscore of the pixels of an image
    :param image: string
    :return: void
    """
    # Calculate the zscore
    im = Image.open(image)
    np_image = np.array(im)
    zscore = np.abs(stats.zscore(np_image))
    # Plot the histogram
    plt.hist(zscore.ravel(), density=True, edgecolor='black')
    plt.xlabel('Pixel value')
    plt.ylabel('relative frequency')
    plt.title('Image ' + image + ' zscore')
    plt.show()


def min_max_histogram_image(image):
    """
    min_max_histogram_image(image)
        Plot a histogram of the min-max normalized pixels of an image
    :param image: string
    :return: void
    """
    # Normalize the data
    im = Image.open(image)
    np_image = np.array(im)
    rez = (np_image - np_image.min()) / (np_image.max() - np_image.min())
    # Plot the histogram
    plt.hist(rez.ravel(), density=True, edgecolor='black')
    plt.xlabel('Pixel value')
    plt.ylabel('relative frequency')
    plt.title('Image ' + image + ' min-max')
    plt.show()


def log_histogram_image(image):
    """
    log_histogram_image(image)
        Plot a histogram of the log normalized pixels of an image
    :param image: string
    :return: void
    """
    # Normalize the data
    im = Image.open(image)
    np_image = np.array(im) + 1e-6
    rez = np.log(np_image)
    # Plot the histogram
    plt.hist(rez.ravel(), density=True, edgecolor='black')
    plt.xlabel('Pixel value')
    plt.ylabel('relative frequency')
    plt.title('Image ' + image + ' log')
    plt.show()


def ex4():
    # 1. Normalize the data from data/employees.csv
    # Read the data
    data = pd.read_csv('data/employees.csv')
    for column in data.columns:
        if data[column].dtype == 'float64' or data[column].dtype == 'int64':
            data[column] = data[column].fillna(data[column].mean())
        else:
            # Fill the missing values with the most frequent value for non-numerical columns
            data[column] = data[column].fillna(data[column].value_counts().idxmax())
    # Plot the histograms
    # - by clipping
    clipped_histogram(data, 'Salary', clip_min=37000, clip_max=147000)
    clipped_histogram(data, 'Bonus %', clip_min=1.5, clip_max=19)
    # - by z-score
    zscore_histogram(data, 'Salary')
    zscore_histogram(data, 'Bonus %')
    # - by min-max
    min_max_histogram(data, 'Salary')
    min_max_histogram(data, 'Bonus %')
    # - by log
    log_histogram(data, 'Salary')
    log_histogram(data, 'Bonus %')

    # for 'Team' column
    team_counts = data['Team'].value_counts()

    # - by zscore
    zscore = np.abs(stats.zscore(team_counts))
    plt.bar(team_counts.index, zscore)
    plt.title('Z-score Normalized Number of Employees in Each Team')
    plt.xlabel('Team')
    plt.ylabel('Z-score Normalized Number of Employees')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()
    # - by min-max
    scaler = MinMaxScaler()
    team_counts_scaled = scaler.fit_transform(team_counts.values.reshape(-1, 1))
    plt.bar(team_counts.index, team_counts_scaled.flatten())
    plt.title('Normalized Number of Employees in Each Team (Min-Max Scaling)')
    plt.xlabel('Team')
    plt.ylabel('Normalized Number of Employees')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()
    # - by log
    team_counts_log = np.log(team_counts)
    plt.bar(team_counts.index, team_counts_log)
    plt.title('Log Normalized Number of Employees in Each Team')
    plt.xlabel('Team')
    plt.ylabel('Log Normalized Number of Employees')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

    # 2. Normalize the values of the pixels of the images from data/images
    images = [image for image in os.listdir('data/images')]
    for image in images:
        pixels_histogram('data/images/' + image)
    # - by clipping
    clipped_histogram_image('data/images/diffusionModel.jpg', clip_min=250, clip_max=255)
    # - by z-score
    zscore_histogram_image('data/images/diffusionModel.jpg')
    # - by min-max
    min_max_histogram_image('data/images/diffusionModel.jpg')
    # - by log
    log_histogram_image('data/images/diffusionModel.jpg')

    # # for all images
    # # save the pixels of all images in a list
    # pixels = []
    # for image in images:
    #     im = Image.open('data/images/' + image)
    #     np_image = np.array(im)
    #     pixels.extend(np_image.ravel())
    #
    # pixels = np.array(pixels)
    # plt.hist(pixels, density=True, edgecolor='black')
    # plt.xlabel('Pixel value')
    # plt.ylabel('relative frequency')
    # plt.title('All images')
    # plt.show()
    # # - by clipping
    # plt.hist(pixels.clip(min=200, max=255), density=True, edgecolor='black')
    # plt.xlabel('Pixel value')
    # plt.ylabel('relative frequency')
    # plt.title('All images clipped')
    # plt.show()
    # # - by z-score
    # zscore_histogram(pixels)
    # # - by min-max
    # min_max_histogram(pixels)
    # # - by log
    # log_histogram(pixels)

    # 3. Normalize the number of appearences of the words at level of the sentences from data/texts.txt
    # Read the data
    with open('data/texts.txt', 'r') as file:
        text = file.read()
    # Tokenize the sentences

    romanian_sentences = nltk.sent_tokenize(text)

    # Tokenize the sentences into words
    tokenized_sentences = [word_tokenize(sentence.lower()) for sentence in romanian_sentences]
    tokenized_sentences = [[word for word in tokens if word.isalpha() and len(word) > 3] for tokens in tokenized_sentences]

    # Count the occurrences of each word in each sentence
    word_counts_per_sentence = [Counter(tokens) for tokens in tokenized_sentences]

    # Normalize the counts within each sentence
    normalized_word_counts_per_sentence = []
    for counts in word_counts_per_sentence:
        total_count = sum(counts.values())
        normalized_counts = {word: count / total_count for word, count in counts.items()}
        normalized_word_counts_per_sentence.append(normalized_counts)

    # Plot the distribution of word frequencies across sentences
    plt.figure(figsize=(12, 6))
    for i, normalized_counts in enumerate(normalized_word_counts_per_sentence):
        words, frequencies = zip(*normalized_counts.items())
        plt.bar(words, frequencies, alpha=0.5, label=f"Sentence {i + 1}")

    plt.xlabel('Word')
    plt.ylabel('Frequency')
    plt.title('Normalized Word Frequencies Across Sentences')
    plt.legend()
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()
