#!/usr/bin/env python3

from datetime import datetime

expiration_timestamp = 1700132064
expiration_datetime = datetime.utcfromtimestamp(expiration_timestamp)

print("Token expiration time:", expiration_datetime)
