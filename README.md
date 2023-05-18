## <ins>Question 1</ins>: <br> Minimax
#### Run the code:
```bash
python autograder.py -q q1
```
#### Run the code faster:
```bash
python autograder.py -q q1 --no-graphics
```
#### Lose as fast as possible:
```bash
python pacman.py -p MinimaxAgent -l trappedClassic -a depth=3
```
## <ins>Question 2</ins>: <br> Alpha-Beta pruning
#### Run the code:
```bash
python autograder.py -q q2
```
#### Run the code faster:
```bash
python autograder.py -q q2 --no-graphics
```
## <ins>Question 3</ins>: <br>  Expectimax
#### Run the code:
```bash
python autograder.py -q q3
```
#### Run the code faster:
```bash
python autograder.py -q q3 --no-graphics
```
#### Random Ghost Movement:
```bash
python pacman.py -p ExpectimaxAgent -l minimaxClassic -a depth=3
```
#### Alpha - Beta:
```bash
python pacman.py -p AlphaBetaAgent -l trappedClassic -a depth=3 -q -n 10
```
#### Expectimax:
```bash
python pacman.py -p ExpectimaxAgent -l trappedClassic -a depth=3 -q -n 10
```