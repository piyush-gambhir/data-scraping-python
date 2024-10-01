import re


def vin_validator(vin):
    pattern = re.compile(r'^[A-HJ-NPR-Z0-9]{17}$')
    return pattern.match(vin) is not None
