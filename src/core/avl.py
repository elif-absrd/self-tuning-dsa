class AVLNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None
        self.height = 1


class AVL:
    """AVL Tree implementation with automatic balancing"""
    
    def __init__(self):
        self.root = None
        self.size = 0
        self.rotation_count = 0
    
    def insert(self, key, value):
        """Insert with automatic rebalancing"""
        self.root, inserted = self._insert_recursive(self.root, key, value)
        if inserted:
            self.size += 1
        return inserted
    
    def _insert_recursive(self, node, key, value):
        # Standard BST insert
        if node is None:
            return AVLNode(key, value), True
        
        if key == node.key:
            node.value = value
            return node, False
        elif key < node.key:
            node.left, inserted = self._insert_recursive(node.left, key, value)
        else:
            node.right, inserted = self._insert_recursive(node.right, key, value)
        
        if not inserted:
            return node, False
        
        # Update height
        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))
        
        # Rebalance
        balance = self._get_balance(node)
        
        # Left-Left
        if balance > 1 and key < node.left.key:
            self.rotation_count += 1
            return self._rotate_right(node), True
        
        # Right-Right
        if balance < -1 and key > node.right.key:
            self.rotation_count += 1
            return self._rotate_left(node), True
        
        # Left-Right
        if balance > 1 and key > node.left.key:
            self.rotation_count += 2
            node.left = self._rotate_left(node.left)
            return self._rotate_right(node), True
        
        # Right-Left
        if balance < -1 and key < node.right.key:
            self.rotation_count += 2
            node.right = self._rotate_right(node.right)
            return self._rotate_left(node), True
        
        return node, True
    
    def search(self, key):
        """Search for key"""
        node = self._search_recursive(self.root, key)
        return node.value if node else None
    
    def _search_recursive(self, node, key):
        if node is None or node.key == key:
            return node
        if key < node.key:
            return self._search_recursive(node.left, key)
        return self._search_recursive(node.right, key)
    
    def delete(self, key):
        """Delete with rebalancing"""
        self.root, deleted = self._delete_recursive(self.root, key)
        if deleted:
            self.size -= 1
        return deleted
    
    def _delete_recursive(self, node, key):
        if node is None:
            return None, False
        
        if key < node.key:
            node.left, deleted = self._delete_recursive(node.left, key)
        elif key > node.key:
            node.right, deleted = self._delete_recursive(node.right, key)
        else:
            # Node found
            if node.left is None:
                return node.right, True
            elif node.right is None:
                return node.left, True
            
            min_node = self._find_min(node.right)
            node.key = min_node.key
            node.value = min_node.value
            node.right, _ = self._delete_recursive(node.right, min_node.key)
            deleted = True
        
        if not deleted or node is None:
            return node, deleted
        
        # Update height and rebalance
        node.height = 1 + max(self._get_height(node.left), 
                              self._get_height(node.right))
        balance = self._get_balance(node)
        
        # Rebalance after deletion
        if balance > 1 and self._get_balance(node.left) >= 0:
            return self._rotate_right(node), True
        if balance > 1 and self._get_balance(node.left) < 0:
            node.left = self._rotate_left(node.left)
            return self._rotate_right(node), True
        if balance < -1 and self._get_balance(node.right) <= 0:
            return self._rotate_left(node), True
        if balance < -1 and self._get_balance(node.right) > 0:
            node.right = self._rotate_right(node.right)
            return self._rotate_left(node), True
        
        return node, deleted
    
    def _find_min(self, node):
        while node.left:
            node = node.left
        return node
    
    def _get_height(self, node):
        return node.height if node else 0
    
    def _get_balance(self, node):
        return self._get_height(node.left) - self._get_height(node.right) if node else 0
    
    def _rotate_left(self, z):
        y = z.right
        T2 = y.left
        y.left = z
        z.right = T2
        z.height = 1 + max(self._get_height(z.left), self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))
        return y
    
    def _rotate_right(self, z):
        y = z.left
        T3 = y.right
        y.right = z
        z.left = T3
        z.height = 1 + max(self._get_height(z.left), self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))
        return y
    
    def get_height(self):
        return self._get_height(self.root)
    
    def get_all_items(self):
        """Get all key-value pairs"""
        items = []
        self._inorder_traversal(self.root, items)
        return items
    
    def _inorder_traversal(self, node, items):
        if node:
            self._inorder_traversal(node.left, items)
            items.append((node.key, node.value))
            self._inorder_traversal(node.right, items)
    
    def clear(self):
        self.root = None
        self.size = 0
        self.rotation_count = 0