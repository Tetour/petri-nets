PY := python3

.PHONY: all nets notes index check simlib clean

all: nets notes simlib index

nets:
	$(PY) -m pn.build

notes:
	$(PY) -m pn.notes

index:
	$(PY) -m pn.index

simlib:
	$(PY) -m pn.simlib

check: simlib
	$(PY) -m pn.build --check-only

clean:
	rm -r build
