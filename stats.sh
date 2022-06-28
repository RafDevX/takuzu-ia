#!/bin/sh

tests_dir="./tests/input_*"
if [ "$1" = "custom-tests" ]; then
	tests_dir="../proj-ist-unit-tests/ia/2021-2022/custom-tests/*.in"
fi

echo "test,search,mean_time,gend_nodes,expd_nodes"

for i in $(ls $tests_dir); do
	for j in "bfs" "dfs" "greedy" "a_star"; do
		nodes_stats=$(python takuzu.py $j < $i | tail -n1)
		gen_nodes=$(echo $nodes_stats | cut -d' ' -f1)
		expd_nodes=$(echo $nodes_stats | cut -d' ' -f2)
		hyperfine "python takuzu.py $j < $i" --warmup 1 --time-unit millisecond --export-csv /tmp/takuzu-hf.csv &>/dev/null
		time=$(cat /tmp/takuzu-hf.csv | tail -n1 | cut -d',' -f2)
		echo "$(basename $i),$j,$time,$gen_nodes,$expd_nodes"
	done
done
