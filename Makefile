PY := python3

.PHONY: all nets notes check clean

all: nets notes

nets:
	$(PY) -m pn.build

notes:
	$(PY) -m pn.notes

check:
	$(PY) -m pn.build --check-only

clean:
	rm -r build
