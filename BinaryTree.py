# -*- coding: utf-8 -*-
"""
Binary search tree 
"""

class Node:
    def __init__(self,val):
        self.value = val
        self.left = None
        self.right = None


class BinaryTree:
    def __init__(self):
        self.root = None
    
    def insert(self,val):
        if self.root is None:
            self.root = Node(val)
        else:
            self._insertRecur(self.root,val)
    
    def _insertRecur(self,node,val):
        if val < node.value:  
            if node.left:
                self._insertRecur(node.left, val) 
            else:
                node.left = Node(val)  
        else:
            if node.right:
                self._insertRecur(node.right, val)
            else:
                node.right = Node(val)
    
    def traverse(self):
        return self._inOrderTraverse(self.root)
        
    def _inOrderTraverse(self, node):
        res = []
        if node is not None:
            res = self._inOrderTraverse(node.left)
            res.append(node.value)
            res = res + self._inOrderTraverse(node.right)
        return res
        
    def count(self):
        return self._count(self.root)
    
    def _count(self,node):
        if node is None:
            return 0
        return self._count(node.left) + self._count(node.right) + 1
    
    def height(self):
        return self._height(self.root)
    
    def _height(self,node):
        if node is None:
            return 0
        return max(self._height(node.left),self._height(node.right)) + 1
    
    def contains(self,val):
        return self._search(val,self.root)
    
    def _search(self,val,node):
        if node is None:
            return False
        elif val == node.value:
            return True
        elif val < node.value:
            return max(val==node.value,self._search(val,node.left))
        elif val > node.value:
            return max(val==node.value,self._search(val,node.right))
    
        
        
test = BinaryTree()
test.insert(2)
test.traverse()
test.insert(3)
test.traverse()
test.insert(1)
test.traverse()
test.insert(4)

test.count()
test.height()
test.contains(4)
test.contains(5)

