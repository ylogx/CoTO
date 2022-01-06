from collections import namedtuple

HealthInfo = namedtuple("HealthInfo", "hc_num, hc_suffix, hc_back, dob, postal_code, email, phone")


def get_data() -> HealthInfo:
    return HealthInfo(
        '',
        '',
        '',
        '',
        '',
        'shubham@chaudhary.xyz',
        ''
    )
