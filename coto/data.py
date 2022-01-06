import os
from collections import namedtuple

HealthInfo = namedtuple("HealthInfo", "hc_num, hc_suffix, hc_back, dob, postal_code, email, phone")


def get_data() -> HealthInfo:
    from dotenv import load_dotenv

    load_dotenv()  # take environment variables from .env
    return HealthInfo(
        os.getenv('hc_num'),
        os.getenv('hc_suffix'),
        os.getenv('hc_back'),
        os.getenv('dob'),
        os.getenv('postal_code'),
        os.getenv('email'),
        os.getenv('phone'),
    )
