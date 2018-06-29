# Nathan Lakritz
# Fall 2016
# natejl123@gmail.com

import random
import diseasegraphics

def generate_grid(size):
    '''Generates a square grid dictionary with length and width (size).'''
    grid_init = {}
    for x in range(size):
        for y in range(size):
            coordinate = (x, y)
            grid_init[coordinate] = "."  # The string "." represents an empty cell.
    return grid_init


def population_density(grid_pop, pop_density):
    '''Creates the initial population of cells based on (density) parameter [0-1] and a random value.'''
    for x in grid_pop:
        if random.random() < pop_density:  # Higher density increases birth rate.
            grid_pop[x] = 0  # The integer 0 represents a healthy cell.
    return grid_pop


def disease_chance(grid_disease, disease_density):
    '''Turns healthy cells into infected cells based on (disease_rate) parameter [0-1] and a random value.'''
    for x in grid_disease:
        if grid_disease[x] == 0:  # Only turns healthy cells into infected cells.
            if random.random() < disease_density:
                grid_disease[x] = 1  # The integer 1 represents a newly infected cell.
    return grid_disease


def birth_chance(birth_update, size, rate):
    '''Generates new healthy cells next to previously healthy cells based on (birth_rate) parameter and a random value.
    Takes (size) to locate coordinates, their surrounding cells, and their values.'''
    x = size - 1  # Zero indexing.
    y = size - 1
    temp = {}  # New dictionary prevents grid from updating too early.
    for j in birth_update:
        if birth_update[j] == 0:
            temp[j] = 0  # Updates new grid with healthy cells from previous grid.
    for j in temp:  # Goes through new set of cells rather than old set, to keep the correct order.
        if birth_update[j] == 0:
            if 0 <= j[0] <= x and 0 <= j[1] <= y:
                try:  # Errors are guaranteed within this loop.
                    if birth_update[(j[0] + 1, j[1] + 1)] == ".":  # Checking to see if surrounding cells fit the given conditions for a new birth.
                        if random.random() < rate:
                            birth_update[(j[0] + 1, j[1] + 1)] = 0  # Turns empty cell into healthy cell if random value is less than provided value.
                except KeyError:  # An error will occur if the coordinate being searched for does not exist. This happens when looking at cells on the border of the grid, as some adjacent cells will not exist.
                    pass  # In the case of a KeyError, the iteration should simply skip over.
                try:
                    if birth_update[(j[0] + 1, j[1])] == ".":
                        if random.random() < rate:
                            birth_update[(j[0] + 1, j[1])] = 0
                except KeyError:
                    pass
                try:
                    if birth_update[(j[0] + 1, j[1] - 1)] == ".":
                        if random.random() < rate:
                            birth_update[(j[0] + 1, j[1] - 1)] = 0
                except KeyError:
                    pass
                try:
                    if birth_update[(j[0], j[1] + 1)] == ".":
                        if random.random() < rate:
                            birth_update[(j[0], j[1] + 1)] = 0
                except KeyError:
                    pass
                try:
                    if birth_update[(j[0], j[1] - 1)] == ".":
                        if random.random() < rate:
                            birth_update[(j[0] + 1, j[1] - 1)] = 0
                except KeyError:
                    pass
                try:
                    if birth_update[(j[0] - 1, j[1] - 1)] == ".":
                        if random.random() < rate:
                            birth_update[(j[0] - 1, j[1] - 1)] = 0
                except KeyError:
                    pass
                try:
                    if birth_update[(j[0] - 1, j[1])] == ".":
                        if random.random() < rate:
                            birth_update[(j[0] - 1, j[1])] = 0
                except KeyError:
                    pass
                try:
                    if birth_update[(j[0] - 1, j[1] + 1)] == ".":
                        if random.random() < rate:
                            birth_update[(j[0] - 1, j[1] + 1)] = 0
                except KeyError:
                    pass
    return birth_update


