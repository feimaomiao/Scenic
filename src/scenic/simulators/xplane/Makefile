SCENIC_FILE="../../../../examples/xplane/example.scenic"
CONFIG_FILE="../../../../examples/xplane/config.json"

.PHONY: simulator location example

all: simulator

simulate:
	ln -s -f $(CONFIG_FILE) .
	scenic $(SCENIC_FILE) --axes --show-records --simulate --count=1 -b
	git clean ../.. -f

simulate_verbose:
	ln -s -f $(CONFIG_FILE) .
	scenic $(SCENIC_FILE) --axes --simulate --count=1 --verbosity=3 -b
	git clean ../.. -f

simulate-finite:
	ln -s -f $(CONFIG_FILE) .
	scenic $(SCENIC_FILE) --axes --simulate --count=5 --time=10 --verbosity=3 -b
	git clean ../.. -f

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
	git pull
	git merge simeon
	git push
	git checkout simeon
	git pull

get-cheuk:
	git checkout xplane-simulator
	git pull
	git checkout simeon
	git merge xplane-simulator
	git push