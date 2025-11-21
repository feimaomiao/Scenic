RUNWAY_PATH="/Users/simeon/Desktop/Repositories/Scenic/examples/xplane/runway.yaml"
SCENIC_FILE="/Users/simeon/Desktop/Repositories/Scenic/examples/xplane/example.scenic"

.PHONY: simulator location example

all: simulator

simulator:
	python3 simulator.py --scenic-file $(SCENIC_FILE)

location:
	python3 ./scripts/location.py

example:
	scenic ./example/example.scenic --axes