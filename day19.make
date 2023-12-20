.PHONY: run_example run_main
# Suppress default .o rules in make
day19.input:;
day19.test:;

day19.input.out day19.test.out: day19_cg.py day19.input day19.test
	python3 day19_cg.py > /dev/null

day19.test.runme: day19.test.o
	ld -macos_version_min 14.0.0 -o day19.test.runme day19.test.o -lSystem -syslibroot `xcrun -sdk macosx --show-sdk-path` -e _start -arch arm64

day19.test.o: day19.test.out
	as -o day19.test.o day19.test.out

example: day19.test.runme
	@echo "--------------------"
	./day19.test.runme

day19.input.runme: day19.input.o
	ld -macos_version_min 14.0.0 -o day19.input.runme day19.input.o -lSystem -syslibroot `xcrun -sdk macosx --show-sdk-path` -e _start -arch arm64

day19.input.o: day19.input.out
	as -o day19.input.o day19.input.out

run_main: day19.input.runme
	@echo "--------------------"
	./day19.input.runme

all: day19.input.runme day19.test.runme 