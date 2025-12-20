import matplotlib.pyplot as plt
import pandas as pd
import networkx as nx

# 1) Load CSV (your file has columns: linkSource, linkTarget)
csv_path = "gamegraph.csv"
df = pd.read_csv(csv_path).dropna(subset=["linkSource", "linkTarget"])
df["linkSource"] = df["linkSource"].astype(str).str.strip()
df["linkTarget"] = df["linkTarget"].astype(str).str.strip()

# 2) Build graph (directed; change to nx.Graph() if you want undirected)
G = nx.from_pandas_edgelist(df, source="linkSource", target="linkTarget", create_using=nx.DiGraph())

# (Optional) see exact node names so you can pick what to highlight
print("Nodes:", sorted(G.nodes()))

# 3) Choose what to color red
red_nodes = {
    # put node names here (must match exactly)
    "Wikipedia graph structure",
    "Introduction",
    "Power of the first links",
    "General player behaviour",
}

red_edges = {
    # put directed edges here as (source, target)
    ("Introduction", "Wikipedia graph structure"),
    ("Wikipedia graph structure", "Power of the first links"),
    ("Power of the first links", "General player behaviour"),
}

# 4) Create color/width lists for drawing
node_colors = ["red" if n in red_nodes else "lightgray" for n in G.nodes()]
edge_colors = ["red" if (u, v) in red_edges else "gray" for (u, v) in G.edges()]
edge_widths = [3.0 if (u, v) in red_edges else 1.2 for (u, v) in G.edges()]

# 5) Draw
backbone_order = [
    "Introduction",
    "Wikipedia graph structure",
    "Power of the first links",
    "General player behaviour",
]

pos = {}
for i, n in enumerate(backbone_order):
    pos[n] = (i * 100, 0)   # spacing=3.0, y=0 => a nice straight line

# 2) Layout the rest *around* the fixed backbone
#    (pos gives initial positions; fixed keeps those nodes pinned)
pos = nx.spring_layout(
    G,
    pos=pos,
    fixed=backbone_order,
    seed=42,
    k=0.2,          # increase to spread things out
    iterations=300
)
# pos = nx.kamada_kawai_layout(G, pos=pos)

plt.figure(figsize=(12, 8))

nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=900, edgecolors="black", linewidths=0.6)
nx.draw_networkx_edges(
    G, pos,
    edge_color=edge_colors,
    width=edge_widths,
    arrows=G.is_directed(),
    arrowsize=18,
    connectionstyle="arc3,rad=0.08"  # slight curve helps readability
)
nx.draw_networkx_labels(G, pos, font_size=8)

plt.axis("off")
plt.tight_layout()
plt.show()
