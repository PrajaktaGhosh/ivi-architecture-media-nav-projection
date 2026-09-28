# Diagram source

All diagrams in `01_Diagrams/` are generated from `generate_diagrams.py` (Python + matplotlib).

```zsh
cd 03_Source
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 generate_diagrams.py ../01_Diagrams
```

Outputs: `D1_IVI_Conceptual_Architecture` (PNG, SVG, PDF), `data_flows/D2-D5` (PNG), `views/D6` (PNG).
