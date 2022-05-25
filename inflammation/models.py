"""Module containing models representing patients and their data.

The Model layer is responsible for the 'business logic' part of the software.

Patients' data is held in an inflammation table (2D array) where each row contains 
inflammation data for a single patient taken over a number of days 
and each column represents a single day across all patients.
"""

import numpy as np


def load_csv(filename):
    """Load a Numpy array from a CSV

    :param filename: Filename of CSV to load
    """
    return np.loadtxt(fname=filename, delimiter=',')


def daily_mean(data):
    """Calculate the daily mean of a 2D inflammation data array.

    :param data: 2D numpy data array with inflammation data
                (each row contains measurements for a single patient across all days).
    :returns: An array of mean values of measurements for each day.

    """
    return np.mean(data, axis=0)


def daily_max(data):
    """Calculate the daily max of a 2D inflammation data array.
        :param data: 2D numpy data array with inflammation data
                (each row contains measurements for a single patient across all days).
        :returns: An array of max values of measurements for each day.
    """
    return np.max(data, axis=0)


def daily_min(data):
    """Calculate the daily min of a 2D inflammation data array.
        :param data: 2D numpy data array with inflammation data
                (each row contains measurements for a single patient across all days).
        :returns: An array of min values of measurements for each day.
    """
    return np.min(data, axis=0)


def patient_normalise(data):
    """
    Normalise patient data from a 2D inflammation data array.

    NaN values are ignored, and normalised to 0.

    Negative values are rounded to 0.
    """
    if not isinstance(data, np.ndarray):
        raise TypeError('data input should be ndarray')
    if len(data.shape) != 2:
        raise ValueError('inflammation array should be 2-dimensional')
    if np.any(data < 0):
        raise ValueError('inflammation values should be non-negative')
    maxima = np.nanmax(data, axis=1)
    with np.errstate(invalid='ignore', divide='ignore'):
        normalised = data / maxima[:, np.newaxis]
    normalised[np.isnan(normalised)] = 0
    normalised[normalised < 0] = 0
    return normalised


def attach_names(data, names):
    """Create datastructure containing patient records."""
    if len(data) != len(names):
        raise ValueError("different numbers of names and datasets")
    named_data = []
    for name, patient_data in zip(names, data):
        entry = {"name": name, "data": patient_data}
        named_data.append(entry)
    return named_data


class Observation:
    def __init__(self, day, value):
        self.day = day
        self.value = value

    def __str__(self):
        return str(self.value)

    def __eq__(self, obj):
        assert isinstance(obj, Observation)
        return  obj.day == self.day and obj.value == self.value


class Person:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name


class Patient(Person):
    def __init__(self, name, observations=None):
        super().__init__(name)
        self.observations = []
        if observations is not None:
            self.observations = observations

    def __eq__(self, obj):
        assert isinstance(obj, Patient)
        return self.name == obj.name and self.observations == obj.observations

    def add_observation(self, value, day=None):
        if day is None:
            try:
                day = self.observations[-1]['day'] + 1
            except IndexError:
                day = 0
        new_observation = Observation(day, value)
        self.observations.append(new_observation)
        return new_observation

    @property
    def last_observation(self):
        return self.observations[-1]


class Doctor(Person):
    def __init__(self, name):
        super().__init__(name)
        # list of patient objects? or just a list of keys (names) ?
        self.patients = []

    # add existing objects or create new ones?
    def add_patient(self, patient):
        self.patients.append(patient)

    def average_observations_over_patients(self):
        means = {}
        sums = {}
        ns = {}
        for patient in self.patients:
            for obs in patient.observations:
                if obs.day in sums:
                    sums[obs.day] += obs.value
                    ns[obs.day] += 1
                else:
                    sums[obs.day] = obs.value
                    ns[obs.day] = 1
        for day in sums:
            means[day] = sums[day] / ns[day]
        return [Observation(k, v) for k, v in means.items()]


class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author

    def __str__(self):
        return "%s by %s" % (self.title, self.author)


class Library:
    def __init__(self):
        self.books = []

    def add_book(self, title, author):
        self.books.append(Book(title, author))

    def __len__(self):
        return len(self.books)

    def __getitem__(self, key):
        return self.books[key]

    def by_author(self, author):
        results = [book for book in self.books if book.author == author]
        if results == []:
            raise KeyError("author does not exist in library")
        return results

    @property
    def titles(self):
        return [book.title for book in self.books]

    @property
    def authors(self):
        authors = {book.author for book in self.books}
        return list(authors)
