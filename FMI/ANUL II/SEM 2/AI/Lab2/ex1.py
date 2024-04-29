import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
import numpy as np


def ex1():
    # Load the data from data/employes.csv
    data = pd.read_csv('data/employees.csv')

    # I
    # 1. Print the number of employees
    print('Number of employees:', len(data))

    # 2. Print the number and the type of information about the employees
    print('Number of information:', len(data.columns))
    print('Type of information:', data.dtypes)

    # 3. Print the number of employees which all data is complete
    complete_data = data.dropna()
    print('Number of employees with complete data:', len(complete_data))

    # 4. Print the minimum, maximum and average values for each column
    # if the column is not numerical, show the most and the least frequent values
    print('Minimum, maximum and average values for each column:')
    for column in data.columns:
        if data[column].dtype == 'float64' or data[column].dtype == 'int64':
            print(column, ":", "min =", data[column].min(), "max =", data[column].max(), "mean =", data[column].mean())
        else:
            print(column, ":", "most frequent value =", data[column].value_counts().idxmax(),
                  "least frequent value =", data[column].value_counts().idxmin())

    # 5. For the non-numerical columns, print the number of possible values for each column
    print('Number of possible values for each column:')
    for column in data.columns:
        if data[column].dtype != 'int64' and data[column].dtype != 'float64':
            print(column, ":", len(data[column].unique()))

    # 6. Verify if there are missing values in the data
    print('Missing values:', data.isnull().values.any())
    # Solve the missing values
    # a. Drop the rows with missing values
    solved_data = data.copy()
    # Test if there are missing values
    assert solved_data.isnull().values.any()
    solved_data = solved_data.dropna()
    # Test if there are missing values
    assert not solved_data.isnull().values.any()
    # b. Fill the missing values with the average value for numerical columns and the most
    # frequent value for non-numerical columns
    # Fill the missing values with the average value for numerical columns
    for column in data.columns:
        if data[column].dtype == 'float64' or data[column].dtype == 'int64':
            data[column] = data[column].fillna(data[column].mean())
        else:
            # Fill the missing values with the most frequent value for non-numerical columns
            data[column] = data[column].fillna(data[column].value_counts().idxmax())
    # Test if there are missing values
    assert not data.isnull().values.any()
    print("The missing values were solved!")

    # II
    # 1. Show the distribution of the salaries of the employees in a histogram by salary categories
    # Show the histogram
    show_histogram(data['Salary'],  None, 'Salaries of the employees', 'Salary', 'Number of employees')

    # 2. Show the distribution of the salaries of the employees in a histogram by salary categories and team in which
    # they work
    # Show the histogram
    show_histogram([data[data['Team'] == team]['Salary'] for team in data['Team'].unique()],
                   data['Team'].unique(), 'Salaries of the employees by team', 'Salary', 'Number of employees', bins=10)
    # 3. Show the employees which can be considered outliers in the
    # - salary distribution
    # Calculate the z-score for the salaries
    z_scores = np.abs(stats.zscore(data['Salary']))
    # Show the employees which can be considered outliers
    outliers = data[z_scores > 1.7]
    outliers['Salary'].plot(kind='hist', edgecolor='black', title='Outliers for salary', xlabel='Salary', ylabel='Number of employees')
    plt.show()
    # - bonus distribution
    # Calculate the z-score for the bonuses
    z_scores = np.abs(stats.zscore(data['Bonus %']))
    # Show the employees which can be considered outliers
    outliers = data[z_scores > 1.7]
    outliers['Bonus %'].plot(kind='hist', edgecolor='black', title='Outliers for bonus', xlabel='Bonus', ylabel='Number of employees')
    plt.show()
    # - outliers for salaries of the employees by team distribution
    # employees_teams = [data[data['Team'] == team]['Salary'] for team in data['Team'].unique()]
    # plt.hist(employees_teams, label=data['Team'].unique(), edgecolor='black', bins=10)
    # plt.legend()
    # for i, team_salaries in enumerate(employees_teams):
    #     q1 = np.percentile(team_salaries, 25)
    #     q3 = np.percentile(team_salaries, 75)
    #     iqr = q3 - q1
    #     lower_bound = q1 - 1.5 * iqr
    #     upper_bound = q3 + 1.5 * iqr
    #
    #     outliers = [salary for salary in team_salaries if salary < lower_bound or salary > upper_bound]
    #     if outliers:
    #         plt.scatter([data['Team'].unique()[i]] * len(outliers), outliers, color='black', marker='o', label='Outliers')
    #
    # plt.show()


def show_histogram(data, label, title, xlabel, ylabel, bins=10):
    """
    show_histogram(data, label, title, xlabel, ylabel, bins)
        Show the histogram of the data with the specified bins, label, title, xlabel, ylabel and bins
    :param data: dataframe
    :param label: list of string
    :param title: string
    :param xlabel: string
    :param ylabel: string
    :param bins: int
    :return: void
    """
    # Create the histogram
    if label is None:
        plt.hist(data, edgecolor='black', bins=bins)
    else:
        plt.hist(data, label=label, edgecolor='black', bins=bins)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    if label is not None:
        plt.legend()
    plt.show()
