# 🧪 DataAssure — Data Validation Framework

![DataAssure Logo](dataassure_logo.png)

**DataAssure** is a lightweight yet powerful **data validation framework** built from scratch in Python using Streamlit.

> ✨ **Inspired by [Great Expectations](https://greatexpectations.io/)**, but built without any external profiling libraries — this is a completely custom, minimal implementation designed for flexibility, ease of use, and quick validation.

It enables users to define expectations on datasets, validate them through a user-friendly web interface, and generate downloadable validation reports — all without writing a line of code.

---

## 🚀 Features

- 📤 Upload CSV files via the web interface  
- 🎛️ Choose from 20+ built-in data validation expectations  
- 🔍 Automatically detect column-based expectations and present dropdowns  
- ✅ Validation powered by a pure Python decorator (`@profile_step`) — no third-party profiling engines  
- 📄 Downloadable `validation_report.txt`  
- 🖼️ Clean UI with centered logo and branding (DataAssure)

---

## 📦 Requirements

Before running the app, make sure you have the following Python libraries installed:

| Library     | Purpose                          |
|-------------|----------------------------------|
| `streamlit` | To build and run the web UI      |
| `pandas`    | For reading and processing data  |

---

## 🧑‍💻 Programmatic Usage (Using as a Decorator)

You can also use `DataAssure` programmatically in any Python script or notebook by importing and applying the `@profile_step` decorator to any function that returns a DataFrame.

### ✅ Example

```python
from profile_step import profile_step
import pandas as pd

@profile_step(
    expect_column_to_exist=["age", "job"],
    expect_no_nulls=["education", "marital"],
    expect_column_mean_to_be_between={"age": (18, 60)},
    expect_column_values_to_be_unique=["id"]
)
def load_data():
    # Simulated or real dataset
    df = pd.read_csv("your_data.csv")
    return df

# Run validation
df_validated = load_data()
```
---
