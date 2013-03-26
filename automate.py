import automaton

operator = list(("+", ".", "*", "(", ")"))

def completer(aut):
	"Complete un automate non complet et ne modifie pas un automate complet"

	aut_complet = aut.clone()
	
	puit = (aut_complet.get_maximal_id()+1)
	
	alpha = list( aut_complet.get_alphabet() )
	states = list( aut_complet.get_states() )
	
	for i in range( len( alpha ) ):
		for j in range( len( states ) ):
			if not aut_complet.delta( alpha[i], [states[j]] ):
				if not alpha[len(alpha)-1] == puit:
						aut_complet.add_state(puit)
				aut_complet.add_transition( (states[j], alpha[i], puit) )


	for i in alpha:
		aut_complet.add_transition((puit, i, puit))


	return aut_complet


def uninter(aut1, aut2, type):

	alpha = list( aut1.get_alphabet() )

	aut = automaton.automaton ( 
		alphabet = alpha,
		epsilons = [ '0 '],
	)

	states1 = list( aut1.get_states() )	
	states2 = list( aut2.get_states() )
	transitions1 = list( aut1.get_transitions() )
	transitions2 = list( aut2.get_transitions() )
	
	for i in range (len (alpha) ):
		for j in range (len (states1) ):
			for k in range (len (states2) ):
				tmp1 = list( aut1.delta( alpha[i], [states1[j]]) )
				tmp2 = list( aut2.delta( alpha[i], [states2[k]]) )
				if tmp1 and tmp2 :
					for l in range (len (tmp1)):
						for m in range (len (tmp2)):
							if not aut.has_state( (states1[j], states2[k]) ):
								aut.add_state((states1[j], states2[k]))

							if type > 0:
								if aut1.state_is_final((states1[j])) or aut2.state_is_final((states2[k])):
									aut.add_final_state((states1[j], states2[k]))
							else :
								if aut1.state_is_final((states1[j])) and aut2.state_is_final((states2[k])):
									aut.add_final_state((states1[j], states2[k]))

							if aut1.state_is_initial((states1[j])) and aut2.state_is_initial((states2[k])):	
								aut.add_initial_state((states1[j], states2[k]))
							aut.add_transition( ((states1[j],states2[k]), alpha[i], (tmp1[l], tmp2[l]) ))
	return aut
	

def union(aut1, aut2):

	aut_union = uninter(aut1, aut2, 1)
	return aut_union

def intersection(aut1, aut2):

	aut_inter = uninter(aut1, aut2, 0)
	return aut_inter

def miroir(aut):
	i = 0
	new_transitions = []
	transitions = list(aut.get_transitions())

	while i < len(transitions):
		new_transitions.append((transitions[i][2], transitions[i][1], transitions[i][0]))
		i+=1

	aut_mirror = automaton.automaton (
		alphabet = aut.get_alphabet(),
		epsilons = aut.get_epsilons(),
		states = aut.get_states() , initials = aut.get_final_states() , finals = aut.get_initial_states(),
		transitions = new_transitions
	)

	return aut_mirror

def determinisation(aut):
	alphabet = list(aut.get_alphabet())
	initials_states = aut.get_initial_states()
	final_states = aut.get_final_states()

	file_sommet = [initials_states]
	liste_nouveaux_sommet = [initials_states]

	liste_transitions = []

	while len(file_sommet) != 0:
		for i in alphabet:
			if aut.delta(i, file_sommet[0]):
				sommet = aut.delta(i, file_sommet[0])
				liste_transitions += [(file_sommet[0], i, sommet)]
				if not sommet in liste_nouveaux_sommet:
					liste_nouveaux_sommet += [sommet]
					file_sommet += [sommet]
		file_sommet.pop(0)


	final = []
	for i in liste_nouveaux_sommet:
		for j in i:
			if j in final_states:
				final += [i]



	aut_deter = automaton.automaton (
		initials = [initials_states],
		finals = final,
		alphabet = alphabet,
		epsilons = aut.get_epsilons(),
		states = liste_nouveaux_sommet,
		transitions = liste_transitions
		)

	
	return aut_deter

