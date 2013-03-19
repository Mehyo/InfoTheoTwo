import automaton


def completer(aut):
	return aut

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

	aut_mirror = automaton . automaton (
	alphabet = aut.get_alphabet(),
	epsilons = [ '0 '] ,
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
	aut1 = automaton . automaton (
	epsilons = [ '0 '] ,
	states = [1] , initials = [0] , finals = [2] ,
	transitions = [(0 , 'a ' ,1) , (1 , 'b ' ,2)]
	)
	aut_miroir = miroir(aut1)
	aut1.display()
	aut_miroir.display()


main()