def spread_chance(spread_update, size, rate):
    '''Similar to the birth_chance function, healthy cells can become infected. The spread parameter reflects the likelihood of
     disease spread.'''
    x = size - 1
    y = size - 1
    temp = {}
    for j in spread_update:
        try:
            if spread_update[j] >= 1:
                temp[j] = spread_update[j]
        except TypeError:
            pass
    for j in temp:
        if spread_update[j] >= 1:
            if 0 <= j[0] <= x and 0 <= j[1] <= y:
                try:
                    if spread_update[(j[0] + 1, j[1] + 1)] == 0:  # Healthy input.
                        if random.random() < rate:
                            spread_update[(j[0] + 1, j[1] + 1)] = 100  # Infected result.
                except KeyError:
                    pass
            try:
                if spread_update[(j[0] + 1, j[1])] == 0:
                    if random.random() < rate:
                        spread_update[(j[0] + 1, j[1])] = 100
            except KeyError:
                pass
            try:
                if spread_update[(j[0] + 1, j[1] - 1)] == 0:
                    if random.random() < rate:
                        spread_update[(j[0] + 1, j[1] - 1)] = 100
            except KeyError:
                pass
            try:
                if spread_update[(j[0], j[1] + 1)] == 0:
                    if random.random() < rate:
                        spread_update[(j[0], j[1] + 1)] = 100
            except KeyError:
                pass
            try:
                if spread_update[(j[0], j[1] - 1)] == 0:
                    if random.random() < rate:
                        spread_update[(j[0] + 1, j[1] - 1)] = 100
            except KeyError:
                pass
            try:
                if spread_update[(j[0] - 1, j[1] - 1)] == 0:
                    if random.random() < rate:
                        spread_update[(j[0] - 1, j[1] - 1)] = 100
            except KeyError:
                pass
            try:
                if spread_update[(j[0] - 1, j[1])] == 0:
                    if random.random() < rate:
                        spread_update[(j[0] - 1, j[1])] = 100
            except KeyError:
                pass
            try:
                if spread_update[(j[0] - 1, j[1] + 1)] == 0:
                    if random.random() < rate:
                        spread_update[(j[0] - 1, j[1] + 1)] = 100
            except KeyError:
                pass
    return spread_update


def disease_duration(duration_update):
    '''Updates the current stage of infection for infected cells.'''
    for x in duration_update:
        try:
            if duration_update[x] >= 1:  # Checks to see if the cell is infected.
                duration_update[x] += 1  # Increases the status of the infected cell.
        except TypeError:  # TypeErrors occur for empty cells which carry string values.
            pass
    return duration_update


def mortality_rate(mortality_update, duration, mortality):
    '''Checks to see if an infected cell that has reached the disease duration will die or become healthy again.
    Outcomes are based on morality.'''
    for x in mortality_update:
        try:
            if mortality_update[x] == duration:
                if random.random() < mortality:  # Both birth and death are based on a random value.
                    mortality_update[x] = ".*"  # Placeholder value so newly birthed cells cannot be immediately affected by other functions.
                else:
                    mortality_update[x] = -1  # Another placeholder value.
        except TypeError:  # TypeErrors occur for string values.
            pass
    return mortality_update


def transformer(grid_transform):
    '''Transforms placeholder values to their appropriate values.'''
    for x in grid_transform:
        if grid_transform[x] == ".*":  # Empty!
            grid_transform[x] = "."
        elif grid_transform[x] == -1:  # Healthy!
            grid_transform[x] = 0
        elif grid_transform[x] == 100:  # Infected!
            grid_transform[x] = 1
    return grid_transform


def print_grid(grid, grid_size):
    '''Prints a visual grid output, using the grid itself and size values to display the results neatly.'''
    for i in range(grid_size):
        for j in range(grid_size):
            print(grid[i, j], end='\t')  # Prints the key values, or coordinate values in a styled format.
        print("\n")


