class DecisionEngine:
    """
    Decides when and which data structure to switch to.
    This is the brain of the self-tuning system.
    """
    
    def __init__(self):
        self.check_interval = 50  # Check every N operations
        self.min_ops_before_switch = 100  # Minimum ops before first switch
        self.switch_cooldown = 200  # Ops to wait after a switch
        
        # Thresholds
        self.sorted_threshold = 0.7  # Order score threshold
        self.search_heavy_threshold = 0.6
        
        self.last_switch_at = 0
        self.switch_history = []
    
    def should_check(self, total_ops):
        """Should we check for a switch now?"""
        if total_ops < self.min_ops_before_switch:
            return False
        
        # Cooldown after switch
        if total_ops - self.last_switch_at < self.switch_cooldown:
            return False
        
        return total_ops % self.check_interval == 0
    
    def decide_structure(self, current_structure, stats_summary, current_height=None):
        """
        Decide which structure should be used.
        Returns: (should_switch: bool, target_structure: str, reason: str)
        """
        order_score = stats_summary['order_score']
        search_ratio = stats_summary['search_ratio']
        total_ops = stats_summary['total_ops']
        
        # Decision logic
        
        # Case 1: Sorted workload detected → Use AVL
        if order_score > self.sorted_threshold:
            if current_structure == 'BST':
                # BST degrading on sorted data
                if current_height and current_height > 15:  # Arbitrary threshold
                    return True, 'AVL', f'High order score ({order_score:.2f}) + tree height {current_height}'
            elif current_structure == 'HashMap':
                # HashMap is fine for sorted, but if we're insert-heavy, AVL might be better
                if stats_summary['insert_ratio'] > 0.5:
                    return True, 'AVL', f'Sorted inserts detected (order: {order_score:.2f})'
        
        # Case 2: Search-heavy + random keys → Use HashMap
        if search_ratio > self.search_heavy_threshold and order_score < 0.5:
            if current_structure != 'HashMap':
                return True, 'HashMap', f'Search-heavy ({search_ratio:.2f}) with random keys'
        
        # Case 3: Balanced workload with low order → HashMap
        if order_score < 0.4 and search_ratio > 0.4:
            if current_structure != 'HashMap':
                return True, 'HashMap', f'Random access pattern (order: {order_score:.2f})'
        
        # Case 4: BST degrading (high height) → Switch to AVL
        if current_structure == 'BST' and current_height and current_height > 20:
            return True, 'AVL', f'BST height too high ({current_height})'
        
        # No switch needed
        return False, current_structure, 'No switch needed'
    
    def record_switch(self, from_structure, to_structure, reason, total_ops):
        """Record a structure switch"""
        self.last_switch_at = total_ops
        self.switch_history.append({
            'from': from_structure,
            'to': to_structure,
            'reason': reason,
            'at_operation': total_ops
        })
    
    def get_switch_history(self):
        """Get all switches"""
        return self.switch_history