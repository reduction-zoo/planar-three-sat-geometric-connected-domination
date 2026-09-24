"""Expose the finite face-flow capacity independently of graph drawing size."""
import networkx as nx
from tsmpy.flownet import Flow_net

for demand in (2**32, 2**32 + 1):
    graph = Flow_net()
    graph.add_node('left', demand=-demand)
    graph.add_node('right', demand=demand)
    graph.add_f2f('left', 'right', 'edge')
    try:
        result = graph.min_cost_flow()
        assert result['left']['right']['edge'] == demand
        print(demand, 'feasible')
    except nx.NetworkXUnfeasible:
        assert demand > 2**32
        print(demand, 'infeasible from fixed capacity')
