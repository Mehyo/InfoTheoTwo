import automaton


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
		epsilons = [ '0 '],
		states = aut.get_states() , initials = aut.get_final_states() , finals = aut.get_initial_states(),
		transitions = new_transitions
	)

	return aut_mirror

def determinisation(aut):
	return aut_deter

def complement(aut):
	return aut_comp

def minimiser(aut):
	return aut_mini

def expression_vers_automate(E):
	return aut


"Un au choix"

def double_renversement():
	return aut

def analyseur(chaine):
	return liste



def main():
	aut1 = automaton.automaton (
		alphabet = ['a', 'b', 'c'],
		states = [2] , initials = [1] , finals = [2],
		transitions = [(1 , 'a' ,1) , (1 , 'b' ,1) , (1 , 'c' ,2) , (2 , 'a' ,2) , (2 , 'b' ,2) , (2 , 'c' ,2)]
	)

	aut2 = automaton.automaton (
		alphabet = ['a', 'b', 'c'],
		states = [3] , initials = [1] , finals = [3],
		transitions = [(1 , 'a' ,1) , (1 , 'c' ,1) , (1 , 'b' ,2) , (2 , 'a' ,3) , (2 , 'b' ,2) , (2 , 'c' ,1),
			(3 , 'a' ,3) , (3 , 'b' ,3) , (3 , 'c' ,3)]
	)

	aut_inter = intersection(aut1, aut2)
	aut_union = union(aut1, aut2)

	aut_inter.display(wait=False)
	aut_union.display(wait=False)


main()	