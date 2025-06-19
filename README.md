# Multi-week Hub Distribution Optimizer

This project is a multi-week, multi-hub inventory distribution optimization tool built using **PuLP** and **Gradio**. It helps optimize shipment costs and manage unmet demands over multiple weeks using Mixed-Integer Linear Programming (MILP) .

---


## 🚀 Features

* Handles **any number of weeks** dynamically (e.g., `week_1`, `week_2`, ..., `week_N`).
* Accepts a **CSV upload** with hub-to-hub cost, inventory, and weekly demand.
* Solves a **linear program** using PuLP to minimize:

  * Shipment costs
  * Penalty for unmet demand (default: 100 per unit)
* Returns **week-by-week results**:

  * Inventory left at each hub
  * Unmet demand per hub

---

## 🔧 How to Run

### 1. Clone the repository

```bash
git clone https://github.com/your-username/multiweek-hub-optimizer.git
cd multiweek-hub-optimizer
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the app

```bash
python app.py
```

This will open a Gradio interface in your browser.

---

## 📄 Sample CSV Format

```
hub_1,hub_2,cost,time in days,starting_inventory,week_1,week_2,week_3,week_4
h1,h2,20,1,100,120,80,60,50
h1,h3,25,1,100,120,80,60,50
h2,h1,20,1,110,60,90,40,70
...
```

* `hub_1`: Source hub
* `hub_2`: Destination hub
* `cost`: Cost per unit
* `starting_inventory`: Inventory at `hub_1` at the beginning
* `week_#`: Demand at `hub_1` in that week

You can use the provided `dataset_hub_multiweek.csv` as a reference.

---

## 💡 Notes

* `time in days` is not used in the model (reserved for future extension)
* Shipments between same hubs (`hub_1 == hub_2`) should be excluded
* Unmet demand is penalized heavily to ensure demand satisfaction is prioritized

---

## 👨‍💼 Author

**Tanmay Adhikari**
---

## 🌟 License

MIT License
