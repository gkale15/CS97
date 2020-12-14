# Keep the function signature,
# but replace its body with your implementation.
#
# Note that this is the driver function.
# Please write a well-structured implemention by creating other functions outside of this one,
# each of which has a designated purpose.
#
# As a good programming practice,
# please do not use any script-level variables that are modifiable.
# This is because those variables live on forever once the script is imported,
# and the changes to them will persist across different invocations of the imported functions.
import zlib
import os.path
import sys
from pathlib import Path
from pathlib import PurePath

from os import path


def topo_order_commits():
    if(checkgit()):
        return 1;
#TASK2
    p = Path('.git')
    objs = Path('.git/objects')
    heads = Path('.git/refs/heads')
#init some path objects using the os and pathlib libraries in python
    headrefs = []
    objstack = set()
    node_List = set()
    branches_dict = {}
    #for all files/folders in refs/heads path inside git folder, create a list of
    #filepaths to an actual file that contains a branch pointer, not a directory
    for x in heads.iterdir():
        if not(Path.is_file(x)):
            for i in x.iterdir():
                headrefs.append(i)
        else:
            headrefs.append(x)

    while (headrefs):
        #extract the name of these pointers from the actual path, this is for TASK5
        head = headrefs.pop()
        for x in range(len(PurePath(head).parts)):
            if PurePath(head).parts[x] == 'heads':
                branchname = '/'.join(PurePath(head).parts[x + 1:])
        #open the files and match each branch head with an actual git object in the objects folder
        #push these resulting objects into a stack, but also create CommitNode objects using their full hash
        headfiles = open(head,'r')
        cur = headfiles.read().replace('\n','')
        for y in objs.iterdir():
            for z in y.iterdir():
                if(Path.is_file(z)):
                    ohash = PurePath(y).name + PurePath(z).name
                    if ohash == cur:
                        flg = False
                        for nodes in node_List:
                            if (nodes.commit_hash == cur):
                                flg = True
                        if flg == False:
                            node_List.add(CommitNode(ohash))
                            objstack.add(z)
                            branches_dict[ohash] = branchname
                        elif flg == True:
                            tempstr = branches_dict[ohash]
                            #this dictionary goes from commit_hash to the names of the branch heads, for TASK5
                            branches_dict[ohash] = tempstr + ' ' + branchname
                        flg = False

                        
                        
    #TASK3
    while(objstack):
        #treating list objstack as a stack by always popping from the end, and then pushing to the end
        #this lets me flatten my recursion into a while loop 
        #pros to this is it saves memory, cons is it takes a hell of a lot more time to do
        i = objstack.pop()
        file = open(i,'rb')
        compressed_data = file.read()
        decompressed_data = zlib.decompress(compressed_data).decode("utf-8")
        parent_hash = []
        srr = decompressed_data.split('\n');
        #getting each parent of a given commit_hash
        for count in srr:
            if (count.split(' ')[0] == 'parent'):
                parent_hash.append(count.split(' ')[1])

        append_hash = PurePath(i).parts[-2:]
        i_hash = ''.join(append_hash)
        #add the commit hash to the list of CommitNodes if it does not already exist
        #more for safety than actual need, should not be needed since I push parents in anyways later
        committed = False
        for ff in node_List:
            if(ff.commit_hash == i_hash):
                committed = True
        if(committed is False):
            node_List.add(CommitNode(i_hash))
        #add to parents of current hash chosen if not already in there
        for k in node_List:
            if k.commit_hash == i_hash:
                for p in parent_hash:
                    if not(p in k.parents):
                        k.parents.add(p)
        #add parents to the list of CommitNodes, and push to stack if not already a CommitNode
        for y in objs.iterdir():
            for z in y.iterdir():
                if(Path.is_file(z)):
                    ohash = PurePath(y).name + PurePath(z).name
                    for p in parent_hash:
                        if ohash == p:
                            flg = False
                            for nodes in node_List:
                                if (nodes.commit_hash == p):
                                    flg = True
                            if flg == False:        
                                node_List.add(CommitNode(p))
                                objstack.add(z)
                            flg = False
        #add the hash we had originally been operating on to children of the parents we have for that hash
        #if not already in the set, that is                
        for l in node_List:
            for p in parent_hash:
                if l.commit_hash == p:
                    if not(i_hash in l.children):
                        l.children.add(i_hash)
    #TASK4
    nodes_hash = {}
    #this dictionary stores a "deep copy" of our list of CommitNodes as strings by hash
    #this is because in the top sort, we end up modifying some of the original objects
    for i in node_List:
        parentstr = " ".join(i.parents)
        childstr = " ".join(i.children)
        nodes_hash[i.commit_hash] = parentstr + ';' + childstr

    #create a list root commits which contains all Nodes with no parents, and remove said nodes form 
    #the original Node list
    root_commits = []
    for i in node_List:
        if(len(i.parents) == 0):
            root_commits.append(i)
    for i in root_commits:
        node_List.remove(i)


    topsort_root = root_commits
    topsort_nodes = node_List
    topsort_fin = []
    #the actual topological sort, also flattened using a while loop, this follows general psuedocode
    while(topsort_root):
        pop_node = topsort_root.pop()
        topsort_fin.append(pop_node.commit_hash)
        #remove edges from all parents that contain said edge
        for i in topsort_nodes:
            for chile in pop_node.children:
                if(chile == i.commit_hash):
                    i.parents.remove(pop_node.commit_hash)
        #if a parent is empty, add that to the root_commits list since it now has no parents technically
        for i in topsort_nodes:
            if(not i.parents):
                topsort_root.append(i)
        #remove all nodes from the node list that are now in the root list
        for j in topsort_root:
            if j in topsort_nodes:
                topsort_nodes.remove(j)

    #reverse list in prep for TASK5
    topsort_fin.reverse()
    
    #TASK5
    for i in range(len(topsort_fin)):
        hashes = topsort_fin[i]
        parents = (nodes_hash[hashes].split(';')[0]).split(' ')
        children = (nodes_hash[hashes].split(';')[1]).split(' ')
        nexthash = ""
        prevhash = ""
        #setting the children and parents of the current hash based on the dictionary we made earlier
        #above for prev statement

        #below, checking if the prevhash and nexthash are parents and children of the current,
        #respectively. If not need to sticky end/start
        if i < (len(topsort_fin) - 1):
            nexthash = topsort_fin[i + 1]
        if i > 0:
            prevhash = topsort_fin[i - 1]

        #this sets hash_branch to hash + branch names if there are any branchnames associated with it.
        #this uses the dictionary we made all the way back during TASK1
        hash_branch = hashes
        if(hashes in branches_dict.keys()):
           hash_branch = (hashes + ' ' + branches_dict[hashes])
        #just some general conditionals, these could have been condensed to make more succint in the future
        if(prevhash != "") and (not(prevhash in children)):
            print("=" + nodes_hash[hashes].split(';')[1])
            if (nexthash != "") and (not(nexthash in parents)):
                print(hash_branch)
                print(" ".join(parents) + "=")
                print("")
            else:
                print(hash_branch)
        elif(nexthash != "") and (not(nexthash in parents)):
            if (prevhash != "") and (not(prevhash in children)):
                print("=" + nodes_hash[hashes].split(';')[1])
            print(hash_branch)
            print(" ".join(parents) + "=")
            print("")
        else:
            print(hash_branch)

