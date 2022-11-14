
data = {
    'a': 1,
}

print(data.get('a'))
print(data.get('a', 2))
print(data.get('b', 3))
print(data.get(None, 4))
print(data.get(None))
print(data)


