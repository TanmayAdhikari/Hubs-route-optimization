import pandas as pd
from pulp import *
import gradio as gr

def optimize_distribution(file):
    data = pd.read_csv(file.name)

    # Detect weeks dynamically
    week_cols = [col for col in data.columns if col.startswith('week_')]
    weeks = [int(col.split('_')[1]) for col in week_cols]
    hubs = data['hub_1'].unique()

    # Starting inventory
    starting_inventory = data.groupby('hub_1')['starting_inventory'].first().to_dict()
    cost_dict = {(row['hub_1'], row['hub_2']): row['cost'] for _, row in data.iterrows()}

    # LP model
    model = LpProblem("MultiWeek_Hub_Distribution_Optimization", LpMinimize)
    ship_vars = {}
    unmet_demand = {}
    inventory = {}

    for week in weeks:
        demand = data.groupby('hub_1')[f'week_{week}'].first().to_dict()
        inventory[week] = LpVariable.dicts(f"Inventory_w{week}", hubs, lowBound=0, cat="Integer")
        unmet_demand[week] = LpVariable.dicts(f"UnmetDemand_w{week}", hubs, lowBound=0, cat="Integer")
        ship_vars[week] = LpVariable.dicts(
            f"Shipment_w{week}",
            [(i, j) for i in hubs for j in hubs if i != j],
            lowBound=0, cat="Integer"
        )

        prev_inv = starting_inventory if week == min(weeks) else inventory[week - 1]

        for h in hubs:
            inflow  = lpSum(ship_vars[week][i, j] for (i, j) in ship_vars[week] if j == h)
            outflow = lpSum(ship_vars[week][h, j] for (h_, j) in ship_vars[week] if h_ == h)
            model += inventory[week][h] == (
                (prev_inv[h] if isinstance(prev_inv[h], (int, float)) else prev_inv[h])
                + inflow - outflow - (demand[h] - unmet_demand[week][h])
            )
            model += unmet_demand[week][h] <= demand[h]

    model += (
        lpSum(ship_vars[w][i, j] * cost_dict[(i, j)] for w in weeks for (i, j) in ship_vars[w]) +
        lpSum(unmet_demand[w][h] * 100 for w in weeks for h in hubs)
    )

    model.solve()

    result = f"Status: {LpStatus[model.status]}\n\n"
    for week in weeks:
        result += f"--- Week {week} ---\n"
        for h in hubs:
            result += f"{h} - Inventory End: {inventory[week][h].value()}\n"
            result += f"{h} - Unmet Demand: {unmet_demand[week][h].value()}\n"
        result += "\n"

    return result

# Gradio UI
demo = gr.Interface(
    fn=optimize_distribution,
    inputs=gr.File(label="Upload CSV file with hub data"),
    outputs=gr.Textbox(label="Optimization Result", lines=20),
    title="Multi-week Hub Distribution Optimizer"
)

demo.launch()
