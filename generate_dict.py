import enchant
d = enchant.Dict("en_US")
alphabet = "abcdefghijklmnopqrstuvwxyz"
valid = []

for i in alphabet:
    print(i)
    for j in alphabet:
        for k in alphabet:
            for q in alphabet:
                for p in alphabet:
                    word = f"{i}{j}{k}{q}{p}"
                    if d.check(word):
                        valid.append(word)

with open("dictionary.txt", 'w') as fh:
    for word in valid:
        fh.write(word + ",\n")