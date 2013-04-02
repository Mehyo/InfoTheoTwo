import automaton
from analyse import *
from expression import *
from uninter import *

def completer(aut):
	"Complete un automate non complet et ne modifie pas un automate complet."

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
	
	if aut_complet.has_state(puit) :
		for i in alpha:
			aut_complet.add_transition((puit, i, puit))


	return aut_complet	

def union(aut1, aut2):
	"Appelle uninter en lui demandant de faire une union."
	aut_union = uninter(aut1, aut2, True)
	return aut_union

def intersection(aut1, aut2):
	"Appelle uninter en lui demandant de faire une intersection."
	aut_inter = uninter(aut1, aut2, False)
	return aut_inter

def miroir(aut):
	"Inverse le sens des transitions et inverse les etats finaux et initaux d'un automate."

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
	"Determinise un automate."

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
	"Retourne le langage complement du langage d'un automate."

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
	"Minimise un automate en utilisant le double reversement."

	aut_min = miroir(aut)
	aut_min = determinisation(aut_min)
	aut_min = miroir(aut_min)
	aut_min = determinisation(aut_min)

	aut_min = aut_min.get_renumbered_automaton()
	return aut_min


def expression_vers_automate(E):
	"Cree un automate a partir d'une chaine de caractere."

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


def analyseur(chaine):
	"Analyse une expression rationnel et la transforme en chaine de caractere exploitable par la fonction expression_vers_automate"

	liste = list(chaine)

	liste = analyse(liste, False)

	return liste[0]



def main():

	aut = automaton.automaton (
		alphabet = ['a', 'b', 'c'],
		epsilons = ['0'],
		states = [2] , initials = [1] , finals = [2],
		transitions = [(1 , 'b' ,1) , (1 , 'c' ,2) , (2 , 'a' ,2) , (2 , 'b' ,2) , (2 , 'c' ,2)]
	)

	aut.display(title ="Base", wait=False)

	"Test de completer"

	complet = completer(aut)
	complet.display(title ="Complet")


	"Test de Union et Intersection"

	aut2 = automaton.automaton (
		alphabet = ['a', 'b', 'c'],
		epsilons = ['0','1'],
		states = [3] , initials = [1] , finals = [3],
		transitions = [(1 , 'a' ,1) , (1 , 'c' ,1) , (1 , 'b' ,2) , (2 , 'a' ,3) , (2 , 'b' ,2) , (2 , 'c' ,1),
			(3 , 'a' ,3) , (3 , 'b' ,3) , (3 , 'c' ,3)]
	)

	inter = intersection(aut, aut2)
	uni = union(aut, aut2)

	inter.display(title = "Intersection", wait=False)
	uni.display(title = "Union")

	"Test de miroir"

	aut_miroir = miroir(aut)
	aut_miroir.display(title ="Miroir")

	"Test de determiniser"

	aut_deter = determinisation(aut)
	aut_deter.display(title ="Determiniser")

	"Test de complement"

	aut_compl = complement(aut)
	aut_compl.display(title ="Complement")

	"Test de minimiser"

	aut_min = minimiser(aut)
	aut_min.display(title ="Minimiser")

	"Test de expression vers automate"

	E = list( ["*", ["+", ["a", [".", ["*","b"], ["a"]]]]])
	aut = expression_vers_automate(E)
	aut.display(title ="Expression->automate")

	"Test de expression vers chaine de caractere"

	E1 = analyseur("(a+b*a)*")
	aut1 = expression_vers_automate(E1)
	aut1.display(title ="Expression->liste->automate")



main()

