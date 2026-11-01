PY := python3

.PHONY: all nets notes index check notecheck simlib clean

all: nets notes simlib index

nets:
	$(PY) -m pn.build

notes:
	$(PY) -m pn.notes

index:
	$(PY) -m pn.index

simlib:
	$(PY) -m pn.simlib

check: notecheck simlib
	$(PY) -m pn.build --check-only

notecheck:
	$(PY) -m pn.notecheck

clean:
	rm -r build
