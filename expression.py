import automaton

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
	j=i+1
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