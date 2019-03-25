#' % Schelling Model
#' % Aish Gupta
#' % 25 March 2019

#+ name='Warnings',echo=False
import warnings
warnings.filterwarnings("ignore")
#' #### Basic 2d graph
#+ name='Packages'
import networkx as nx
import matplotlib.pyplot as plt
import random
#+ name='Basic'
N = 10
G = nx.grid_2d_graph(N,N)
nx.draw(G)
plt.show()


#' ##### Format of nodes
#+ name='tuple_display',echo=False
print('These tuples are relative positions',G.nodes())

#' #### To show the grid in a better way
#+ name='draw_grid'
pos = dict((n,n) for n in G.nodes())
nx.draw(G,pos, with_labels=True)
plt.show()

#' #### Resolving tuples
#+ name='draw_grid_with_labels'
labels = dict(((i,j),i*10+j) for i,j in G.nodes())

nx.draw(G,pos,with_labels = False)

nx.draw_networkx_labels(G,pos, labels= labels)
plt.show()

#' #### Adding Diagonals
#+ name='Diagnol_addition',f_size=(8,8)
for (u,v) in G.nodes():
	if (u+1 <= N-1) and (v+1 <= N-1):
		G.add_edge((u,v),(u+1,v+1))

nx.draw(G,pos, with_labels=True)
plt.title('main diagnols')
plt.show()

for (u,v) in G.nodes():
	if (u+1 <= N-1) and (v-1 >= 0):
		G.add_edge((u,v),(u+1,v-1))

nx.draw(G,pos,with_labels = False)
nx.draw_networkx_labels(G,pos, labels= labels)
plt.title('both diagnols')
plt.show()

#' ### Splitting the nodes into 3 types
#' * Green
#' * Red
#' * Empty
#+ name='Assigning_type',f_size=(8,8)
for n in G.nodes():
	G.node[n]['type'] = random.randint(0,2)

type1_node_list = [n for (n,d) in G.nodes(data= True) if d['type'] == 1]
type2_node_list = [n for (n,d) in G.nodes(data= True) if d['type'] == 2]
empty_cells = [n for (n,d) in G.nodes(data = True) if d['type'] == 0]

#+ name='Decor',f_size=(8,8)
def display_graph(G):
	nodes_g = nx.draw_networkx_nodes(G,pos,node_color = 'green', nodelist= type1_node_list)
	nodes_g = nx.draw_networkx_nodes(G,pos,node_color = 'red', nodelist= type2_node_list)
	nodes_g = nx.draw_networkx_nodes(G,pos,node_color = 'white', nodelist= empty_cells)

	nx.draw_networkx_edges(G,pos)
	nx.draw_networkx_labels(G,pos, labels= labels)
	plt.show()
display_graph(G)

#' ##### Retriving Boundary and Internal nodes
#+ name='internal_boundary'
def get_boundary_nodes(G):
	boundary_nodes_list=[]
	for ((u,v),d) in G.nodes(data= True):
		if u == 0 or u == N-1 or v == 0 or v == N-1:
			boundary_nodes_list.append((u,v))
	return boundary_nodes_list

boundary_nodes_list = get_boundary_nodes(G)
internal_nodes_list = list(set(G.nodes()) - set(boundary_nodes_list))

#' #### Neighbours
#+ name='Neighbours'
def get_neigh_for_internal(u,v):
	neigh = []
	for i in range(-1,2):
		for j in range(-1,2):
			neigh.append((u-i,v-j))
	neigh.remove((u,v))
	return neigh

def get_neigh_for_boundary(u,v):
	if u == 0 and v == 0:
		return [(0,1),(1,1),(1,0)]
	elif u == N-1 and v == N-1:
		return [(N-2,N-2),(N-1,N-2),(N-2,N-1)]
	elif u == N-1 and v == 0:
		return [(u-1,v),(u,v+1),(u-1,v+1)]
	elif u == 0 and v == N-1:
		return [(u+1,v),(u+1,v-1),(u,v-1)]
	elif u == 0:
		return [(u,v-1),(u+1,v),(u,v+1),(u+1,v+1),(u+1,v-1)]
	elif u == N-1:
		return [(u-1,v),(u,v-1),(u,v+1),(u-1,v+1),(u-1,v-1)]
	elif v == N-1:
		return [(u,v-1),(u-1,v),(u+1,v),(u-1,v-1),(u+1,v-1)]
	elif v == 0:
		return [(u-1,v),(u+1,v),(u,v+1),(u-1,v+1),(u+1,v+1)]

#' #### To check the satisfaction
#+ name='Satisfaction'

def get_unsatisfied_nodes_list(G, internal_nodes_list, boundary_nodes_list):
	unsatified_nodes_list = []
	t = 3
	for u,v in G.nodes():
		type_of_this_node = G.node[(u,v)]['type']
		if type_of_this_node == 0:
			continue
		else:
			similar_nodes = 0
			if (u,v) in internal_nodes_list:
				neigh = get_neigh_for_internal(u,v)
			elif (u,v) in boundary_nodes_list:
				neigh = get_neigh_for_boundary(u,v)

			for each in neigh:
				if G.node[each]['type'] == type_of_this_node:
					similar_nodes += 1

			if similar_nodes <= t:
				unsatified_nodes_list.append((u,v))

	return unsatified_nodes_list

#+ name='Printing_unsatisfaction'
unsatisfied_nodes_list = get_unsatisfied_nodes_list(G, internal_nodes_list, boundary_nodes_list)
print(unsatisfied_nodes_list)

#' ### Iteratively satisfying the nodes
#+ name='Satisfying_them'
def make_a_node_satisfied(unsatisfied_nodes_list, empty_cells):
	if len(unsatisfied_nodes_list) != 0:
		node_to_shift = random.choice(unsatisfied_nodes_list)
		new_position = random.choice(empty_cells)

		G.node[new_position]['type'] = G.node[node_to_shift]['type']
		G.node[node_to_shift]['type'] = 0
		labels[node_to_shift],labels[new_position] = labels[new_position], labels[node_to_shift]
	else:
		pass

for i in range(200000):
	unsatisfied_nodes_list = get_unsatisfied_nodes_list(G, internal_nodes_list, boundary_nodes_list)

	make_a_node_satisfied(unsatisfied_nodes_list,empty_cells)
	type1_node_list = [n for (n,d) in G.nodes(data= True) if d['type'] == 1]
	type2_node_list = [n for (n,d) in G.nodes(data= True) if d['type'] == 2]
	empty_cells = [n for (n,d) in G.nodes(data = True) if d['type'] == 0]
	if len(unsatisfied_nodes_list) == 0:
		print(i)
		break
display_graph(G)
print(get_unsatisfied_nodes_list(G, internal_nodes_list, boundary_nodes_list))