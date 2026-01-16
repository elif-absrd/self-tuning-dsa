# 🧠 Self-Tuning Data Structure

This project demonstrates how data structures can automatically adapt to workload patterns in real-time.
I am still working on this and a lot of things are remaining. for now a basic working of bst and avl and hash map has been completed.



## 🎯 What This Does

Watch in real-time as the system:
- Detects **sorted inserts** → switches to **AVL Tree**
- Detects **search-heavy random access** → switches to **HashMap**
- Detects **BST degradation** → switches to **AVL**
- Tracks metrics and visualizes decision-making

## 🏗️ Architecture

```
Core Engine (Pure Logic)
├── BST (Binary Search Tree)
├── AVL (Self-balancing tree)
├── HashMap (Hash table with chaining)
├── StatsCollector (Workload analysis)
├── DecisionEngine (Switching logic)
└── SelfTuningMap (Orchestrator)

UI Layer (Streamlit)
└── Interactive visualization + controls
```

## 🚀 Quick Start

### 1. Install Dependencies
(after activating you venv)
```bash
pip install -r requirements.txt 
```

### 2. Run the Application
```bash
python run.py
```

Or directly:
```bash
streamlit run src/ui/app.py
```

### 3. Experiment!
- Choose a workload pattern (sorted, random, search-heavy, etc.)
- Watch the structure adapt
- Observe the metrics and switching behavior

## 🧪 Learning Experiments

### Experiment 1: Sorted Inserts
**Hypothesis**: BST will degrade, system switches to AVL

1. Select "Sorted Inserts" workload
2. Run 100 operations
3. Observe:
   - BST height grows linearly
   - Switch triggers when height > threshold
   - AVL maintains balance

### Experiment 2: Search-Heavy Random
**Hypothesis**: System switches to HashMap for O(1) lookups

1. Select "Search-Heavy" workload
2. Run 200 operations
3. Observe:
   - Search ratio climbs
   - Random key pattern detected
   - Switch to HashMap

### Experiment 3: Evolving Workload
**Hypothesis**: System adapts as patterns change

1. Select "Evolving Pattern"
2. Watch it transition through phases
3. See multiple switches

## 📊 Metrics Explained

- **Search Ratio**: % of operations that are searches (in recent window)
- **Order Score**: How sorted the insert keys are (0=random, 1=sorted)
- **Tree Height**: Current height of BST/AVL
- **Load Factor**: HashMap fullness (triggers rehashing)

## 🎓 What You'll Learn

- How workload patterns affect data structure performance
- When AVL balancing is worth the overhead
- Why HashMap excels at random access
- Trade-offs between different data structures
- Real-time algorithmic decision-making

## 🛠️ Extending the Project

Ideas for enhancement:
- Add **Red-Black Tree** as another option
- Implement **decay** in stats (recent behavior weighted more)
- Add **cost estimation** before switching
- Compare against **fixed baseline** structures
- Export experiment logs to CSV

## 📝 File Structure

```
src/
├── core/              # Pure logic, no UI
│   ├── bst.py
│   ├── avl.py
│   ├── hashmap.py
│   ├── stats_collector.py
│   ├── decision_engine.py
│   └── self_tuning_map.py
├── ui/
│   └── app.py         # Streamlit interface
└── utils/
    └── workload_generator.py
```

## 🧠 Core Principles

1. **Separation of Concerns**: Core logic is UI-independent
2. **Observable Behavior**: Every decision is visible and explainable
3. **Learning First**: Built for understanding, not just functionality
4. **Experimentation**: Easy to tweak thresholds and test hypotheses

## 🤝 Contributing

This is a learning project! Feel free to:
- Experiment with different switching strategies
- Add new data structures
- Improve the decision logic
- Enhance visualizations

## 📚 Further Reading

- [AVL Trees Explained](https://en.wikipedia.org/wiki/AVL_tree)
- [Hash Tables Deep Dive](https://en.wikipedia.org/wiki/Hash_table)
- [Self-Tuning Databases](https://scholar.google.com/scholar?q=self-tuning+database)

---

**Built for curiosity. Learn by doing. 🚀**