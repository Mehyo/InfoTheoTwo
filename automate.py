import automaton


def completer(aut):

	aut_complet = aut.clone()
	
	puit = (aut_complet.get_maximal_id()+1)
	print(puit)
	aut_complet.add_state(puit)
	aut_complet.display()
	
	alpha = list( aut_complet.get_alphabet() )
	states = list( aut_complet.get_states() )
	
	for i in range( len( alpha ) ):
		for j in range( len( states ) ):
			if not aut_complet.delta( alpha[i], [states[j]] ):
				aut_complet.add_transition( (states[j], alpha[i], puit) )

	return aut_complet

def union(aut1, aut2):
	return aut_union

def intersection(aut1, aut2):
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
	aut = automaton.automaton (
		epsilons = [ '0 '],
		states = [5] , initials = [0,1] , finals = [3,4],
		transitions = [(0 , 'a' ,1) , (1 , 'b' ,2) , (2 , 'b' ,2) , (2 , '0' ,3) ,(3 , 'a' ,4)]
	)
	#aut_miroir = miroir(aut)
	#aut_miroir.display()

	aut_complet = completer(aut)
	aut.display()
	aut_complet.remove_epsilon_transitions()
	aut_complet.display()


main()	