def complement(aut):
	aut_complet = completer(aut)
	aut_deter = determinisation(aut_complet)
	
	states = aut_deter.get_states()
	finals_states = [] 

	for i in states:
		if not aut_deter.state_is_final(i):
			finals_states.append(i)

	
	aut_compl = automaton.automaton (
		initials = aut_deter.get_initial_states(),
		finals = finals_states,
		alphabet = aut_deter.get_alphabet(),
		epsilons = aut_deter.get_epsilons(),
		states = aut_deter.get_states(),
		transitions = aut_deter.get_transitions()
		)

	return aut_compl

def minimiser(aut):
	aut_min = miroir(aut)
	aut_min = determinisation(aut_min)
	aut_min = miroir(aut_min)
	aut_min = determinisation(aut_min)
	return aut_min

def expression_vers_automate(E):

	liste = list ()
	get_expression(E, liste)

	aut = automaton.automaton (
			epsilons = ['0']
		)

	alphabet = list()
	states = list()
	
	while len(liste) > 0 :
		cmpt = liste.pop()
		if not operator.count(cmpt):
			alphabet.append(cmpt)
			if not aut.get_maximal_id():
				i=0
			else:
				i = aut.get_maximal_id() 
				i+=1
			j=i+1	
			aut.add_transition( (i, cmpt, j) )
			states.append([i, j])
		else : 
			if cmpt == "+":
				states.append( plus(aut, states.pop(), states.pop()) )
			if cmpt == ".":
				states.append( produit(aut, states.pop(), states.pop()) )
			if cmpt == "*":
				states.append( star(aut, states.pop()) )

	aut = automaton.automaton(
		alphabet = alphabet,
		epsilons = ['0'],
		states = aut.get_states(), initials = aut.get_initial_states(), finals = aut.get_final_states(),
		transitions = aut.get_transitions()
	)

	return minimiser(aut)


def get_expression(E, liste):
	l = E
	while len(l) > 1:
		liste.append( l.pop(0))
		if len (l) > 0:
			get_expression(l.pop(0), liste )
			if len (l) > 0:
				get_expression(l.pop(0), liste )
	if len (l) > 0:
		liste.append( l[0] )


def	plus(aut, state1, state2):
	i = aut.get_maximal_id()
	i+=1
	aut.add_initial_state(i)
	j = aut.get_maximal_id()
	j+=1
	aut.add_final_state(j)
	
	aut.add_transitions([(i, '0', state1[0]), (state1[1], '0', j)])
	aut.add_transitions([(i, '0', state2[0]), (state2[1], '0', j)])

	return ([i, j])


def	produit(aut, state1, state2):
	i = aut.get_maximal_id()
	i+=1
	aut.add_initial_state(i)
	j = aut.get_maximal_id()
	j+=1
	aut.add_final_state(j)

	aut.add_transitions([(i, '0', state1[0]) , (state1[1], '0', state2[0]), (state2[1], '0', j)])
	
	return ([i, j])


def	star(aut, state):
	i = aut.get_maximal_id()
	i+=1
	aut.add_initial_state(i)
	j = aut.get_maximal_id()
	j+=1
	aut.add_final_state(j)

	aut.add_transitions([(i, '0', state[0]), (state[1], '0', j) , (state[1], '0', state[0]), (i, '0', j) ])

	return ([i, j])


"Un au choix = analyseur d'expression"

def analyseur(chaine):

	liste = list(chaine)

	liste = analyse(liste, False)

	return liste[0]

def parenthese(i, liste, test):

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

	result_analyse = analyse(ll, test)
	l.append(result_analyse[0])

	new_liste.insert(i-1, l[0])
	return new_liste

def analyse_plus(i, liste, test):	
	new_liste = list(liste)

	if test == False:

		compt = 0
		while new_liste[compt] != '+' or compt == len(liste):
			compt+=1
		compt+=1

		l = list([new_liste.pop(i)])
		i-=1
		
		left = new_liste.pop(i)
		
		result_analyse = analyse(new_liste, True)
		test = False

		l.append(left)
		l.append(result_analyse[0])
		
		for j in range(i, compt):
			new_liste.pop(i)

		new_liste.insert(i, l)
		return new_liste
	
	else:
		return (new_liste.pop(i-1))

