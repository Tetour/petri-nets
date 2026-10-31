PY := python3

.PHONY: all check clean

all:
	$(PY) -m pn.build

check:
	$(PY) -m pn.build --check-only

clean:
	rm -r build
