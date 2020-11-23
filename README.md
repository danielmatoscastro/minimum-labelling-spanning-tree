# Minimum Labelled Spanning Tree
An experiment with genetic algorithms.

## Dependencies
- Click: lib for building CLI's with as little code as possible.
```
pip install click
```
- igraph: lib to plot graphs. Installation is required only if you'll use the *plot* command (see section below).
```
pip install python-igraph
```
- pycairo and cairocffi: they're dependencies of igraph.
cairocffi is a fallback of pycairo, so you can install only one of these libs.
```
pip install cairocffi
```
```
pip install pycairo
```

## Usage

To run a single execution and save result in .json file, use the command below:

```
python3 genetic-algorithm/main.py run --file="data/testFile_9_75_60.col" --seed=2 --population-size=400 --mutation-rate=0.2 --elitism-rate=0.3 --output-file="experiments/9_75_60_1.json"
```

To generate an image of a single execution result:
```
python3 genetic-algorithm/main.py plot --file="experiments/100-990-25-3-1-1.json"
```

To run 10 executions and export a full report:
```
python3 genetic-algorithm/main.py run-multiple --file="data/testFile_9_75_60.col" --population-size=400 --mutation-rate=0.2 --elitism-rate=0.3 --bks=7 --output-file="experiments/9_75_60.json"
```