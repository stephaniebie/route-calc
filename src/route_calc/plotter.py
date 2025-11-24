from plotly import colors
from route_calc.map import Map
import plotly.graph_objects as go


def plot_map(
    map: Map, show_edges: bool = True, colorway: list = colors.qualitative.Plotly
) -> go.Figure:
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
                    x=1,
                    y=1.05,
                    xanchor="left",
                    yanchor="bottom",
                    showactive=False,
                    buttons=buttons,
                )
            ]
        )
    return fig
