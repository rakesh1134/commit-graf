import os
import zlib
import networkx as nx
from matplotlib import pyplot as plt

#git_dir = 'C:\\\\test\\.git'
git_dir = 'C:\\llama-models\\.git'

edges = []

class CommitNode:
    def __init__(self,commit_id,parents):
        self.commit_id = commit_id
        self.parents = parents
        #self.children() = []

def parse_commit_object_to_node(commit_id):
    parents = []
    for line in get_obj_content(commit_id).splitlines():
        #print(line)
        line = line.decode('ascii').strip('\n')
        #print("-->line" )
        #print(line)
        if (line.startswith('parent ')):
            #print("yes")
            parent_id = line[7:]
            parents.append(parent_id)

            tup = (commit_id[:6],parent_id[:6])
            edges.append(tup)

    n = CommitNode(commit_id,parents)
    return n
    

def getheads():
    return git_dir + '\\refs\\heads'

def getbranches():
    heads_dir = getheads()
    branches = os.listdir(heads_dir)
    return branches

def get_top_commit_branch():
    top_commits = []
    
    for b in getbranches():

        commit_id = open(getheads() +'\\' + b, 'rb').read()
        top_commits.append(commit_id.decode('ascii').strip('\n'))
        #branch_names.append(b)
    return top_commits

def get_obj_content(objid):
    objs_dir = git_dir +"\\objects"

    #print("objid")
    #print(objid)
    obj_dir_1 = objid[:2]
    obj_dir_2 = objid[2:]
    #print(obj_dir_1)
    #print(obj_dir_2)
    #print("hello")
    compressed_contents = open(objs_dir +"\\" + obj_dir_1 +"\\"+ obj_dir_2, 'rb').read()
    decompressed_contents = zlib.decompress(compressed_contents)
    return decompressed_contents

def print_commit_tree(commit,level):

    indent = " " * level
   # print(indent + "========================================")
    commit_nd = parse_commit_object_to_node(commit)

   # print(indent + "Commit: ")
    #print(indent + commit_nd.commit_id)


    #print(indent + "Parents: ")

    for p in commit_nd.parents:
        #print()
        #print(indent +  p)
        print_commit_tree(p,level+1)

def show_commit_graph():
    g1 = nx.DiGraph()
    g1.add_edges_from(edges)
    plt.tight_layout()
    nx.draw_networkx(g1, arrows=True)
    plt.show()
    
for commit in get_top_commit_branch():
    print_commit_tree(commit,1)

    show_commit_graph()
    #n = parse_commit_object_to_node(commit)
    #print("============")
    #print(n.commit_id)
    #print("--parents")
    #for p in n.parents:
    #    print(p)
    #print(get_obj_content(commit))
    #for line in get_obj_content(commit).splitlines():
    #    parse_commit_object_to_node(line,commit)
    #    print(line.decode('ascii').strip('\n'))
