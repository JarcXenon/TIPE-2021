from sheets import values

n = len(values[0])
m = n//2
condorcet = []
appreciation = []

choix = values.pop(0)
choix = choix[:m]

for k in values:
    condorcet.append(k[m:])
    appreciation.append(k[:m])

def doublon(tab):
    for i in range(1, 9):
        if tab.count(i) != 1:
            return True
    return False

k = 0
s = 0

while k < len(condorcet):
    for i in range(8):
        condorcet[k][i] = int(condorcet[k][i])
    if doublon(condorcet[k]):
        condorcet.pop(k)
        appreciation.pop(s)
    else:
        k+=1
    s += 1
    
appreciations_vote = ["Nul", "Insuffisant", "Passable", "Assez bien", "Bien",
                      "Excellent"]
choix[3] ="""Deux patates dans un four, la première dit 'Purée il fait chaud',
l'autre répond 'Oh mon dieu, une patate qui parle !!'"""

for k in appreciation:
    for i in range(8):
        k[i] = appreciations_vote.index(k[i]) + 1

with open('condorcet.csv', 'w') as f:
    f.writelines(['"'+i+'"' + ';' for i in choix])
    f.write('\n')
    f.writelines([str(i)[1:-1]+'\n' for i in condorcet])

with open('appreciation.csv', 'w') as f:
    f.writelines(['"'+i+'"' + ';' for i in choix])
    f.write('\n')
    f.writelines([str(i)[1:-1]+'\n' for i in appreciation])