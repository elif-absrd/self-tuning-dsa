from .bst import BST
from .avl import AVL
from .hashmap import HashMap
from .stats_collector import StatsCollector
from .decision_engine import DecisionEngine
import time


class SelfTuningMap:
    """
    Main orchestrator - the self-tuning data structure.
    Automatically switches between BST, AVL, and HashMap based on workload.
    """
    
    def __init__(self, initial_structure='BST'):
        # Initialize with BST by default
        self.current_structure = initial_structure
        self.structures = {
            'BST': BST(),
            'AVL': AVL(),
            'HashMap': HashMap()
        }
        self.active_ds = self.structures[initial_structure]
        
        # Monitoring components
        self.stats = StatsCollector()
        self.decision_engine = DecisionEngine()
        
        # Metrics
        self.migration_count = 0
        self.total_migration_time = 0
    
    def insert(self, key, value):
        """Insert operation with monitoring"""
        start = time.time()
        result = self.active_ds.insert(key, value)
        duration = time.time() - start
        
        self.stats.record_insert(key, duration)
        self._maybe_switch()
        return result
    
    def search(self, key):
        """Search operation with monitoring"""
        start = time.time()
        result = self.active_ds.search(key)
        duration = time.time() - start
        
        self.stats.record_search(key, duration)
        self._maybe_switch()
        return result
    
    def delete(self, key):
        """Delete operation with monitoring"""
        start = time.time()
        result = self.active_ds.delete(key)
        duration = time.time() - start
        
        self.stats.record_delete(key, duration)
        self._maybe_switch()
        return result
    
    def _maybe_switch(self):
        """Check if we should switch data structures"""
        total_ops = self.stats.total_inserts + self.stats.total_searches + self.stats.total_deletes
        
        if not self.decision_engine.should_check(total_ops):
            return
        
        # Get current stats
        stats_summary = self.stats.get_summary()
        
        # Get current height if tree-based
        current_height = None
        if self.current_structure in ['BST', 'AVL']:
            current_height = self.active_ds.get_height()
        
        # Ask decision engine
        should_switch, target, reason = self.decision_engine.decide_structure(
            self.current_structure,
            stats_summary,
            current_height
        )
        
        if should_switch and target != self.current_structure:
            self._migrate_to(target, reason, total_ops)
    
    def _migrate_to(self, target_structure, reason, total_ops):
        """Migrate data to new structure"""
        print(f"\n🔄 SWITCHING: {self.current_structure} → {target_structure}")
        print(f"   Reason: {reason}")
        
        start = time.time()
        
        # Get all data from current structure
        items = self.active_ds.get_all_items()
        
        # Clear target structure and insert all items
        target_ds = self.structures[target_structure]
        target_ds.clear()
        
        for key, value in items:
            target_ds.insert(key, value)
        
        # Switch active structure
        self.current_structure = target_structure
        self.active_ds = target_ds
        
        # Record metrics
        migration_time = time.time() - start
        self.migration_count += 1
        self.total_migration_time += migration_time
        
        self.decision_engine.record_switch(
            self.current_structure,
            target_structure,
            reason,
            total_ops
        )
        
        print(f"   Migration completed in {migration_time*1000:.2f}ms")
        print(f"   Migrated {len(items)} items\n")
    
    def get_current_structure(self):
        """Get name of current structure"""
        return self.current_structure
    
    def get_stats(self):
        """Get all statistics"""
        stats = self.stats.get_summary()
        stats['current_structure'] = self.current_structure
        stats['migration_count'] = self.migration_count
        stats['total_migration_time'] = self.total_migration_time
        stats['switch_history'] = self.decision_engine.get_switch_history()
        
        # Add structure-specific stats
        if self.current_structure in ['BST', 'AVL']:
            stats['tree_height'] = self.active_ds.get_height()
            if self.current_structure == 'AVL':
                stats['rotation_count'] = self.active_ds.rotation_count
        elif self.current_structure == 'HashMap':
            stats['load_factor'] = self.active_ds.get_load_factor()
            stats['collision_rate'] = self.active_ds.get_collision_rate()
        
        return stats
    
    def force_switch(self, target_structure):
        """Manually force a switch (for experimentation)"""
        if target_structure not in self.structures:
            raise ValueError(f"Unknown structure: {target_structure}")
        
        if target_structure != self.current_structure:
            total_ops = self.stats.total_inserts + self.stats.total_searches
            self._migrate_to(target_structure, "Manual switch", total_ops)