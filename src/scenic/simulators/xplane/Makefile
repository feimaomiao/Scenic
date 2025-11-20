RUNWAY_PATH="/Users/simeon/Desktop/Repositories/Scenic/examples/xplane/runway.yaml"
SCENIC_FILE="/Users/simeon/Desktop/Repositories/Scenic/examples/xplane/example.scenic"

PHONY: simulator playground

all: simulator

simulator:
	python3 simulator.py --runway $(RUNWAY_PATH) --scenic-file $(SCENIC_FILE)

location:
	python3 location.py