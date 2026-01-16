class BSTNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None


class BST:
    """Binary Search Tree implementation"""
    
    def __init__(self):
        self.root = None
        self.size = 0
    
    def insert(self, key, value):
        """Insert key-value pair"""
        if self.root is None:
            self.root = BSTNode(key, value)
            self.size += 1
            return True
        
        return self._insert_recursive(self.root, key, value)
    
    def _insert_recursive(self, node, key, value):
        if key == node.key:
            node.value = value  # Update existing
            return False
        elif key < node.key:
            if node.left is None:
                node.left = BSTNode(key, value)
                self.size += 1
                return True
            return self._insert_recursive(node.left, key, value)
        else:
            if node.right is None:
                node.right = BSTNode(key, value)
                self.size += 1
                return True
            return self._insert_recursive(node.right, key, value)
    
    def search(self, key):
        """Search for key, return value or None"""
        node = self._search_recursive(self.root, key)
        return node.value if node else None
    
    def _search_recursive(self, node, key):
        if node is None or node.key == key:
            return node
        if key < node.key:
            return self._search_recursive(node.left, key)
        return self._search_recursive(node.right, key)
    
    def delete(self, key):
        """Delete key from tree"""
        self.root, deleted = self._delete_recursive(self.root, key)
        if deleted:
            self.size -= 1
        return deleted
    
    def _delete_recursive(self, node, key):
        if node is None:
            return None, False
        
        if key < node.key:
            node.left, deleted = self._delete_recursive(node.left, key)
            return node, deleted
        elif key > node.key:
            node.right, deleted = self._delete_recursive(node.right, key)
            return node, deleted
        else:
            # Node to delete found
            if node.left is None:
                return node.right, True
            elif node.right is None:
                return node.left, True
            
            # Two children: find min in right subtree
            min_node = self._find_min(node.right)
            node.key = min_node.key
            node.value = min_node.value
            node.right, _ = self._delete_recursive(node.right, min_node.key)
            return node, True
    
    def _find_min(self, node):
        while node.left:
            node = node.left
        return node
    
    def get_height(self):
        """Calculate tree height"""
        return self._height_recursive(self.root)
    
    def _height_recursive(self, node):
        if node is None:
            return 0
        return 1 + max(self._height_recursive(node.left), 
                       self._height_recursive(node.right))
    
    def get_all_items(self):
        """Get all key-value pairs (in-order)"""
        items = []
        self._inorder_traversal(self.root, items)
        return items
    
    def _inorder_traversal(self, node, items):
        if node:
            self._inorder_traversal(node.left, items)
            items.append((node.key, node.value))
            self._inorder_traversal(node.right, items)
    
    def clear(self):
        """Clear all nodes"""
        self.root = None
        self.size = 0