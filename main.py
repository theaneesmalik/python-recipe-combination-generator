import re


class Ingredient:
    def __init__(self, name:str, amounts):
        self.name = name
        self.amounts = amounts
        self.minLength = max(max(len(amount) for amount in amounts), len(name))

    # def get_header(self ,align, filler, separator):
    #     return f"{self.name.center(self.length, filler)}{separator}"
    def get_header(self, left_padding, right_padding, padding_filler, separator='|'):
        return f"{padding_filler * left_padding}{self.name.center(self.minLength, padding_filler)}{padding_filler * right_padding}{separator}"


    def get_divider(self, filler, left_padding, right_padding, separator):
        return f"{filler * (self.minLength + left_padding + right_padding)}{separator}"

    def get_special_divider(self, filler):
        filler_length = len(filler)
        repeated_fillers = filler * (self.length // filler_length)
        remaining_length = self.length % filler_length
        result = repeated_fillers + filler[:remaining_length]
        return result

    def get_length(self, length):
        if(length < self.minLength): return self.minLength
        else: return length

class Recipe:
    def __init__(self, name):
        self.name = name
        self.ingredients = []
        self.combinations = []

    def add_ingredient(self, name, amounts):
        ingredient = Ingredient(name, amounts)
        self.ingredients.append(ingredient)

    def generate_combinations(self):
        combinations = [[]]

        for ingredient in self.ingredients:
            ingredient_combinations = []

            for combination in combinations:
                for amount in ingredient.amounts:
                    new_combination = combination + [(ingredient.name, amount)]
                    # new_combination.append((ingredient.name, amount))
                    ingredient_combinations.append(new_combination)

            combinations = ingredient_combinations

        self.combinations = combinations




def extract_recipe_data(input_file):
    with open(input_file, "r") as file:
        lines = file.readlines()

    recipes = []
    current_recipe = None
    ingredient_pattern = r"([a-zA-Z]+)\s+=\s+(.+)"

    for line in lines:
        line = line.strip()

        if line:
            if line.endswith(":"):
                recipe_name = line[:-1]
                current_recipe = Recipe(recipe_name)
                recipes.append(current_recipe)
            else:
                match = re.match(ingredient_pattern, line)
                if match:
                    ingredient_name = match.group(1)
                    amounts = [amount.strip() for amount in match.group(2).split(",")]
                    current_recipe.add_ingredient(ingredient_name, amounts)

    return recipes


def write_recipe_combinations(recipe,first_column_name='Combos', divider_filler="-" ,separator='|',left_padding=0,right_padding=0,padding_filler=' '):
    output_file = f"{recipe.name}_recipe_combos.txt"

    with open(output_file, "w") as file:
        header = f"{separator}{padding_filler * left_padding}{first_column_name}{padding_filler * right_padding}{separator}"
        divider1 = f"{separator}{''.center(len(header) - 2,divider_filler)}{separator}"

        for ingredient in recipe.ingredients:
            ingredient_name = ingredient.name
            header += ingredient.get_header(left_padding, right_padding, padding_filler, separator)
            divider1 += ingredient.get_divider(divider_filler,left_padding, right_padding, separator)

        # file.write(f"{divider3}\n")
        file.write(f"{header}\n")
        file.write(f"{divider1}\n")

        for index, combination in enumerate(recipe.combinations, 1):
            row = f"{separator}{padding_filler * left_padding}{str(index).center(len(first_column_name),padding_filler)}{padding_filler * right_padding}{separator}"
            for ingredient_name, amount in combination:
                current_ingredient = next(
                    (
                        ingredient
                        for ingredient in recipe.ingredients
                        if ingredient.name == ingredient_name
                    ),
                    None,
                )
                if current_ingredient:
                    max_length = current_ingredient.minLength
                    row += f"{padding_filler * left_padding}{amount.center(max_length,padding_filler)}{padding_filler * right_padding}{separator}"
            file.write(f"{row}\n")

    print(f"Generated recipe combinations for {recipe.name} in {output_file}")



def main():
    input_file = "recipes_input_data.txt"
    recipes = extract_recipe_data(input_file)
    # Change below variables for custome variations
    first_column_name='Combos'
    divider_filler="-" 
    separator='|'
    left_padding=1
    right_padding=1
    padding_filler=' '
    # Change above variables
    for recipe in recipes:
        recipe.generate_combinations()
        write_recipe_combinations(recipe,first_column_name, divider_filler, separator, left_padding, right_padding, padding_filler)


if __name__ == "__main__":
    main()
