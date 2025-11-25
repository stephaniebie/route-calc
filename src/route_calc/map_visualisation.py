import pandas as pd
from pathlib import Path
import networkx as nx
import matplotlib.pyplot as plt

script_dir = Path(__file__).parent
csv_path = script_dir.parent / "assets" / "routes.csv"
data_frame = pd.read_csv(csv_path)
visual_graph_node = nx.Graph()

for row in data_frame.itertuples():
    visual_graph_node.add_edge(row.start, row.end, weight=row.duration)

plt.figure(figsize=(12, 8))
pos = nx.spring_layout(visual_graph_node, seed=37, k=2)

nx.draw_networkx_nodes(
    visual_graph_node, pos, node_size=2000, node_color="orange", edgecolors="black"
)
nx.draw_networkx_edges(visual_graph_node, pos, width=2,
                       alpha=0.6, edge_color="gray")
nx.draw_networkx_labels(visual_graph_node, pos,
                        font_size=10, font_weight="bold")

edge_labels = nx.get_edge_attributes(visual_graph_node, "weight")
nx.draw_networkx_edge_labels(
    visual_graph_node, pos, edge_labels=edge_labels, font_size=9
)

plt.title("Map visualization")
plt.show()
