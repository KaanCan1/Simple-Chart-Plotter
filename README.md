# TGSS 2024 — Chart Panel

A Python project that automatically generates charts from the Turkey General Social Survey 2024 (n = 2,615) dataset. You can create and view charts through a Streamlit interface.

## Requirements

| Requirement | Minimum version |
|-------------|-----------------|
| Python | 3.10 or higher (3.11 recommended) |
| pip | Latest version |
| Git | For cloning the repo |

An internet connection is required on first setup to download packages.

## Project Structure

```
Simple-Chart-Plotter/
├── app.py                  # Streamlit web interface
├── main.py                 # Chart generation logic
├── SimpleChartPlotter.py   # Chart class (matplotlib)
├── data/
│   └── TGSS2024.csv        # Survey data (included with repo)
├── outputs/                # Generated PNGs (auto-created)
├── requirements.txt
└── README.md
```

## Setup (from scratch)

### 1. Clone the repo

```bash
git clone https://github.com/KaanCan1/Simple-Chart-Plotter.git
cd Simple-Chart-Plotter
```

### 2. Create a virtual environment

macOS / Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows (PowerShell):
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

When the virtual environment is active, you will see the `(.venv)` prefix in your terminal.

### 3. Install dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

Main packages installed: `streamlit`, `matplotlib`, `seaborn`, `pandas`, `numpy`, `scipy`, `pillow`.

### 4. Verify the data file

Make sure `data/TGSS2024.csv` exists. Charts cannot be generated without this file.

## Running the App

### Web interface (recommended)

From the project root folder, with the virtual environment **active**:

```bash
streamlit run app.py
```

The browser opens automatically (usually at `http://localhost:8501`). If it doesn't open, enter that address manually.

Click the **⟳ Generate Charts** button in the interface. Six charts will be saved to the `outputs/` folder and displayed on the page.

- On first run, matplotlib may build its font cache — this is normal and happens only once.
- Subsequent runs typically take only a few seconds.

### Terminal-only chart generation

To generate PNGs directly without Streamlit:

```bash
python main.py
```

Output files: `outputs/line.png`, `bar.png`, `scatter.png`, `pie.png`, `histogram.png`, `dashboard.png`.

## Generated Charts

| File | Description |
|------|-------------|
| `line.png` | Happiness, satisfaction, and health by age group |
| `bar.png` | Average societal threat perception scores |
| `scatter.png` | Social trust × life satisfaction (by gender) |
| `pie.png` | Marital status distribution |
| `histogram.png` | Participant age distribution |
| `dashboard.png` | Three-panel overview |

## Common Issues

### `ModuleNotFoundError` (streamlit, pandas, scipy, etc.)

You are running commands without activating the virtual environment. Run this at the start of every session:

```bash
source .venv/bin/activate   # macOS / Linux
pip install -r requirements.txt
```

### Charts are generating very slowly

- Run commands **inside the virtual environment**; don't mix with the system `python3`.
- Use `streamlit run app.py`; avoid older methods that spawn a new process each time.
- After the first run, `.mpl_cache/` is created and subsequent runs will be faster.

### `FileNotFoundError: data/TGSS2024.csv`

Run the command from the project root directory:

```bash
cd Simple-Chart-Plotter
streamlit run app.py
```

### Port already in use

Start on a different port:

```bash
streamlit run app.py --server.port 8502
```

## Development Notes

- Chart engine: `matplotlib` (`Agg` backend, saves to file).
- Interface: `Streamlit`.
- `outputs/` and `.mpl_cache/` are not tracked by git; they are created at runtime.

## License

This project is for educational / demo purposes. Usage terms for the TGSS data belong to the data owner.
