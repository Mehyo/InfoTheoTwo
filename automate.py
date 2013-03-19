import automaton


def completer(aut):
	states = list(aut.get_states())
	transitions = list(aut.get_transitions())
	alphabet = list(aut.get_alphabet())
	epsilons = list(aut.get_epsilons())
	aut.add_state('P')

	i = 0
	j = 0
	k = 0

	while i < len(states):
		while j < len(alphabet):
			if (alphabet[j] in epsilons):
				j+=1
			while k < len(transitions):
				if (transitions[k][0] == states[i]) & (transitions[k][1] == alphabet[j]):
					break
				else:
					if(k == len(transitions) - 1):
						aut.add_transition((states[i], alphabet[j], 'P'))
				k+=1
			j+=1
			k = 0
		i+=1
		j = 0

	for t in alphabet:
		if t in epsilons:
			continue
		aut.add_transition(('P', t, 'P'))

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
	epsilons = ['0'],
	states = [1] , initials = [0] , finals = [2] ,
	transitions = [(0 , 'a ' ,1) , (1 , 'b ' ,2)]
	)
	aut1.display()
	aut_completer = completer(aut1)
	aut_completer.display()
	


main()