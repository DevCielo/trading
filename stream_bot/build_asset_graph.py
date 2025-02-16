import numpy as np
import networkx as nx
import torch
from torch_geometric.data import Data

def build_asset_graph(asset_data: dict) -> Data:
    assets = list(asset_data.keys())
    features = [asset_data[a] for a in assets]
    x = torch.tensor(features, dtype=torch.float)

    # Build an edge list. For demonstration, we might use correlations between asset features.
    # Here, we create a fully connected graph (or use some threshold on correlation).
    edge_index = []
    num_assets = len(assets)
    for i in range(num_assets):
        for j in range(num_assets):
            if i != j:
                edge_index.append([i, j])
    edge_index = torch.tensor(edge_index, dtype=torch.long).t().contiguous()

    data = Data(x=x, edge_index=edge_index)
    return data