def analyse_dot(i, liste, test):
	new_liste = list(liste)

	l = list([new_liste.pop(i)])
	i-=1
	left = new_liste.pop(i)
	result_analyse = analyse(new_liste, test)
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

def analyse(liste, test):

	i=0
	while len(liste) != 1:
		if i >= len(liste) and len(liste)==2:
			i-=1
		if operator.count(liste[i]):
			
			if liste[i] == '*':
				i-=1
				liste.insert(i, [liste.pop(i+1), liste.pop(i)])

			elif liste[i] == '+' :
				liste = analyse_plus(i, liste, test)

			elif liste[i] == '.':
				liste = analyse_dot(i, liste, test)

			elif liste[i] == '(':
				liste = parenthese(i, liste, test)

		else:

			if i> 0 and liste[i-1] != None:
				if (i+1) <= len(liste)-1 :
					if liste[i+1] != '*':
						liste = analyse_character(i, liste)
				else:
					liste = analyse_character(i, liste)
		i+=1
		

	return liste



def main():
	# aut1 = automaton.automaton (
	# 	alphabet = ['a', 'b', 'c'],
	# 	states = [2] , initials = [1] , finals = [2],
	# 	transitions = [(1 , 'a' ,1) , (1 , 'b' ,1) , (1 , 'c' ,2) , (2 , 'a' ,2) , (2 , 'b' ,2) , (2 , 'c' ,2)]
	# )

	# aut2 = automaton.automaton (
	# 	alphabet = ['a', 'b', 'c'],
	# 	states = [3] , initials = [1] , finals = [3],
	# 	transitions = [(1 , 'a' ,1) , (1 , 'c' ,1) , (1 , 'b' ,2) , (2 , 'a' ,3) , (2 , 'b' ,2) , (2 , 'c' ,1),
	# 		(3 , 'a' ,3) , (3 , 'b' ,3) , (3 , 'c' ,3)]
	# )

	# aut_inter = intersection(aut1, aut2)
	# aut_union = union(aut1, aut2)

	# aut_inter.display(wait=False)
	# aut_union.display(wait=False)
	# aut = automaton.automaton (
	# 	states = [2] , initials = [0] , finals = [1,2],
	# 	transitions = [(0 , 'a' ,1) , (0 , 'b' ,1) , (0 , 'b' ,2), (1 , 'a' ,0), (1 , 'a' ,2), (2 , 'a' ,2)]
	# 	)

	# aut.display(wait="false")
	# aut_deter = determinisation(aut)

	#E = list( ["*", ["+", ["a", [".", ["*","b"], ["a"]]]]])
	#aut = expression_vers_automate(E)
	#aut.display(wait=False)

	#E1 = analyseur("(a+b*a)*")
	#aut1 = expression_vers_automate(E1)
	#aut1.display(wait=False)

	# aut = automaton.automaton (
	#  	alphabet = ['a', 'b'],
	#  	states = [7] , initials = [0] , finals = [2],
	# 	transitions = [(0 , 'a' ,1), (0 , 'b' ,5), (1 , 'b' ,2), (2 , 'b' ,2), (2 , 'a' ,3), (3 , 'b' ,6), (4 , 'b' ,5), (4 , 'a' ,7), (5 , 'a' ,2), (5 , 'b' ,6), (6 , 'b' ,4), (6 , 'a' ,7),(7 , 'b' ,2)]
	#  )
	# aut = aut.get_renumbered_automaton()
	
	# aut_min = minimiser(aut)
	# aut_min = aut_min.get_renumbered_automaton()
	# #aut.display(wait = False)
	# aut_min.display()

	 aut = automaton.automaton (
	  	alphabet = ['a', 'b'],
	  	states = [3] , initials = [0] , finals = [2,3],
	 	transitions = [(0 , 'a' ,1), (1 , 'b' ,2), (2 , 'a' ,3)]
	 	)
	 aut.display(wait = False)
	 aut_compl = complement(aut)
	 aut_compl.display(wait = False)

main()

