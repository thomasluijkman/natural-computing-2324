# To train either the betting strategy or blackjack strategy run either

```bash
python ga.py
```
# or
```bash
python ga_betting.py
```
# respecively

# For ga.py you can either one of two function in the main:
```python
test_different_mu() #testing a range of mu (change mu range in function)
run_single_algorithm() #evolving a single run
```
# The hyperparameters can be are defined as global variables at the top of the file.

# for ga_betting.py you can run use the following functions:
```python
run_single_algorithm() #evolving a single run
test_different_agents() #trains and plot different agents
test_different_deck_count() #test different deck sizes (change deck sizes in function)
```

# The hyperparameters can be are defined as global variables at the top of the file.

