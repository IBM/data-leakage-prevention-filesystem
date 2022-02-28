from dlpfs.transformation import compile_transformation
from faker import Faker
from datetime import datetime

import random

import pytest


def test_redact():
    transformation = compile_transformation({"type": "redact"})

    faker = Faker()

    for value in [faker.pricetag() for _ in range(100)]:
        transformed = transformation(value)

        assert value != transformed


def test_redact_customize_character():
    transformation = compile_transformation({"type": "redact", "char": "X"})

    transformed = transformation("123456789")

    assert transformed == "XXXXXXXXX"


def test_dp():
    # DP defaults to Laplacian mechanism with e=0.1 and d=0.0
    dp_transformation = compile_transformation({'type': 'dp'})

    faker = Faker()

    for value in [str(faker.pricetag()[1:]).replace(",", "") for _ in range(100)]:
        transformed = dp_transformation(str(value))

        assert value != transformed


def test_dp_laplace():
    laplacian_tranformation = compile_transformation({'type': 'dp', 'mech': 'Laplace', 'e': 8, 'd': 0})

    faker = Faker()

    for value in [str(faker.pricetag()[1:]).replace(",", "") for _ in range(100)]:
        transformed = laplacian_tranformation(str(value))

        assert value != transformed


def test_dp_binary():
    binary_transformation = compile_transformation({'type': 'dp', 'mech': 'Binary', 'e': 0.1, 'true': str(True), 'false': str(False)})

    flip_count = 0
    for value in [str(bool(random.randrange(0, 1))) for _ in range(1000)]:
        transformed = binary_transformation(str(value))

        flip_count += 1 if value != transformed else 0

    assert flip_count


def test_dp_gaussian():
    gaussian_transformation = compile_transformation({"type": "dp", "mech": "Gaussian", "e": 0.1, "d": 0.1})

    faker = Faker()

    for value in [str(faker.pricetag()[1:]).replace(",", "") for _ in range(100)]:
        transformed = gaussian_transformation(str(value))

        assert value != transformed


@pytest.mark.skip("Needs to be discussed to better understand the usage of the exponential mechanism")
def test_dp_exponential():
    candidates = [f"candidate {i}" for i in range(20)]
    exponential_transformation = compile_transformation({"type": "dp", "mech": "Exponential", "candidates": candidates, "utility": [1 for _ in candidates]})

    for value in [random.choice(candidates) for _ in range(100)]:
        transformed = exponential_transformation(str(value))

        assert value != transformed


def test_none():
    no_transformation = compile_transformation({'type': 'none'})

    faker = Faker()

    for value in [faker.pricetag() for _ in range(100)]:
        transformed = no_transformation(str(value))

        assert value == transformed


@pytest.mark.skip("Benchmark test needs to be explicitly invoked")
def test_benchmark():
    faker = Faker()

    none = compile_transformation({'type': 'none'})
    redact = compile_transformation({'type': 'redact'})
    dp = compile_transformation({'type': 'dp', 'mech': 'Laplace', 'e': 8, 'd': 0})

    values = [faker.pricetag()[1:].replace(',', '') for _ in range(20000)]

    def randomize(c: str) -> str:
        if c == ".":
            return c
        return str(random.randint(0, 9))

    def mask(x: str) -> str:
        return ''.join([
            randomize(c) for c in x[:]
        ])

    for i in range(30):
        start = datetime.now()
        for value in values:
            _ = none(value)
        end = datetime.now()

        print(f'none {i} {(end-start).microseconds/1000}')

        start = datetime.now()
        for value in values:
            _ = redact(value)
        end = datetime.now()

        print(f'redact {i} {(end-start).microseconds/1000}')

        start = datetime.now()
        for value in values:
            _ = dp(value)
        end = datetime.now()

        print(f'dp {i} {(end-start).microseconds/1000}')

        start = datetime.now()
        for value in values:
            _ = mask(value)
        end = datetime.now()

        print(f'mask {i} {(end-start).microseconds/1000}')
