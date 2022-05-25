"""Tests for the Patient model."""
from inflammation.models import Patient, Doctor


def test_create_patient():
    name = 'Alice'
    p = Patient(name=name)
    assert p.name == name


def test_add_patient_obervation():
    name = 'Alice'
    p = Patient(name=name)
    p.add_observation(5)
    assert len(p.observations) == 1
    obs = p.observations[0]
    assert obs.day == 0
    assert obs.value == 5


def test_add_patient_obervation_with_day():
    name = 'Alice'
    p = Patient(name=name)
    days = [0, 1, 2]
    values = [5, 4, 3]
    for day, value in zip(days, values):
        p.add_observation(value, day=day)
    assert len(p.observations) == len(days)
    for i, obs in enumerate(p.observations):
        assert obs.day == days[i]
        assert obs.value == values[i]


def test_create_doctor():
    name = 'Dr. Alice'
    d = Doctor(name=name)
    assert d.name == name


def test_add_patients_to_doctor():
    name = 'Dr. House'
    d = Doctor(name=name)
    name = 'Alice'
    p = Patient(name=name)
    d.add_patient(p)
    assert len(d.patients) == 1
    doctors_patient = d.patients[0]
    assert doctors_patient.name == p.name
    assert doctors_patient.observations == p.observations


def test_average_observations_over_patients():
    name = 'Dr. House'
    d = Doctor(name=name)
    patient_names = ['alice', 'bob', 'sam']
    days = [0, 1, 2]
    values = [5, 4, 3]
    for name in patient_names:
        p = Patient(name=name)
        for day, value in zip(days, values):
            p.add_observation(value, day=day)
        d.add_patient(p)
    avg_obs = d.average_observations_over_patients()
    assert len(avg_obs) == 3
    for i, obs in enumerate(avg_obs):
        assert obs.day == days[i]
        assert obs.value == values[i]