def sim(grid_size, density, disease, birth, spread, duration, mortality, days, graphic):
    '''Runs the total disease simulation based on several parameters.
    This function calls every other function multiple times and implements a loop for each day's grid following the initial grid.'''
    day_counter = 1  # Tracks current day.
    grid = generate_grid(grid_size)  # Starts off with an empty grid.
    populated_grid = population_density(grid, density)  # Populates grid with healthy cells.
    diseased_grid = disease_chance(populated_grid, disease)  # Infects some healthy cells.

    if graphic == True:
        z = diseasegraphics.DiseaseGrid(grid_size, sq=0)  # Generates the correct grid size.
        z.set_speed(0)  # Sets the default speed.
        for j in diseased_grid:
            try:
                x = j[0]
                y = j[1]
                value = (diseased_grid[j])  # Sets the value to the value of the cell.
                if value >= 1:
                    value = ((diseased_grid[j]) * 100) / (duration)  # Calculates the state of infection.
                z.update_cell(x, y, value)  # Updates cells with their correct state.
            except TypeError:  # Ignores empty cells.
                pass
        z.display_grid(day_counter)  # Keeps track of days.

    print("Grid at start of simulation")
    print_grid(diseased_grid, grid_size)
    print("\n")

    if duration != 1:  # Running the most common form of simulation, where the disease duration is greater than 1.
        duration_grid = disease_duration(diseased_grid)  # Increasing the current duration-state for initially infected cells.
        spread_grid = spread_chance(duration_grid, grid_size, spread)  # Spreading the infection.
        transformed_grid = transformer(spread_grid)  # Switching out the placeholders.
        birth_grid = birth_chance(transformed_grid, grid_size, birth)  # Birthing new healthy cells.

        if graphic == True:
            for j in birth_grid:
                try:
                    x = j[0]
                    y = j[1]
                    value = (birth_grid[j])
                    if value >= 1:
                        value = ((birth_grid[j]) * 100) / (duration)
                    z.update_cell(x, y, value)
                except TypeError:
                    pass
                except KeyError:
                    pass
            z.display_grid(day_counter)

        print("Grid after Day 1.")
        print_grid(birth_grid, grid_size)  # Printing the grid after the first day.
        print("\n")
        mortality_grid = mortality_rate(birth_grid, duration,mortality)  # Killing off infected cells which have reached the max duration for the following day.
        while day_counter < days:  # Looping for the remaining day cycles.
            day_counter += 1  # Advancing current day
            duration_grid = disease_duration(mortality_grid)
            spread_grid = spread_chance(duration_grid, grid_size, spread)
            birth_grid = birth_chance(spread_grid, grid_size, birth)
            transformed_grid = transformer(birth_grid)

            if graphic == True:
                for j in transformed_grid:
                    try:
                        x = j[0]
                        y = j[1]
                        value = (transformed_grid[j])
                        if value == ".":
	                        value = -1
                        if value >= 1:
                            value = ((transformed_grid[j]) * 100) / (duration)
                        z.update_cell(x, y, value)
                    except TypeError:
                        pass
                    except KeyError:
                        pass
                z.display_grid(day_counter)

            print("Grid after day " + str(day_counter))
            print_grid(transformed_grid, grid_size)
            print("\n")
            mortality_grid = mortality_rate(transformed_grid, duration, mortality)

    else:  # Special case where disease duration is equal to 1. Infected cells still need to die or become healthy, but not immediately after being spread.
        spread_grid = spread_chance(diseased_grid, grid_size, spread)  # Infection spreads.
        birth_grid = birth_chance(spread_grid, grid_size, birth)  # Healthy cells spread.
        mortality_grid = mortality_rate(birth_grid, duration, mortality)  # Old infected cells die.
        transformed_grid = transformer(mortality_grid)  # Placeholder values for newly infected cells prevent them from dying or healing right after being infected.
        print("Grid after Day 1.")
        print_grid(transformed_grid, grid_size)  # Prints grid for user.
        print("\n")
        while day_counter < days:
            day_counter += 1
            spread_grid = spread_chance(transformed_grid, grid_size, spread)
            birth_grid = birth_chance(spread_grid, grid_size, birth)
            mortality_grid = mortality_rate(birth_grid, duration, mortality)
            transformed_grid = transformer(mortality_grid)
            print("Grid after day " + str(day_counter))
            print_grid(transformed_grid, grid_size)
            print("\n")

sim(25, 0.5, 0.5, 0.5, 0.5, 10, 0.5, 100, True)  # Hard-code parameters. True activates graphics.
