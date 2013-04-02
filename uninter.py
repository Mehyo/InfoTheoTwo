import automaton

def uninter(aut1, aut2, type):
	"Effectue une union ou une intersection suivant la valeur de la variable type."

	alpha = list( aut1.get_alphabet() )

	aut = automaton.automaton ( 
		alphabet = alpha,
		epsilons = aut1.get_epsilons(),
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

							if type:
								if aut1.state_is_final((states1[j])) or aut2.state_is_final((states2[k])):
									aut.add_final_state((states1[j], states2[k]))
							else :
								if aut1.state_is_final((states1[j])) and aut2.state_is_final((states2[k])):
									aut.add_final_state((states1[j], states2[k]))

							if aut1.state_is_initial((states1[j])) and aut2.state_is_initial((states2[k])):	
								aut.add_initial_state((states1[j], states2[k]))
							aut.add_transition( ((states1[j],states2[k]), alpha[i], (tmp1[l], tmp2[l]) ))
	return aut