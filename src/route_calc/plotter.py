import networkx as nx
from plotly import colors
from matplotlib import figure
from route_calc.map import Map
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from route_calc.location import Location


def plot_map(
    map: Map, show_edges: bool = True, colorway: list = colors.qualitative.Plotly
) -> go.Figure:
    """
    Visualize a Map object on a geographical map.

    Parameters
    ----------
    map: Map
        A Map object
    show_edges: bool
        Toggles the edges between nodes
    colorway: list
        List of colors to use for each consecutive node (and edges)

    Returns
    -------
    A Plotly Figure object
    """
    traces = []
    for i, (starting_location, connecting_locations) in enumerate(
        map._adjacency_list.items()
    ):
        traces.append(
            go.Scattermap(
                lat=[starting_location.latitude],
                lon=[starting_location.longitude],
                mode="markers+text",
                marker={"size": 15, "color": colorway[i % len(colorway)]},
                showlegend=not show_edges,
                name=starting_location.name,
                legendgroup=starting_location.name if show_edges else "Locations",
                legendgrouptitle_text=(
                    starting_location.name if show_edges else "Locations"
                ),
                text=[starting_location.name],
                textposition="top center",
                hovertemplate=(
                    f"<b>{starting_location.name}</b><br>"
                    "Latitude: %{lat}<br>"
                    "Longitude: %{lon}<extra></extra>"
                ),
            )
        )
        if show_edges is True:
            for location, duration in connecting_locations.items():
                traces.append(
                    go.Scattermap(
                        lat=[starting_location.latitude, location.latitude],
                        lon=[starting_location.longitude, location.longitude],
                        mode="lines",
                        line=(
                            {"width": 2, "color": "black"}
                            if duration == float("inf")
                            else {"width": 1, "color": colorway[i % len(colorway)]}
                        ),
                        name=f"to {location.name}",
                        legendgroup=starting_location.name,
                        legendgrouptitle_text=starting_location.name,
                        visible="legendonly" if duration == float("inf") else True,
                        hovertemplate=(
                            f"<b>{starting_location.name}</b><br>"
                            "Latitude: %{lat}<br>"
                            "Longitude: %{lon}<extra></extra>"
                        ),
                        meta="BLOCKED" if duration == float("inf") else "",
                    )
                )
                traces.append(
                    go.Scattermap(
                        lat=[(starting_location.latitude + location.latitude) / 2],
                        lon=[(starting_location.longitude + location.longitude) / 2],
                        mode="markers+text",
                        marker=(
                            {
                                "size": 0,
                                "color": (
                                    "black"
                                    if duration == float("inf")
                                    else colorway[i % len(colorway)]
                                ),
                            }
                        ),
                        name=(
                            "   BLOCKED"
                            if duration == float("inf")
                            else f"   Duration: {round(duration, 1)} {map.time_units}"
                        ),
                        legendgroup=starting_location.name,
                        legendgrouptitle_text=starting_location.name,
                        visible=False,
                        text=(
                            "BLOCKED"
                            if duration == float("inf")
                            else f"{round(duration, 1)} {map.time_units}"
                        ),
                        textposition="top center",
                        hovertemplate=(
                            "BLOCKED<br>"
                            if duration == float("inf")
                            else f"Duration: {round(duration, 1)} {map.time_units}<br>"
                        )
                        + ("Latitude: %{lat}<br>" "Longitude: %{lon}<extra></extra>"),
                        meta="BLOCKED" if duration == float("inf") else "",
                    )
                )

    fig = go.Figure(
        data=traces,
        layout={
            "map_style": "carto-positron",
            "map_zoom": 12.5,
            "map_center": {
                "lat": sum([l.latitude for l in map._adjacency_list])
                / len(map._adjacency_list),
                "lon": sum([l.longitude for l in map._adjacency_list])
                / len(map._adjacency_list),
            },
            "legend_groupclick": "toggleitem",
        },
    )
    if show_edges is True:
        buttons = [
            dict(
                label="Show Duration",
                method="restyle",
                args=[
                    {
                        "visible": [
                            (
                                False
                                if "Duration" in t.name or "BLOCKED" in t.name
                                else "legendonly" if t.meta == "BLOCKED" else True
                            )
                            for t in fig.data
                        ]
                    }
                ],
                args2=[
                    {
                        "visible": [
                            ("legendonly" if t.meta == "BLOCKED" else True)
                            for t in fig.data
                        ]
                    }
                ],
            )
        ]
        fig.update_layout(
            updatemenus=[
                dict(
                    type="buttons",
                    x=1.01,
                    y=1.02,
                    xanchor="left",
                    yanchor="bottom",
                    showactive=False,
                    buttons=buttons,
                )
            ]
        )
    return fig


def plot_nodes(map: Map) -> figure:
    """
    Visualize a Map object as a network of nodes.

    Parameters
    ----------
    map: Map
        A Map object

    Returns
    -------
    Matplotlib figure
    """
    visual_graph_node = nx.Graph()

    for start, duration_mapping in map._adjacency_list.items():
        for end, duration in duration_mapping.items():
            visual_graph_node.add_edge(start, end, weight=duration)

    fig, ax = plt.subplots(figsize=(12, 8))
    pos = nx.spring_layout(visual_graph_node, seed=37, k=2)

    nx.draw_networkx_nodes(
        visual_graph_node,
        pos,
        node_size=2000,
        node_color="orange",
        edgecolors="black",
        ax=ax,
    )
    nx.draw_networkx_edges(
        visual_graph_node, pos, width=2, alpha=0.6, edge_color="gray", ax=ax
    )
    nx.draw_networkx_labels(
        visual_graph_node, pos, font_size=10, font_weight="bold", ax=ax
    )

    edge_labels = nx.get_edge_attributes(visual_graph_node, "weight")
    nx.draw_networkx_edge_labels(
        visual_graph_node, pos, edge_labels=edge_labels, font_size=9, ax=ax
    )

    ax.set_title("Map visualization")
    return fig


