import automaton

operator = list(("+", ".", "*", "(", ")"))

def parenthese(i, liste, plus_bool):

	new_liste = list(liste)
	ll = list()

	if (i-1) >= 0:
		l = list('.')
	else:
		l = list()

	j=k=i
	compt = 0
	for j in range(i, len(new_liste)):
		if new_liste[j] == '(':
			compt += 1
		if new_liste[j] == ')':
			while compt !=0 :
				if new_liste[j] == ')':
					compt -= 1

			break

	for k in  range(i, j-1):
		ll.append(new_liste[k+1])

	for k in range(i, j+1) :
		new_liste.pop(i)

	if i-1>=0:
		left = new_liste.pop(i-1)
		l.append(left)

	result_analyse = analyse(ll, plus_bool
)
	l.append(result_analyse[0])

	new_liste.insert(i-1, l[0])
	return new_liste

def analyse_plus(i, liste, plus_bool):	
	new_liste = list(liste)

	if plus_bool == False:

		compt = 0
		while new_liste[compt] != '+' or compt == len(liste):
			compt+=1
		compt+=1

		l = list([new_liste.pop(i)])
		i-=1
		
		left = new_liste.pop(i)
		
		result_analyse = analyse(new_liste, True)
		plus_bool = False

		l.append(left)
		l.append(result_analyse[0])
		
		for j in range(i, compt):
			new_liste.pop(i)

		new_liste.insert(i, l)
		return new_liste
	
	else:
		return (new_liste.pop(i-1))

def analyse_dot(i, liste, plus_bool):
	new_liste = list(liste)

	l = list([new_liste.pop(i)])
	i-=1
	left = new_liste.pop(i)
	result_analyse = analyse(new_liste, plus_bool
)
	l.append(left)
	l.append(result_analyse[0])
	i-=1
	new_liste.insert(i, l)
	return new_liste

def analyse_character(i, liste):
	new_liste = list(liste)
	if not operator.count(new_liste[i-1]):
		l = list(".")
		l.append(new_liste.pop(i-1))
		l.append(new_liste.pop(i-1))
		i-=1
		new_liste.insert(i, l)
	return new_liste

def analyse(liste, plus_bool):

	i=0
	while len(liste) != 1:
		if i >= len(liste) and len(liste)==2:
			i-=1
		if operator.count(liste[i]):
			
			if liste[i] == '*':
				i-=1
				liste.insert(i, [liste.pop(i+1), liste.pop(i)])

			elif liste[i] == '+' :
				liste = analyse_plus(i, liste, plus_bool
			)

			elif liste[i] == '.':
				liste = analyse_dot(i, liste, plus_bool
			)

			elif liste[i] == '(':
				liste = parenthese(i, liste, plus_bool
			)

		else:

			if i> 0 and liste[i-1] != None:
				if (i+1) <= len(liste)-1 :
					if liste[i+1] != '*':
						liste = analyse_character(i, liste)
				else:
					liste = analyse_character(i, liste)
		i+=1
		

	return liste