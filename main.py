import re


class Ingredient:
    def __init__(self, name: str, amounts):
        self.name = name
        self.amounts = amounts
        self.length = max(max(len(amount) for amount in amounts), len(name)) + 2

    def get_header(self):
        return f"{self.name.center(self.length,' ')}|"
        # return f"{' ' * (self._spacing + self._extra)}{self.name}{' ' * self._spacing}|"

    def get_divider(self, filler):
        return f"{''.center(self.length, filler)}|"

    def get_special_divider(self, filler):
        filler_length = len(filler)
        repeated_fillers = filler * (self.length // filler_length)
        remaining_length = self.length % filler_length
        result = repeated_fillers + filler[:remaining_length]
        return result


class Recipe:
    def __init__(self, name):
        self.name = name
        self.ingredients = []

    def add_ingredient(self, name, amounts):
        ingredient = Ingredient(name, amounts)
        self.ingredients.append(ingredient)

    @property
    def combinations(self):
        combinations = [[]]

        for ingredient in self.ingredients:
            ingredient_combinations = []
            for combination in combinations:
                for amount in ingredient.amounts:
                    new_combination = combination + [(ingredient.name, amount)]
                    ingredient_combinations.append(new_combination)
            combinations = ingredient_combinations
        return combinations


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


def write_recipe_combinations(recipe):
    output_file = f"{recipe.name}_recipe_combos.txt"

    with open(output_file, "w") as file:
        header = f"|{'Combos'.center(8, ' ')}|"
        divider1 = f"|{''.center(8,'-')}|"
        divider2 = f"|{''.center(8,'*')}|"
        divider3 = f"|{'*-' * 4}|"

        for ingredient in recipe.ingredients:
            ingredient_name = ingredient.name
            header += ingredient.get_header()
            divider1 += ingredient.get_divider("-")
            divider2 += ingredient.get_divider("8")
            divider3 += ingredient.get_special_divider("*-")

        # file.write(f"{divider3}\n")
        file.write(f"{header}\n")
        file.write(f"{divider1}\n")

        for index, combination in enumerate(recipe.combinations, 1):
            row = f"|{str(index).center(8)}|"
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
                    max_length = current_ingredient.length
                    row += f"{amount.center(max_length)}|"
            file.write(f"{row}\n")
            # file.write(f"{divider3}\n")

            # if index % 2 == 0:
            #     file.write(f"{divider1}\n")
            # else:
            #     file.write(f"{divider2}\n")

    print(f"Generated recipe combinations for {recipe.name} in {output_file}")


def main():
    input_file = "recipes_input_data.txt"
    recipes = extract_recipe_data(input_file)

    for recipe in recipes:
        write_recipe_combinations(recipe)


if __name__ == "__main__":
    main()