def plot_route(
    maps: list[Map], titles: list[str], start: Location | str, end: Location | str
):
    """
    Plot a route on multiple maps.

    Parameters
    ----------
    maps: list[Map]
        List of Map objects
    titles: list[str]
        List of map titles
    start: Location | str
        Starting location
    end: Location | str
        Ending location
    """

    def build_nx_graph(adj):
        G = nx.Graph()
        for u, edges in adj.items():
            for v, w in edges.items():
                G.add_edge(u.name, v.name, weight=w)
        return G

    def subplot_shortest_path(ax, map_obj, start, end, scenario_label):
        dist = map_obj.calculate_duration(start, end)
        path = map_obj.construct_path(start, end)
        G = build_nx_graph(map_obj._adjacency_list)
        path_edges = set(zip(path, path[1:]))
        pos = nx.spring_layout(G, seed=42, k=1.2, iterations=100)

        nx.draw_networkx_nodes(G, pos, node_color="#89bdd3", node_size=300, ax=ax)
        nx.draw_networkx_labels(
            G, pos, font_size=5, font_weight="semibold", font_color="#222", ax=ax
        )
        nx.draw_networkx_edges(
            G,
            pos,
            edgelist=[
                e
                for e in G.edges()
                if e not in path_edges and (e[1], e[0]) not in path_edges
            ],
            edge_color="lightgray",
            width=1.3,
            ax=ax,
        )
        nx.draw_networkx_edges(
            G, pos, edgelist=list(path_edges), edge_color="#e04836", width=3, ax=ax
        )

        # Standard edge labels
        edge_labels = {(u, v): f"{d['weight']:.1f}" for u, v, d in G.edges(data=True)}
        nx.draw_networkx_edge_labels(
            G,
            pos,
            edge_labels=edge_labels,
            font_size=6,
            font_color="#111",
            verticalalignment="bottom",
            horizontalalignment="center",
            ax=ax,
            bbox=dict(facecolor="white", edgecolor="none", alpha=0.6, pad=0.1),
        )

        # Highlight chosen event edges' weights in red
        # event_edges = set(zip(path, path[1:]))
        event_edges = set(frozenset((u, v)) for u, v in zip(path, path[1:]))

        for u, v in G.edges():
            #edge = tuple(sorted((u, v)))
            edge = frozenset((u, v))
            if edge in event_edges:
                x = (pos[u][0] + pos[v][0]) / 2
                y = (pos[u][1] + pos[v][1]) / 2
                weight = G[u][v]["weight"]
                ax.text(
                    x,
                    y,
                    f"{weight:.1f}",
                    color="red",
                    fontsize=5,
                    fontweight="bold",
                    ha="center",
                    va="center",
                    bbox=dict(facecolor="white", edgecolor="none", alpha=0.6, pad=0.1),
                )

        # Display the path and travel times at the bottom of the plot
        path = [str(p) for p in path]
        path_str = " → ".join(
            [
                f"{node}({G[node][path[i+1]]['weight']:.1f}min)"
                for i, node in enumerate(path[:-1])
            ]
            + [path[-1]]
        )
        ax.text(
            0.5,
            -0.05,
            path_str,
            transform=ax.transAxes,
            fontsize=5,
            ha="center",
            va="top",
            bbox=dict(facecolor="white", edgecolor="black", alpha=0.7, pad=2),
        )

        ax.set_title(
            f"{scenario_label}\nShortest: {dist:.2f} min",
            fontsize=11,
            fontweight="semibold",
        )
        ax.axis("off")

    def plot_both_directions(fig, axs, map_obj, start, end, titles):
        subplot_shortest_path(axs[0], map_obj, start, end, titles[0])
        subplot_shortest_path(axs[1], map_obj, end, start, titles[1])

    # each page with the necessary graph and paths displayed

    pages = [
        (title, (map_obj, [f"{start} \u2192 {end}", f"{end} \u2192 {start}"]))
        for title, map_obj in zip(titles, maps)
    ]

    # create single figure with two subplots (left/right)
    fig, axs = plt.subplots(1, 2, figsize=(14, 6))
    plt.subplots_adjust(bottom=0.18, wspace=0.25)

    current = {"idx": 0}  # mutable container for closures

    def draw_current_page():
        # clear axes
        for ax in axs:
            ax.clear()

        title, (map_obj, titles_pair) = pages[current["idx"]]
        # draw both directions using your helper
        plot_both_directions(fig, axs, map_obj, start, end, titles_pair)
        fig.suptitle(title, fontsize=15)
        # page indicator
        page_text.set_text(f"Page {current['idx']+1} / {len(pages)}")
        plt.draw()

    # create Prev / Next buttons and page label
    axprev = plt.axes([0.28, 0.04, 0.12, 0.06])  # left, bottom, width, height
    axnext = plt.axes([0.6, 0.04, 0.12, 0.06])
    axlabel = plt.axes([0.44, 0.04, 0.12, 0.06])
    bprev = plt.Button(axprev, "\u25c0 Prev")
    bnext = plt.Button(axnext, "Next \u25b6")
    # small invisible axes for the page label (we'll place text on it)
    axlabel.axis("off")
    page_text = axlabel.text(
        0.5, 0.5, "", ha="center", va="center", fontsize=10, fontweight="semibold"
    )

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
    return fig
