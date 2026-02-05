import re

example = '"<a href="https://www.x-rates.com/graph/?from=USD&amp;to=GBP">0.738508</a>"'

#pattern = r';(to=GBP)">(\w+)</a>'
pattern = r'(to=\w+)">([\d.]+)</a>'
link = re.search(pattern, example)

if link:
    conversion_type = link.group(1)
    conversion = link.group(2)
    if conversion_type == "to=GBP":
        print(conversion_type)
        print(conversion)
else:
    print("Not found")