import re

m = re.search("(?P<year>\d{4})","output_1984_2016_3205.text")

print(m.group("year"))
