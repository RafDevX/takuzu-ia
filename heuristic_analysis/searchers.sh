# Use with TESTS_DIR=<path> ./heuristic_analysis/searchers.sh > /tmp/searchers.out

for i in $(ls $TESTS_DIR/*.in); do
	echo $(basename $i)
	python takuzu.py < $i
done