###TASK1
#here I am checking to see if there is a valid git file that can be traced back from the current directory
def checkgit():
    path = os.getcwd()
    while(path != '/'):
        #if the path is in the cwd return 0, and the cwd is changed
        if os.path.exists(".git"):
            return 0;
        #otherwise recurse back to the parent of the current directory
        os.chdir('../')
        path = os.getcwd()
    #final check to see if the file exists in / directory
    if os.path.exists(".git"):
        return 0
    else:
        print("Not inside a Git repository.")
        return 1
    return 0

class CommitNode:
    def __init__(self, commit_hash):
        """
        :type commit_hash: str
        """
        self.commit_hash = commit_hash
        self.parents = set()
        self.children = set()

#running strace on this function results in many many system calls, all of which are done because of something 
#that python called in order to print or display or change directory through an indirect method
#either through os or pathlib, which were used extensively in TASKS 1-3 to generate general sorts.
#There are no calls to shell/bash functions, which supports the fact that we never ran direct terminal commands
#in our program, and only used python commands to handle everything, and that too only commands contained
#in the general few functions.
#the search for 'bash' in the list of outputs returns null, while everything called from /bin is from the
#python folder


#overall, this implementation is a little slower than writing recursively in smaller functions, but while 
#hacking it together it is easier to keep track of variables and edge cases this way. Retuning and refactoring
#would probably warrant far fewer indexed memory references, but that screws up readability for the graders case

if __name__ == '__main__':
    topo_order_commits()
