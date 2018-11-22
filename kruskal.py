#!/usr/bin/python
import fileinput
import csv
from sets import Set

def ordered_insert(element, lista):
	i = 0;
	# print element
	while i < len(lista) and lista[i][2] <= element[2]:
		i += 1		
	lista.insert(i, element)
	# lista.append(element)
	# return lista  
def add_node(graph, node_f, node_t):
	# print "-" * 5, "detect_cicles", "-" * 5
	# print node_f, "=>", node_t
	# for n in graph:
	# 	print n, ":", graph[n]
	if node_f in graph and node_t in graph:
		if graph[node_t] == graph[node_f]:
			return True
		else:
			for n in graph:
				if graph[n] == graph[node_f]:
					graph[n] = graph[node_t]
	elif node_f in graph and not node_t in graph:
		graph[node_t] = graph[node_f]
	elif not node_f in graph and node_t in graph :
		graph[node_f] = graph[node_t]
	else:
		aux_num = len(graph)
		graph[node_t] = aux_num
		graph[node_f] = aux_num
	# print "-" * 5, "END detect", "-" * 5
	return False

def kruskal(lista):
	connected_1 = Set()
	connected_2 = Set()
	ids = []
	graph = {}
	l_from = []
	l_to = []
	for e in lista:
		e0_c1 = e[0] in connected_1
		e1_c1 = e[1] in connected_1
		e0_c2 = e[0] in connected_2
		e1_c2 = e[1] in connected_2
		cycle = False
		if e[0] in graph and e[1] in graph:
			cycle = graph[e[0]] == graph[e[1]]
		# print int(e0_c1), int(e1_c1), int(e0_c2), int(e1_c2), cycle, " | ",
		if not e0_c1 and not e1_c1 and not e0_c2 and not e1_c2 and not cycle:
			add_node(graph, e[0], e[1])
			l_from.append(e[0])
			l_to.append(e[1])
			connected_1.add(e[0])
			connected_1.add(e[1])
			# print "1"
		elif not e0_c1 and e1_c1 and not e0_c2 and not e1_c2 and not cycle:
			add_node(graph, e[0], e[1])
			l_from.append(e[0])
			l_to.append(e[1])
			connected_1.add(e[0])
			connected_2.add(e[1])
			# print "2"
		elif e0_c1 and not e1_c1 and not e0_c2 and not e1_c2 and not cycle:
			add_node(graph, e[0], e[1])
			l_from.append(e[0])
			l_to.append(e[1])
			connected_1.add(e[1])
			connected_2.add(e[0])
			# print "3"
		elif e0_c1 and e1_c1 and not e0_c2 and not e1_c2 and not cycle:
			add_node(graph, e[0], e[1])
		 	l_from.append(e[0])
			l_to.append(e[1])
			connected_2.add(e[0])
			connected_2.add(e[1])
			# print "4"

	return l_from, l_to

distances = {}
points = {}

skip = True

mat = []
i = 0
j = 0
ordered_list = []
for l in  csv.reader(fileinput.input(), quotechar='"', delimiter=',',
                     quoting=csv.QUOTE_ALL, skipinitialspace=True):
	if skip:
		skip = False
	else:
		aux = l[1] + l[2]
		distances[aux] = l[3] 
		# print aux
		ordered_insert((l[1], l[2], int(l[3])), ordered_list)
		# ordered_list = ordered_insert((l[1], l[2], int(l[3])), ordered_list)

		if not l[1] in points:
			points[l[1]] = len(points)
		if not l[2] in points:
			points[l[2]] = len(points)

# for e in ordered_list:
# 	print e
# print len(ordered_list)

l1, l2 = kruskal(ordered_list)


print "=" * 10
tot_dist = 0
for l, t in zip(l1, l2):
	tot_dist += int(distances[l + t])
	print l, "->", t, ":", distances[l + t]
print "Total distance:", tot_dist, "\tTotal trips:", len(l1)
print "=" * 10


