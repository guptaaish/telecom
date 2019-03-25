#' % Fatman Model
#' % Aish Gupta
#' % 22 March 2019

#+ echo=False
import warnings
warnings.filterwarnings("ignore")
#' #### Importing the packages
import networkx as nx
import matplotlib.pyplot as plt

#' Making the graph
G = nx.Graph()

G.add_nodes_from(range(1,101))

nx.draw(G)
plt.show()

#' All the functionalities are now modeled into methods

def create_graph():
	G = nx.Graph()
	G.add_nodes_from(range(1,101))
	return G

def visualize(G):
	nx.draw(G)
	plt.show()

G = create_graph()
visualize(G)

#' Assigning BMI for nodes
import random
def assign_bmi(G):
	for each in G.nodes():
		G.node[each]['name'] = random.randint(15,40)
		G.node[each]['type'] = 'person'

#' #### format of BMI assignment
#+ echo=False
assign_bmi(G)
count = 0
for i in G.nodes():
	print(G.node[i])
	count += 1
	if count > 6:
		break

#' #### Label Getter
def get_labels(G):
	return {i: G.node[i]['name'] for i in G.nodes()}

def visualize_with_BMI(G,labeldict):
	nx.draw(G, labels=labeldict)
	plt.show()
#+ echo=True, f_size=(7,7)
G = create_graph()
assign_bmi(G)

labeldict = get_labels(G)
visualize_with_BMI(G,labeldict)

#' ##### Drawing graph nodes in accordance to BMI
#+ echo=True, evaluate=True
def get_size(G):
	return [G.node[i]['name'] for i in G.nodes()]

def visualize_BMI_sized(G,labeldict,nodesize):
	nx.draw(G,labels=labeldict,node_size=nodesize)
	plt.show()


#+ echo=True, f_size=(10,10)
nodesize = get_size(G)
visualize_BMI_sized(G,labeldict,nodesize)

#' ##### Since the size is very small
#+ f_size=(10,10)
def get_size(G):
	return [G.node[i]['name']*30 for i in G.nodes()]

nodesize = get_size(G)
visualize_BMI_sized(G,labeldict,nodesize)

#' #### Node sized according to BMI with node number as display
#+ f_size=(10,10)
def visualize_sized(G,nodesize):
	nx.draw(G,with_labels= True, node_size=nodesize)
	plt.show()

nodesize = get_size(G)
visualize_sized(G,nodesize)

#' ### We add the community businesses 
#+ echo=True
def add_foci_nodes(G):
	n = G.order() + 1
	foci_nodes = ['gym', 'eatout', 'movie_club', 'karate_club','Yoga_club']
	for j in range(0,5):
		G.add_node(n)
		G.node[n]['name'] = foci_nodes[j]
		G.node[n]['type'] = 'foci'
		n = n+1
#Since the foci are added then in get_size(G), we need to change the conditions

def get_size(G):
	size_array = []
	for each in G.nodes():
		if G.node[each]['type'] == 'person':
			size_array.append(G.node[each]['name']*20)
		else:
			size_array.append(1000)
	return size_array

#+ evaluate=True, f_size=(10,10)
add_foci_nodes(G)
labeldict = get_labels(G)
nodesize = get_size(G)
visualize_BMI_sized(G,labeldict,nodesize)


#+ echo=True
def get_colors(G):
	c = []
	for each in G.nodes():
		if G.node[each]['type'] == 'person':
			c.append('blue')
		else:
			c.append('red')
	return c

def visualize_BMI_sized_colored(G,labeldict,nodesize,color):
	nx.draw(G,labels=labeldict,with_labels = True,node_size=nodesize,node_color = color)
	plt.show()

#+ evaluate=True, f_size=(10,10)
color_arr = get_colors(G)
visualize_BMI_sized_colored(G,labeldict,nodesize,color_arr)

#' #### Adding edges to the Foci
#+ echo=True
def get_foci_nodes(G):
	f = []
	for each in G.nodes():
		if G.node[each]['type'] == 'foci':
			f.append(each)
	return f

def get_person_nodes(G):
	p = []
	for each in G.nodes():
		if G.node[each]['type'] == 'person':
			p.append(each)
	return p

def add_foci_edges(G):
	foci_nodes = get_foci_nodes(G)
	person_nodes = get_person_nodes(G)
	for each in person_nodes:
		r = random.choice(foci_nodes)
		G.add_edge(each,r)

def visualize_kamada_BMI_sized_colored(G,labeldict,nodesize,color):
	nx.draw_kamada_kawai(G,labels=labeldict, with_labels=True,node_size=nodesize,node_color = color)
	plt.show()

#+ f_size=(8,8)
add_foci_edges(G)
visualize_kamada_BMI_sized_colored(G,labeldict,nodesize,color_arr)

#' ## To Program Homophily
#' It is evident that:
#' Probability of 2 people becoming friends is **inversely proportional** to difference of their BMI.
#' More is the difference in BMI, less likely people will becom friends 

#' P(X and Y becoming friends) = $\frac{1}{|b(X)-b(Y)|}$

#' <div style="text-align: center"> b(A) is BMI of person A </div>
#' But we don't use the above expression, We use:

#' **P(X and Y becoming friends) =**
#' $\frac{1}{|b(X)-b(Y)| + 1000}$ 

#' The benefit with this is:
#' * If 2 BMIs are equal then the infinity condition is handeled
#' * Delays the convergence of the evolutionary algorithm

#' Initially, the probability are assigned randomly and we will benchmark the probability of becoming friends to be 0.4. **If the 2 people have probability less than 0.4, we generate the edge, otherwise, we don't.

#' #### Implementing Underweight in green and overweight in yellow and remaining in yellow

