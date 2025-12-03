RUNWAY_PATH="/Users/simeon/Desktop/Repositories/Scenic/examples/xplane/runway.yaml"
SCENIC_FILE="./example/example.scenic"

.PHONY: simulator location example

all: simulator

simulate:
	scenic ./example/example.scenic --axes --simulate

simulator:
	python3 simulator.py --scenic-file $(SCENIC_FILE)

location:
	python3 ./scripts/location.py

example:
	scenic ./example/example.scenic --axes

random_location:
	python3 ./scripts/random_location.py --scenic-file $(SCENIC_FILE)

merge:
	git checkout main
	git merge simeon
	git checkout chen
	git merge main
	git checkout simeon