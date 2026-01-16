import random


class WorkloadGenerator:
    """Generates different workload patterns for experimentation"""
    
    @staticmethod
    def sorted_inserts(n, start=0):
        """Generate sorted sequential keys"""
        return [(i + start, f"value_{i}") for i in range(n)]
    
    @staticmethod
    def reverse_sorted_inserts(n, start=1000):
        """Generate reverse sorted keys"""
        return [(start - i, f"value_{i}") for i in range(n)]
    
    @staticmethod
    def random_inserts(n, min_key=0, max_key=10000):
        """Generate random keys"""
        keys = random.sample(range(min_key, max_key), min(n, max_key - min_key))
        return [(k, f"value_{k}") for k in keys]
    
    @staticmethod
    def mixed_workload(n_inserts=100, n_searches=50, keys=None):
        """
        Generate a mixed workload of inserts and searches.
        Returns list of operations: ('insert', key, value) or ('search', key)
        """
        ops = []
        
        # Generate inserts
        if keys is None:
            keys = [random.randint(0, 10000) for _ in range(n_inserts)]
        
        for i, key in enumerate(keys[:n_inserts]):
            ops.append(('insert', key, f"value_{key}"))
        
        # Generate searches (search for existing keys)
        search_keys = random.choices(keys[:n_inserts], k=n_searches)
        for key in search_keys:
            ops.append(('search', key, None))
        
        # Shuffle operations
        random.shuffle(ops)
        return ops
    
    @staticmethod
    def search_heavy_workload(n_inserts=100, search_ratio=0.7):
        """Workload with high search ratio"""
        n_searches = int(n_inserts * search_ratio / (1 - search_ratio))
        keys = [random.randint(0, 10000) for _ in range(n_inserts)]
        return WorkloadGenerator.mixed_workload(n_inserts, n_searches, keys)
    
    @staticmethod
    def insert_heavy_workload(n_inserts=100, search_ratio=0.2):
        """Workload with high insert ratio"""
        n_searches = int(n_inserts * search_ratio / (1 - search_ratio))
        keys = list(range(n_inserts))  # Sorted inserts
        return WorkloadGenerator.mixed_workload(n_inserts, n_searches, keys)
    
    @staticmethod
    def evolving_workload():
        """
        Workload that changes pattern over time.
        Perfect for testing switching behavior.
        """
        ops = []
        
        # Phase 1: Sorted inserts (should trigger AVL)
        print("Phase 1: Sorted inserts")
        for i in range(100):
            ops.append(('insert', i, f"value_{i}"))
        
        # Phase 2: Heavy searches (should stay in AVL or switch to HashMap)
        print("Phase 2: Search-heavy phase")
        for _ in range(200):
            key = random.randint(0, 99)
            ops.append(('search', key, None))
        
        # Phase 3: Random inserts + searches (should trigger HashMap)
        print("Phase 3: Random access pattern")
        for _ in range(150):
            if random.random() < 0.6:
                key = random.randint(1000, 2000)
                ops.append(('search', key, None))
            else:
                key = random.randint(1000, 2000)
                ops.append(('insert', key, f"value_{key}"))
        
        return ops  