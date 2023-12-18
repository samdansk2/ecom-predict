# Program to illustrate depth first search algorithm :
# Used set type for repeated values
# To represent a graph in python basically we use curly braces and values
graph = {
  '1':['8','5','2'],
  '8':['6','4','3'],
  '5':[],
  '2':['9'],
  '6':['10','7'],
  '4':[],
  '3':[],
  '9':[],
  '10':[],
  '7':[] 
}

visited = set()

def dfs(visited, graph, node):
    if node not in visited:
        print(node,end=" ")
        visited.add(node)
        for neighbour in graph[node]:
            dfs(visited, graph, neighbour)

dfs(visited, graph, '1')

