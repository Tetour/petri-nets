PY := python3

.PHONY: all nets notes check simlib clean

all: nets notes simlib

nets:
	$(PY) -m pn.build

notes:
	$(PY) -m pn.notes

simlib:
	$(PY) -m pn.simlib

check: simlib
	$(PY) -m pn.build --check-only

clean:
	rm -r build
