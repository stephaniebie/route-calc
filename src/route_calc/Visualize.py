import networkx as nx
import matplotlib.pyplot as plt
from Route import load_adjacencylist_from_csv
from Map import rush_hour_graph, dijkstra_shortest_path, build_the_path
from Dynamic_Routing import sample_event_edges, uncertain_events_on_edges

def build_nx_graph(adj):
    G = nx.Graph()
    for u, edges in adj.items():
        for v, w in edges:
            G.add_edge(u, v, weight=w)
    return G

def subplot_shortest_path(ax, graph, start, end, scenario_label, event_edges=None):
    dist, prev = dijkstra_shortest_path(graph, start)
    path = build_the_path(prev, start, end)
    G = build_nx_graph(graph)
    path_edges = set(zip(path, path[1:]))
    pos = nx.spring_layout(G, seed=42, k=1.2, iterations=100)

    nx.draw_networkx_nodes(G, pos, node_color="#89bdd3", node_size=300, ax=ax)
    nx.draw_networkx_labels(
        G, pos, font_size=5, font_weight="semibold", font_color="#222", ax=ax
    )
    nx.draw_networkx_edges(
        G, pos,
        edgelist=[e for e in G.edges() if e not in path_edges and (e[1], e[0]) not in path_edges],
        edge_color="lightgray", width=1.3, ax=ax
    )
    nx.draw_networkx_edges(
        G, pos,
        edgelist=list(path_edges),
        edge_color="#e04836", width=3, ax=ax
    )

    # Standard edge labels
    edge_labels = {(u, v): f"{d['weight']:.1f}" for u, v, d in G.edges(data=True)}
    nx.draw_networkx_edge_labels(
        G, pos, edge_labels=edge_labels, font_size=6,
        font_color="#111", verticalalignment='bottom', horizontalalignment='center', ax=ax,
        bbox=dict(facecolor="white", edgecolor="none", alpha=0.6, pad=0.1)
    )

    # Highlight chosen event edges' weights in red
    if event_edges:
        for u, v in G.edges():
            edge = tuple(sorted((u, v)))
            if edge in event_edges:
                x = (pos[u][0] + pos[v][0]) / 2
                y = (pos[u][1] + pos[v][1]) / 2
                weight = G[u][v]['weight']
                ax.text(x, y, f"{weight:.1f}", color='red', fontsize=5,
                        fontweight='bold', ha='center', va='center',
                        bbox=dict(facecolor="white", edgecolor="none", alpha=0.6, pad=0.1))

    # Display the path and travel times at the bottom of the plot
    path_str = " → ".join([f"{node}({G[node][path[i+1]]['weight']:.1f}min)" 
                           for i, node in enumerate(path[:-1])] + [path[-1]])
    ax.text(0.5, -0.05, path_str, transform=ax.transAxes, fontsize=5, ha='center', va='top',
            bbox=dict(facecolor="white", edgecolor="black", alpha=0.7, pad=2))

    ax.set_title(f"{scenario_label}\nShortest: {dist.get(end):.2f} min", fontsize=11, fontweight='semibold')
    ax.axis("off")

def plot_both_directions(fig, axs, graph, start, end, titles, event_edges=None):
    subplot_shortest_path(axs[0], graph, start, end, titles[0], event_edges=event_edges)
    subplot_shortest_path(axs[1], graph, end, start, titles[1], event_edges=event_edges)

if __name__ == "__main__":
    base_graph = load_adjacencylist_from_csv("../../data/routes.csv")
    start = "Fenway Park"
    end = "Massachusetts State House"
    rush_graph = rush_hour_graph(base_graph)
    event_edges = sample_event_edges(base_graph, 3)
    print(f"Selected event edges: {event_edges}")
    dynamic_graph = uncertain_events_on_edges(base_graph, event_edges)

    dynamic_rush_graph = uncertain_events_on_edges(rush_graph, event_edges)

    # each page with the necessary graph and paths displayed

    pages = [
        ("Base Case",(base_graph, [f"{start} \u2192 {end}",f"{end} \u2192 {start}"]),False),
        ("Rush Hour",(rush_graph, [f" {start} \u2192 {end}",f" {end} \u2192 {start}"]),False),
        ("Base Case + Uncertain Events",(dynamic_graph, [f" {start} \u2192 {end}",f" {end} \u2192 {start}"]),True),
        ("Rush Hour + Uncertain Events",(dynamic_rush_graph, [f" {start} \u2192 {end}",f" {end} \u2192 {start}"]),True),
    ]

    # create single figure with two subplots (left/right)
    fig, axs = plt.subplots(1, 2, figsize=(14, 6))
    plt.subplots_adjust(bottom=0.18, wspace=0.25)

    current = {"idx": 0}  # mutable container for closures

    def draw_current_page():
        # clear axes
        for ax in axs:
            ax.clear()

        title, (graph, titles_pair), highlight = pages[current["idx"]]
        # draw both directions using your helper
        plot_both_directions(fig, axs, graph, start, end, titles_pair, event_edges=event_edges if highlight else None)
        fig.suptitle(title, fontsize=15)
        # page indicator
        page_text.set_text(f"Page {current['idx']+1} / {len(pages)}")
        plt.draw()

    # create Prev / Next buttons and page label
    axprev = plt.axes([0.28, 0.04, 0.12, 0.06])  # left, bottom, width, height
    axnext = plt.axes([0.6, 0.04, 0.12, 0.06])
    axlabel = plt.axes([0.44, 0.04, 0.12, 0.06])
    bprev = plt.Button(axprev, '\u25C0 Prev')
    bnext = plt.Button(axnext, 'Next \u25B6')
    # small invisible axes for the page label (we'll place text on it)
    axlabel.axis('off')
    page_text = axlabel.text(0.5, 0.5, "", ha='center', va='center', fontsize=10, fontweight='semibold')

    def on_prev(event=None):
        current["idx"] = (current["idx"] - 1) % len(pages)
        draw_current_page()

    def on_next(event=None):
        current["idx"] = (current["idx"] + 1) % len(pages)
        draw_current_page()

    bprev.on_clicked(on_prev)
    bnext.on_clicked(on_next)

    # keyboard support: left/right arrows
    def on_key(event):
        if event.key in ("left", "arrowleft"):
            on_prev(event)
        elif event.key in ("right", "arrowright"):
            on_next(event)

    fig.canvas.mpl_connect("key_press_event", on_key)
    draw_current_page()
    plt.show()
