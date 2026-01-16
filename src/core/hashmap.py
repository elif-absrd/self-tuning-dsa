class HashMap:
    """Hash Map with chaining for collision resolution"""
    
    def __init__(self, initial_capacity=16):
        self.capacity = initial_capacity
        self.size = 0
        self.buckets = [[] for _ in range(self.capacity)]
        self.collision_count = 0
    
    def _hash(self, key):
        """Hash function"""
        return hash(key) % self.capacity
    
    def insert(self, key, value):
        """Insert key-value pair"""
        index = self._hash(key)
        bucket = self.buckets[index]
        
        # Check if key exists
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return False
        
        # New key
        if len(bucket) > 0:
            self.collision_count += 1
        
        bucket.append((key, value))
        self.size += 1
        
        # Rehash if load factor > 0.75
        if self.size / self.capacity > 0.75:
            self._rehash()
        
        return True
    
    def search(self, key):
        """Search for key"""
        index = self._hash(key)
        bucket = self.buckets[index]
        
        for k, v in bucket:
            if k == key:
                return v
        return None
    
    def delete(self, key):
        """Delete key"""
        index = self._hash(key)
        bucket = self.buckets[index]
        
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket.pop(i)
                self.size -= 1
                return True
        return False
    
    def _rehash(self):
        """Double capacity and rehash all items"""
        old_buckets = self.buckets
        self.capacity *= 2
        self.buckets = [[] for _ in range(self.capacity)]
        self.size = 0
        self.collision_count = 0
        
        for bucket in old_buckets:
            for key, value in bucket:
                self.insert(key, value)
    
    def get_all_items(self):
        """Get all key-value pairs"""
        items = []
        for bucket in self.buckets:
            items.extend(bucket)
        return items
    
    def get_load_factor(self):
        """Current load factor"""
        return self.size / self.capacity if self.capacity > 0 else 0
    
    def get_collision_rate(self):
        """Collision rate"""
        return self.collision_count / self.size if self.size > 0 else 0
    
    def clear(self):
        """Clear all items"""
        self.buckets = [[] for _ in range(self.capacity)]
        self.size = 0
        self.collision_count = 0