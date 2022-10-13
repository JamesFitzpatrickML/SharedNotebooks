import json
import xpress as xp


problem = xp.problem(name="Pig Diet Problem") # Create and name the Problem

# Set up the data for the problem

with open("pig_diet_problem_data.json") as data: # Open the file using a context manager
    data = json.load(data) # Load in all the data as a dictionary

feed_names = data["feed_names"] # Load in the feed names
nutrient_names = data["nutrient_names"] # Load in the nutrient names
feed_costs = data["feed_costs"] # Load in the feed costs
nutrient_requirements = data["nutrient_requirements"] # Load in the nutrient requirements
nutrient_quantities = data["nutrient_quantities"] # Load in the nutrient quantities

# Construct the problem

variables = [
    xp.var(name=feed_name, lb=0, vartype=xp.continuous) for feed_name in feed_names
] # Use the strings to create a list of named variables
variable_dict = {
    feed_name: variable for (feed_name, variable) in zip(feed_names, variables)
} # Create a dictionary of variables for easy access

feed_cost = sum([
    variable_dict[feed_name] * feed_costs[feed_name] for feed_name in feed_names
]) # Sum the costs of the feeds multiplied by the quanitites purchased

constraint_dict = {} # Make an empty dictionary to contain the constraints for the

for nutrient_name in nutrient_names: # For each of the nutrients
    nutrient_requirement = nutrient_requirements[nutrient_name] # Get the required nutrient amount
    nutrient_quantity = nutrient_quantities[nutrient_name] # Get the amount in each feed
    nutrient_sum = sum([
        variable_dict[feed_name] * nutrient_quantity[feed_name] for feed_name in feed_names
    ]) # Compute the sum of the feed quantities times the nutrients in the feed
    nutrient_constraint = nutrient_sum >= nutrient_requirement # Construct the nutrient constraint
    constraint_dict[nutrient_name] = nutrient_constraint # Add the nutrient constraint to the dictionary
    
problem.addVariable(variable_dict) # Add the variables to the problem
problem.addConstraint(constraint_dict) # Add the constraints to the problem
problem.setObjective(feed_cost, sense=xp.minimize) # Add the objective function to the problem

problem.solve() # Solve the problem

solution_values = problem.getSolution() # Get the solution values

print("\n\n\n") # Print some blank lines
print("Objective function value: ", problem.getObjVal()) # Print the optimal objective function value
for variable_name, solution_value in zip(variable_dict.keys(), solution_values):
    print(variable_name + " quantity: ", solution_value) # Print the value of the variable
