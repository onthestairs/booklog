import re

def strip_non_numeric(str):
	non_decimal = re.compile(r'[^\d.]+')
	return non_decimal.sub('', str)