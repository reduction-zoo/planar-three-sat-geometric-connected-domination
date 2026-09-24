"""Experimental drawing pipeline with input-dependent exact flow computations."""
import importlib.util
from pathlib import Path
import networkx as nx
from tsmpy.planarization import Planarization
from tsmpy.orthogonalization import Orthogonalization
from tsmpy.compaction import Compaction

ROOT = Path(__file__).parents[2]
spec = importlib.util.spec_from_file_location('exact_flow', ROOT / 'rounds/026/exact_flow.py')
exact_flow = importlib.util.module_from_spec(spec)
spec.loader.exec_module(exact_flow)


def nested(flow):
    result = {}
    for (u, v, key), value in flow.items():
        result.setdefault(u, {}).setdefault(v, {})[key] = value
    return result


class ExactShape(Orthogonalization):
    def tamassia_orthogonalization(self):
        graph = self.flow_network.copy()
        demand = {v: graph.nodes[v]['demand'] for v in graph}
        for u, v, data in graph.edges(data=True):
            demand[u] += data['lowerbound']
            demand[v] -= data['lowerbound']
        supply = sum(-d for d in demand.values() if d < 0)
        for u, v, data in graph.edges(data=True):
            if data['capacity'] == 2**32:
                data['capacity'] = data['lowerbound'] + supply
        answer = exact_flow.min_cost_flow(graph)
        self.flow_network.cost = sum(answer[u, v, key] * data['weight'] for u, v, key, data in graph.edges(keys=True, data=True))
        return nested(answer)


class ExactMetrics(Compaction):
    def tidy_rectangle_compaction(self, halfedge_side):
        answer = {}
        for direction in (0, 1):
            graph = nx.MultiDiGraph()
            source, sink = self.dcel.ext_face.id, ('face', 'end')
            for he, side in halfedge_side.items():
                if side == direction:
                    left, right = he.twin.inc, he.inc
                    graph.add_edge(left.id, sink if right.is_external else right.id, key=he.id, lowerbound=1, weight=1)
            if not graph:
                continue
            assert nx.is_directed_acyclic_graph(graph)
            assert nx.descendants(graph, source) | {source} == set(graph)
            assert nx.ancestors(graph, sink) | {sink} == set(graph)
            supply = len(graph.edges)
            nx.set_node_attributes(graph, 0, 'demand')
            graph.nodes[source]['demand'] = -supply
            graph.nodes[sink]['demand'] = supply
            nx.set_edge_attributes(graph, supply, 'capacity')
            graph.add_edge(source, sink, key='extend_edge', lowerbound=0, capacity=supply, weight=0)
            flow = exact_flow.min_cost_flow(graph)
            for he, side in halfedge_side.items():
                if side == direction:
                    right = he.inc
                    value = flow[he.twin.inc.id, sink if right.is_external else right.id, he.id]
                    answer[he] = answer[he.twin] = value
        return answer


def layout(graph):
    compaction = ExactMetrics(ExactShape(Planarization(graph)))
    return compaction.G, compaction.pos
