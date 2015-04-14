f = open('Puzzles/Medium','r')
x = []

for i in f:
	x = x + [i.strip('\n').split(',')]

print x

input("ptq")