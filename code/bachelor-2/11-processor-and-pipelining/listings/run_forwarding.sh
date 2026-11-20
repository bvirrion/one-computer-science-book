# capture: session copy=pipeline.py,predictor.py,forwarding.py,forwarding.S,exo_x0.S
python forwarding.py forwarding.S
python forwarding.py exo_x0.S --forget-x0
