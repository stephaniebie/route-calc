# handles the Uncertainty and Unexpected Events (dynamic solution) over the map
# atleast 3 pairs of nodes must have extreme events such as 
#route blockage,severe delays (10x or more)
#model the above using discrete distributions such that 80% chance no disruption and 20% of major disruption, use random module to simulate
# implement Dijkstra's algorithm to find the optimal path considering these dynamic disruptions

# use the visualize.py module to visualize the dynamic routing results
# Dynamic_Routing.py
import random

def sample_event_edges(graph, num_events=3):
    #using set to capture unique undirected edges
    edges = set()
    for u in graph:
        for v, _ in graph[u]:
            edge = tuple(sorted((u, v)))
            edges.add(edge)
    edges = list(edges)
    return random.sample(edges, num_events)


def sample_event_outcomes(event_edges, prob=0.2):
    """
    Generate an outcomes dict for the given event_edges.
    This is useful when you want to apply the exact same random
    realization to multiple graph variants (e.g. base and rush).
    """
    outcomes = {}
    for i, edge in enumerate(event_edges):
        if i == 0:
            outcomes[edge] = {"action": "delay", "triggered": (random.random() < prob)}
        else:
            outcomes[edge] = {"action": "block", "triggered": (random.random() < prob)}
    return outcomes

def uncertain_events_on_edges(graph, event_edges, outcomes=None, prob=0.2):
    """
    Apply uncertain events to `graph` given `event_edges`.

    - If `outcomes` is None, a new outcomes dict is sampled and used.
      The outcomes dict maps each undirected edge tuple -> {"action":"delay"|"block", "triggered": bool}.
    - If `outcomes` is provided, it must be in the same format and will
      be used so multiple graphs (e.g. base and rush) can share the same
      event realizations.
    """
    # If outcomes not provided, sample once here and reuse for both directions
    if outcomes is None:
        outcomes = {}
        for i, edge in enumerate(event_edges):
            if i == 0:
                outcomes[edge] = {"action": "delay", "triggered": (random.random() < prob)}
            else:
                outcomes[edge] = {"action": "block", "triggered": (random.random() < prob)}

    # Build new graph applying the pre-sampled outcomes symmetrically
    new_graph = {u: [] for u in graph}
    for u in graph:
        for v, w in graph[u]:
            edge = tuple(sorted((u, v)))
            outcome = outcomes.get(edge)
            if outcome:
                if outcome["action"] == "delay" and outcome["triggered"]:
                    # apply severe delay
                    print(f"Severe delay on edge {edge}")
                    w = w * 10
                elif outcome["action"] == "block" and outcome["triggered"]:
                    # blocked edge: skip adding this directed entry (both
                    # directions will be skipped because we use the same outcome
                    # when we encounter the reverse edge)
                    continue
            new_graph[u].append((v, w))

    return new_graph
