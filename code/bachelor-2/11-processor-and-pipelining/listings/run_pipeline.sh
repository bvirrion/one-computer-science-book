# capture: session copy=pipeline.py,predictor.py,timing_diagram.py,independent.S,load_use.S
python timing_diagram.py independent.S
python timing_diagram.py load_use.S --no-forwarding
python timing_diagram.py load_use.S
