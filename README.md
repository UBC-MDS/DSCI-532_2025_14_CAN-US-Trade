# Canada-U.S. Trade Relations Dashboard

Welcome to the **Canada-U.S. Trade Relations Dashboard** repository!  
This interactive dashboard provides **data-driven insights into the trade relationship between Canada and the U.S.**, helping users analyze trade trends, net trade balances, and industry-specific impacts.

![Dashboard Preview](img/demo.gif)  

---

## **🌍 Live Dashboard**

You can access the deployed version of the dashboard here:  
➡️ **[CAN-US Trade Relations Dashboard](https://dsci-532-2025-14-can-us-trade.onrender.com/)**

---

## **📌 The Problem**

In January 2025, the **United States proposed a 25% tariff on nearly all Canadian imports**, citing concerns over trade imbalances. Given that the **U.S. is Canada’s largest trading partner**, this policy change could have significant economic consequences.  
Canadian analysts need to **assess industry vulnerabilities, measure potential trade reductions, and anticipate economic impacts** efficiently.  

However, **raw trade data is complex** and difficult to interpret quickly. Decision-makers require an **intuitive tool** to analyze trends and take informed action.

---

## **✅ Our Solution: Interactive Trade Dashboard**

To address this, we built an **interactive dashboard** that:  
✔ **Visualizes historical trade data** for Canada and the U.S.  
✔ **Breaks down net trade balance** by industry and region.  
✔ **Allows filtering by year, province, and trade type.**  
✔ **Presents clear insights** for economists, policymakers, and the general public.  

---

## **👨‍💻 About the Developers**

This dashboard is developed by **Danish Karlin Isa, Elshaday Yoseph, and Wangkai Zhu**, Master of Data Science (MDS) students at the **University of British Columbia (UBC)**.  

This project is part of **DSCI 532 – Data Visualization II**, a core course in the UBC MDS program.

---

## **📢 Facing Issues?**  

We’d love to hear your feedback! 🚀  
If you encounter a bug or have suggestions for improvement, **please create a new Issue** under the Issues tab, and we’ll address it promptly.

---

## **🛠 Installation & Running the Dashboard Locally**

Follow these steps to **set up and run the dashboard on your local machine**.

### **🔹 Prerequisites**
Before running the dashboard, ensure you have the following installed:
- Python **3.11.11** or later  
- Conda **24.11.3** or later  
- Required dependencies listed in `environment.yaml`

---

### **🔹 Steps to Run the Dashboard Locally**
1️⃣ **Clone this GitHub repository**  
```bash
git clone https://github.com/UBC-MDS/DSCI-532_2025_14_CAN-US-Trade.git
cd DSCI-532_2025_14_CAN-US-Trade
```

2️⃣ **Set up the Conda environment**  
```bash
conda env create -f environment.yml
conda activate 532
```

3️⃣ **Run the dashboard**  
```bash
python src/app.py
```

4️⃣ **Access the dashboard**  
- Once the server starts, look for an output like this in your terminal:
  ```
  Dash is running on http://127.0.0.1:8050/
  ```
- Open the link in your **web browser** to view the dashboard.

![Terminal Output](img/terminal_output.png)  

---

## **🛠 Contributing to the Dashboard**

We **welcome contributions!** Here’s how you can contribute:

1. **Clone the repository** using the steps above.  
2. **Create a new branch** and implement your changes.  
3. **Push your branch** and submit a **Pull Request (PR)**.  
4. Our team will review your improvements, and once approved, we’ll merge them!

For more details, see our [CONTRIBUTING.md](https://github.com/UBC-MDS/DSCI-532_2025_14_CAN-US-Trade/blob/main/CONTRIBUTING.md).

---

## **📜 License & Data Source**

### **📊 Dataset**
The dataset used in this dashboard is obtained from **Statistics Canada (StatCan)** and is licensed under the [Statistics Canada Open License](https://www.statcan.gc.ca/en/reference/licence).  
✔ You may use, share, or redistribute the dataset for **both commercial and non-commercial purposes**, provided that proper credit is given.

### **📜 Software License**
The source code is licensed under the **MIT License**.  
See the [LICENSE](https://github.com/UBC-MDS/DSCI-532_2025_14_CAN-US-Trade/blob/main/LICENSE) file for more details.

---