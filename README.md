# Simple Chart Plotter

A Python tool that generates basic charts from CSV data using matplotlib and seaborn.

## Charts

- Line chart
- Bar chart
- Scatter plot
- Pie chart
- Histogram
- Dashboard (all in one)

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install matplotlib seaborn pandas numpy streamlit pillow
```

## Usage

**Generate charts (saves PNGs to `outputs/`)**
```bash
python3 main.py
```

**Launch web UI**
```bash
streamlit run app.py
```

Then open `http://localhost:8501` in your browser.

## Project Structure

```
Simple-Chart-Plotter/
├── SimpleChartPlotter.py   # Chart plotter class
├── main.py                 # Run all charts
├── app.py                  # Streamlit web UI
├── data/
│   └── ornek.csv           # Sample dataset
└── outputs/                # Generated PNGs
```

## Dataset

Sample data contains monthly sales figures across 5 Turkish regions:
Marmara, İç Anadolu, Ege, Karadeniz, Güneydoğu Anadolu.
