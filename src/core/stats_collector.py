from collections import deque
import time


class StatsCollector:
    """Collects and analyzes workload statistics"""
    
    def __init__(self, window_size=100):
        self.window_size = window_size
        self.recent_ops = deque(maxlen=window_size)
        
        # Counters
        self.total_inserts = 0
        self.total_searches = 0
        self.total_deletes = 0
        
        # Key analysis
        self.inserted_keys = []
        self.max_key = None
        self.min_key = None
        
        # Timing
        self.operation_times = []
        
    def record_insert(self, key, duration=0):
        """Record an insert operation"""
        self.recent_ops.append('insert')
        self.total_inserts += 1
        self.inserted_keys.append(key)
        self.operation_times.append(duration)
        
        if self.max_key is None or key > self.max_key:
            self.max_key = key
        if self.min_key is None or key < self.min_key:
            self.min_key = key
    
    def record_search(self, key, duration=0):
        """Record a search operation"""
        self.recent_ops.append('search')
        self.total_searches += 1
        self.operation_times.append(duration)
    
    def record_delete(self, key, duration=0):
        """Record a delete operation"""
        self.recent_ops.append('delete')
        self.total_deletes += 1
        self.operation_times.append(duration)
    
    def get_search_ratio(self):
        """Calculate ratio of searches in recent window"""
        if not self.recent_ops:
            return 0.0
        searches = sum(1 for op in self.recent_ops if op == 'search')
        return searches / len(self.recent_ops)
    
    def get_insert_ratio(self):
        """Calculate ratio of inserts in recent window"""
        if not self.recent_ops:
            return 0.0
        inserts = sum(1 for op in self.recent_ops if op == 'insert')
        return inserts / len(self.recent_ops)
    
    def get_order_score(self):
        """
        Calculate how sorted the inserted keys are.
        Returns value between 0 (random) and 1 (perfectly sorted)
        """
        if len(self.inserted_keys) < 10:
            return 0.5  # Not enough data
        
        # Check last N keys
        recent_keys = self.inserted_keys[-min(50, len(self.inserted_keys)):]
        
        # Count ascending pairs
        ascending = sum(1 for i in range(len(recent_keys)-1) 
                       if recent_keys[i] < recent_keys[i+1])
        
        # Count descending pairs
        descending = sum(1 for i in range(len(recent_keys)-1) 
                        if recent_keys[i] > recent_keys[i+1])
        
        total_pairs = len(recent_keys) - 1
        
        # High order score = mostly sorted (ascending or descending)
        order_score = max(ascending, descending) / total_pairs
        return order_score
    
    def is_sorted_workload(self, threshold=0.7):
        """Determine if workload is sorted"""
        return self.get_order_score() > threshold
    
    def is_search_heavy(self, threshold=0.6):
        """Determine if workload is search-heavy"""
        return self.get_search_ratio() > threshold
    
    def get_avg_operation_time(self):
        """Get average operation time"""
        if not self.operation_times:
            return 0
        recent_times = self.operation_times[-100:]
        return sum(recent_times) / len(recent_times)
    
    def get_summary(self):
        """Get statistics summary"""
        return {
            'total_ops': self.total_inserts + self.total_searches + self.total_deletes,
            'inserts': self.total_inserts,
            'searches': self.total_searches,
            'deletes': self.total_deletes,
            'search_ratio': self.get_search_ratio(),
            'insert_ratio': self.get_insert_ratio(),
            'order_score': self.get_order_score(),
            'is_sorted': self.is_sorted_workload(),
            'is_search_heavy': self.is_search_heavy(),
            'avg_time': self.get_avg_operation_time()
        }
    
    def reset(self):
        """Reset all statistics"""
        self.recent_ops.clear()
        self.total_inserts = 0
        self.total_searches = 0
        self.total_deletes = 0
        self.inserted_keys = []
        self.max_key = None
        self.min_key = None
        self.operation_times = []