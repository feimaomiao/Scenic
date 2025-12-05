SCENIC_FILE="../../../../examples/xplane/example.scenic"
CONFIG_FILE="../../../../examples/xplane/config.json"

.PHONY: simulator location example

all: simulator

simulate:
	ln -s $(CONFIG_FILE) .
	scenic $(SCENIC_FILE) --axes --simulate --count=5 --time=10 --verbosity=3 -b

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
	git checkout chen
	git pull
	git merge main
	git push
	git checkout xplane-simulator
	git pull
	git merge main
	git push
	git checkout simeon
	git pull

get-cheuk:
	git checkout xplane-simulator
	git pull
	git checkout simeon
	git merge xplane-simulator
	git push