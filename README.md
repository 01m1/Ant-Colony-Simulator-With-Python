# Ant Colony Simulator 🐜
Explore the behaviour of ants in this interactive simulator. This project leverages Python, utilising Pygame and NumPy to simulate realistic ant behaviour.

# Getting Started

Upon launching the program, you'll encounter a user-friendly menu where you can adjust simulation settings and start the simulation.

![image](https://github.com/01m1/Ant-Colony-Simulator-With-Python/assets/69215780/aa911744-6f89-41f2-8b5b-d5e6f3284e5b)

**Simulation Features**

* **Ant Behavior:** Ants wander around randomly across the screen in search of food. Once they collect food, they transport it back to their home.

* **Pheromone Trails:** Ants lay down pheromone trails to guide others to food sources. Paths strengthen over time as more ants use them, with shorter paths initially stronger.

* **Pheromone Dynamics:** Pheromones evaporate gradually, adjusting path strengths dynamically based on recent activity. This results in ants discovering the shortest path to a food source.

* **Queen Ant Mechanics:** The queen ant, identified by its yellow head and blue circle, can fly over walls. It spawns a new ant every 50 food items collected, contributing to colony growth.

**Settings**

Navigate to the settings menu to customise the simulator. Import and export settings using the buttons at the top-right corner. Settings configurations are saved locally as text files for future use.

# Controls

![image](https://github.com/01m1/Ant-Colony-Simulator-With-Python/assets/69215780/3ee67223-45e4-4979-b63d-4f48f3f9a6eb)

Start the simulation by clicking the 'Start' button on the main menu. Observe ants as they navigate the simulated environment.

* **Left Click:** Place food items
* **Right Click:** Remove food items or create walls
* **Middle Click:** Build walls

# Installation

Python can be installed from the official python website.

You can clone the repository and setup a virtual environment and install all the necessary libraries automatically by running `install.sh` (for Linux).

OR

You can install NumPy and PyGame yourself through the following command in your terminal.

`pip install numpy pygame`

Clone the repository and execute main.py with python3 to begin.

`python3 main.py`

# Gallery

![Recording2024-07-06at23 14 42-ezgif com-crop](https://github.com/01m1/Ant-Colony-Simulator-With-Python/assets/69215780/a74a560c-bfbd-42c3-ab24-e622ef978e9a)

![Recording2024-07-06at23 21 32-ezgif com-cut](https://github.com/01m1/Ant-Colony-Simulator-With-Python/assets/69215780/8133ef33-66db-4757-ad2a-77d6341c738f)
