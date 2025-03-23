# Brophy's Game Of Life

<img alt="GitHub forks" src="https://img.shields.io/github/forks/Chris-B33/Brophys-Game-Of-Life"> <img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/Chris-B33/Brophys-Game-Of-Life">

## Description
This project was an introduction to my own private study of Machine Learning outside of education.
Conway's Game of Life (CGOL) is an interesting piece of cellular automota and I wanted to put my own spin on it.
<br>
Conway's original version had a set ruleset:
- An alive cell with less than 2 neighbours dies to "underpopulation".
- An alive cell with more than 3 neighbours dies to "overpopulation".
- A dead cell with exactly 3 neighbours becomes alive.
<br>

My version generates as many random rule states as defined in "config.ini" and then trains a model to run on that dataset. Hence, the ruleset changes every time.

## Example
This is how a 'glider', a classic pattern in CGOL, behaves under two different sets of automatically generated rules in my version: <br>

| Example 1 | Example 2 |
|-----------|-----------|
| <img src="./assets/example1.gif" width="150" height="150"/> | <img src="./assets/example2.gif" width="150" height="150"/> |

## Installation
- Run the command "pip install -r requirements.txt".
- Then run main.py.

## Controls
- "r" => Resets the grid to empty.
- "o" => Advances the grid by one state
- "space" => Sets the grid to 'running'. It will continue to update automatically. 
