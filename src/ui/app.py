import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from core.self_tuning_map import SelfTuningMap
from utils.workload_generator import WorkloadGenerator


st.set_page_config(page_title="Self-Tuning Data Structure", layout="wide")

# Initialize session state
if 'stm' not in st.session_state:
    st.session_state.stm = SelfTuningMap(initial_structure='BST')
    st.session_state.history = {
        'operations': [],
        'search_ratio': [],
        'order_score': [],
        'structure': [],
        'height': []
    }


def run_workload(operations):
    """Execute a list of operations"""
    for op_type, key, value in operations:
        if op_type == 'insert':
            st.session_state.stm.insert(key, value)
        elif op_type == 'search':
            st.session_state.stm.search(key)
        
        # Record history
        stats = st.session_state.stm.get_stats()
        st.session_state.history['operations'].append(stats['total_ops'])
        st.session_state.history['search_ratio'].append(stats['search_ratio'])
        st.session_state.history['order_score'].append(stats['order_score'])
        st.session_state.history['structure'].append(stats['current_structure'])
        
        height = stats.get('tree_height', 0)
        st.session_state.history['height'].append(height)


# Title
st.title("🧠 Self-Tuning Data Structure Visualizer")
st.markdown("*Watch algorithms adapt in real-time*")

# Sidebar - Controls
st.sidebar.header("⚙️ Workload Controls")

workload_type = st.sidebar.selectbox(
    "Select Workload Pattern",
    ["Sorted Inserts", "Random Inserts", "Search-Heavy", "Insert-Heavy", "Evolving Pattern"]
)

n_operations = st.sidebar.slider("Number of Operations", 10, 500, 100)

if st.sidebar.button("🚀 Run Workload", type="primary"):
    # Generate workload
    if workload_type == "Sorted Inserts":
        ops = [(('insert', k, v)) for k, v in WorkloadGenerator.sorted_inserts(n_operations)]
    elif workload_type == "Random Inserts":
        ops = [(('insert', k, v)) for k, v in WorkloadGenerator.random_inserts(n_operations)]
    elif workload_type == "Search-Heavy":
        ops = WorkloadGenerator.search_heavy_workload(n_operations)
    elif workload_type == "Insert-Heavy":
        ops = WorkloadGenerator.insert_heavy_workload(n_operations)
    else:  # Evolving
        ops = WorkloadGenerator.evolving_workload()
    
    run_workload(ops)
    st.sidebar.success(f"✅ Executed {len(ops)} operations")

if st.sidebar.button("🔄 Reset"):
    st.session_state.stm = SelfTuningMap(initial_structure='BST')
    st.session_state.history = {
        'operations': [],
        'search_ratio': [],
        'order_score': [],
        'structure': [],
        'height': []
    }
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.markdown("### Manual Control")
manual_key = st.sidebar.number_input("Key", value=0, step=1)
manual_value = st.sidebar.text_input("Value", "test_value")

col1, col2 = st.sidebar.columns(2)
if col1.button("Insert"):
    st.session_state.stm.insert(manual_key, manual_value)
    st.rerun()
if col2.button("Search"):
    result = st.session_state.stm.search(manual_key)
    st.sidebar.write(f"Result: {result}")

# Main content
stats = st.session_state.stm.get_stats()

# Current Structure Display
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Current Structure", stats['current_structure'])
with col2:
    st.metric("Total Operations", stats['total_ops'])
with col3:
    st.metric("Switches", stats['migration_count'])

# Metrics row
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Search Ratio", f"{stats['search_ratio']:.2%}")
with col2:
    st.metric("Order Score", f"{stats['order_score']:.2f}")
with col3:
    if 'tree_height' in stats:
        st.metric("Tree Height", stats['tree_height'])
    elif 'load_factor' in stats:
        st.metric("Load Factor", f"{stats['load_factor']:.2f}")
with col4:
    if 'rotation_count' in stats:
        st.metric("Rotations (AVL)", stats['rotation_count'])
    elif 'collision_rate' in stats:
        st.metric("Collision Rate", f"{stats['collision_rate']:.2%}")

# Graphs
if len(st.session_state.history['operations']) > 1:
    st.markdown("---")
    st.subheader("📊 Live Metrics")
    
    # Create dataframe
    df = pd.DataFrame(st.session_state.history)
    
    # Search Ratio Graph
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(
        x=df['operations'],
        y=df['search_ratio'],
        mode='lines',
        name='Search Ratio',
        line=dict(color='#FF6B6B', width=2)
    ))
    fig1.update_layout(
        title="Search Ratio Over Time",
        xaxis_title="Operations",
        yaxis_title="Search Ratio",
        height=300
    )
    st.plotly_chart(fig1, use_container_width=True)
    
    # Order Score Graph
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(
        x=df['operations'],
        y=df['order_score'],
        mode='lines',
        name='Order Score',
        line=dict(color='#4ECDC4', width=2)
    ))
    fig2.update_layout(
        title="Order Score Over Time",
        xaxis_title="Operations",
        yaxis_title="Order Score",
        height=300
    )
    st.plotly_chart(fig2, use_container_width=True)
    
    # Structure Timeline
    st.subheader("🔄 Structure Switches")
    if stats['switch_history']:
        for switch in stats['switch_history']:
            st.info(f"**Op {switch['at_operation']}**: {switch['from']} → {switch['to']} | *{switch['reason']}*")
    else:
        st.write("No switches yet. Run more operations!")

# Footer
st.markdown("---")
st.markdown("*Built for learning. Experiment with different patterns and watch the magic happen.*")