def get_colors(G):
	c = []
	for each in G.nodes():
		if G.node[each]['type'] == 'person':
			if G.node[each]['name'] < 19:
				c.append('green')
			elif G.node[each]['name'] > 34:
				c.append('yellow')
			else:
				c.append('blue')
		else:
			c.append('red')
	return c

#' #### This appears as
#+ f_size=(6,6)
color_arr = get_colors(G)
visualize_kamada_BMI_sized_colored(G,labeldict,nodesize,color_arr)

#' #### Adding Homophily
def homophily(G):
	pnodes = get_person_nodes(G)
	for u in pnodes:
		for v in pnodes:
			if u != v:
				diff = abs(G.node[u]['name'] - G.node[v]['name'])
				p = float(1/(diff+1000))
				r = random.uniform(0,1)
				if r < p:
					G.add_edge(u,v)

#+ f_size=(10,10)
homophily(G)
visualize_BMI_sized_colored(G,labeldict,nodesize,color_arr)

#' We have found the formula for probability for triadic closure to be = 1-${(1-p)}^{k}$ where p is the probability of 2 nodes joining  and k is the no of common neighbors

#' For now we use the same formula for triadic and focal closure
import math

def cmn(u,v,G):
	nu = set(G.neighbors(u))
	nv = set(G.neighbors(v))
	return len(nu & nv)

def closure(G):
	#The below array will have 2 nodes and the probability of them joining
	array1 = []
	#both the nodes should not be foci nodes
	for u in G.nodes():
		for v in G.nodes():
			if u!=v and ('person' in [G.node[u]['type'], G.node[v]['type']]):
				k = cmn(u,v,G)
				p = 1 - math.pow((1-0.1),k)
				tmp = [u,v,p]
				array1.append(tmp)
	for each in array1:
		u,v,p = each
		r = random.uniform(0,1)
		if r<p:
			G.add_edge(u,v)

#+ echo=True,f_size=(10,10)
closure(G)
visualize_kamada_BMI_sized_colored(G,labeldict,nodesize,color_arr)

#' ### So far it looks like
#+ echo=False
del G

#+ echo=True,f_size=(10,10)
G = create_graph()
assign_bmi(G)
add_foci_nodes(G)
add_foci_edges(G)
homophily(G)
closure(G)
labeldict = get_labels(G)
nodesize = get_size(G)
color_arr = get_colors(G)
visualize_kamada_BMI_sized_colored(G,labeldict,nodesize,color_arr)

#' # Social Influence
#' If person goes to the gym, their BMI decreases. Social Influence suggests that  BMI increases in the case of eatery.

def change_bmi(G):
	fnodes = get_foci_nodes(G)
	for each in fnodes:
		if G.node[each]['name'] == 'eatout':
			for each1 in G.neighbors(each):
				if G.node[each1]['name'] != 40:
					G.node[each1]['name'] = G.node[each1]['name'] + 1

		if G.node[each]['name'] == 'gym':
			for each1 in G.neighbors(each):
				if G.node[each1]['name'] != 15:
					G.node[each1]['name'] = G.node[each1]['name'] - 1

#' #### Modifying all the visualization functions
#+ f_size=(10,10)

#Basic graph visualization
def visualize(G):
	nx.draw(G)
	plt.show()

#Graph visualization with nodes sized according to BMI
def visualize_sized(G):
	nx.draw(G,with_labels= True, node_size= get_size(G))
	plt.show()

#Graph visualization with nodes displaying BMI and sized according to BMI
def visualize_BMI_sized(G):
	nx.draw(G,labels= get_labels(G),node_size= get_size(G))
	plt.show()

#Graph visualization with nodes displaying node no. and sized according to BMI
def visualize_with_BMI(G):
	nx.draw(G, labels= get_labels(G))
	plt.show()

#Graph visualization with nodes displaying BMI and sized & coloured according to BMI
def visualize_BMI_sized_colored(G):
	nx.draw(G,labels= get_labels(G), with_labels= True,node_size= get_size(G),node_color = get_colors(G))
	plt.show()

#Graph visualization in Kamada Kawai format, with nodes displaying BMI and sized & coloured according to BMI
def visualize_kamada_BMI_sized_colored(G):
	nx.draw_kamada_kawai(G,labels= get_labels(G), with_labels= True,node_size= get_size(G),node_color = get_colors(G))
	plt.show()

#' ### Iterating to see social influence
#' The relevance of *graph_list* is shown later
#+ f_size=(10,10),	
graph_list = []
visualize_kamada_BMI_sized_colored(G)

#nx.Graph(G) Creates an instance of G
graph_list.append(nx.Graph(G))

for t in range(0,10):
	homophily(G)
	closure(G)
	change_bmi(G)
	visualize_kamada_BMI_sized_colored(G)
	#nx.Graph(G) Creates an instance of G
	graph_list.append(nx.Graph(G))

#' ### Analyzing the various graphs stored in the *graph_list*
#+ f_size=(8,8)
def plot_density(graph_list):
	x = list(range(len(graph_list)))
	y = [nx.density(i) for i in graph_list]
	print('x =',x,'\ny = ',y)
	plt.xlabel('Time')
	plt.ylabel('Density')
	plt.title('Change in Density')
	plt.plot(x,y,'bo-')
	plt.show()

def obesity(G):
	num = 0
	for each in G.nodes():
		if G.node[each]['name'] == 40:
			num+=1
	return num

def plot_obesity(graph_list):
	x = list(range(len(graph_list)))
	y = [obesity(i) for i in graph_list]
	plt.xlabel('Time')
	plt.ylabel('Obesity')
	plt.title('Change in Obesity')
	plt.plot(x,y,'ro-')
	plt.show()

plot_obesity(graph_list)
plot_density(graph_list)