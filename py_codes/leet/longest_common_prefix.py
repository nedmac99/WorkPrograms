strs = ["charge", "change", "chain", "chasm"]




#Correct solution using AI
'''
prefix = ""

for chars in zip(*strs):
    if all(char == chars[0] for char in chars):
        prefix += chars[0]
    else:
        break

print(prefix)
'''

'''
def longest_common_prefix(strs: List[str]) -> str:
    ...
'''