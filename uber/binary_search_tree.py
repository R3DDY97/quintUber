# class Node():

#     def __init__(self,key):
#         self.key = key
#         self.left = None
#         self.right = None
#         self.parent = None


# class Tree():

#     def __init__(self):
#         self.root = None

#     def add_node(self,key,node=None):

#         if node is None:
#             node = self.root

#         if self.root is None:
#             self.root = Node(key)
#             return


#         if key <= node.key :
#             if node.left is None:
#                 node.left = Node(key)
#                 node.left.parent = node
#             else:
#                 return self.add_node(key,node = node.left)
#         else:
#             if node.right is None:
#                 node.right = Node(key)
#                 node.right.parent = node
#             else:
#                 return self.add_node(key,node = node.right)


#     def search(self,key,node = None):

#         if node is None:
#             node = self.root

#         if self.root.key == key:
#             return self.root.key

#         if node.key == key :
#             return node

#         if key < node.key:
#             if node.left is not None:
#                 return self.search(key,node = node.left)
#             else:
#                 return node

#         if  key > node.key:
#             if node.right is not None:
#                 return self.search(key,node = node.right)
#             else:
#                 return node

#     def delete_node(self, node):

#         key = node.key
#         if self.root.key == key:
#             parent_node = self.root
#         else:
#             parent_node = node.parent

#         if node.left is None and node.right is None:
#             if key <= parent_node.key:
#                 parent_node.left = None
#             else:
#                 parent_node.right = None
#             return

#         if node.left is not None and node.right is None :
#             if node.left.key < parent_node.key :
#                 parent_node.left = node.left
#             else:
#                 parent_node.right = node.left
#             return

#         if node.right is not None and node.left is None:
#             if node.key <= parent_node.key:
#                 parent_node.left = node.right
#             else:
#                 parent_node.right = node.right
#             return

#         if node.left is not None and node.right is not None:
#             min_value = self.find_minimum(node)
#             node.key = min_value.key
#             min_value.parent.left = None
#             return

#         def find_minimum(self,node = None):

#             if node is None:
#                 node = self.root

#             if node.right is not None:
#                 node = node.right
#             else:
#                 return node

#             if node.left is not None:
#                 return self.find_minimum(node = node.left)
#             else:
#                 return node
