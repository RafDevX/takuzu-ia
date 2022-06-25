#!/bin/sh

files=$(ls tests/ | grep "^input_")

for file in $files
do
  python takuzu.py < tests/$file > /tmp/takuzu.out
  output=$(cat /tmp/takuzu.out)
  output_file=$(echo $file | sed 's/input/output/')
  expected_output=$(cat tests/$output_file)
  if [ "$output" = "$expected_output" ]; then
    echo -e "\e[32mTest $file SUCCESS\e[0m"
  else
    echo -e "\e[31mTest $file FAILED\e[0m"
    colordiff -u /tmp/takuzu.out tests/$output_file
  fi
  rm /tmp/takuzu.out
done
