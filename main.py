import re


class Ingredient:
    def __init__(self, name: str, amounts):
        self.name = name
        self.amounts = amounts
        self.minLength = max(max(len(amount) for amount in amounts), len(name))

    def get_divider(
        self, filler, left_padding, right_padding, separator, column_length
    ):
        return f"{filler * (max(self.minLength, column_length) + left_padding + right_padding)}{separator}"


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
                    ingredient_combinations.append(new_combination)
            combinations = ingredient_combinations
        self.combinations = combinations


class RecipeFile:
    def __init__(self, input_file: str):
        self.input_file = input_file
        self.first_column_name = "Combos"
        self.divider_filler = "-"
        self.separator = "|"
        self.left_padding = 0
        self.right_padding = 0
        self.padding_filler = " "
        self.column_length = 10
        self.text_align = "left"

    def get_aligned_text(self, str, length=None):
        if length is None:
            length = self.column_length
        if self.text_align == "left":
            return str.ljust(length, self.padding_filler)
        elif self.text_align == "right":
            return str.rjust(length, self.padding_filler)
        return str.center(length, self.padding_filler)

    def extract_recipe_data(self):
        with open(self.input_file, "r") as file:
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
                        amounts = [
                            amount.strip() for amount in match.group(2).split(",")
                        ]
                        current_recipe.add_ingredient(ingredient_name, amounts)
        return recipes

    def write_recipe_combinations(self, recipe):
        def get_first_column_length():
            length = len(recipe.combinations)
            digitCount = 0
            while length:
                digitCount += 1
                length //= 10
            return max(len(self.first_column_name), digitCount, self.column_length)

        separator_with_padding = f"{self.padding_filler * self.left_padding}{self.separator}{self.padding_filler * self.right_padding}"
        output_file = f"{recipe.name}_recipe_combos.txt"
        with open(output_file, "w") as file:
            header = f"{self.separator}{self.right_padding * self.padding_filler}{self.get_aligned_text(self.first_column_name)}{separator_with_padding}"
            divider1 = f"{self.separator}{''.center(len(header) - 2 - self.right_padding,self.divider_filler)}{self.separator}"
            for ingredient in recipe.ingredients:
                ingredient_name = ingredient.name
                header += f"{self.get_aligned_text(ingredient.name, max(ingredient.minLength, self.column_length))}{separator_with_padding}"
                divider1 += ingredient.get_divider(
                    self.divider_filler,
                    self.left_padding,
                    self.right_padding,
                    self.separator,
                    self.column_length,
                )
            file.write(f"{header}\n")
            file.write(f"{divider1}\n")
            for index, combination in enumerate(recipe.combinations, 1):
                row = f"{self.separator}{self.padding_filler * self.right_padding}{self.get_aligned_text(str(index))}{separator_with_padding}"
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
                        max_length = max(
                            current_ingredient.minLength, self.column_length
                        )
                        row += f"{self.get_aligned_text(amount,max_length)}{separator_with_padding}"
                file.write(f"{row}\n")
        print(f"Generated recipe combinations for {recipe.name} in {output_file}")


def main():
    input_file = "recipes_input_data.txt"
    file = RecipeFile(input_file)
    recipes = file.extract_recipe_data()
    # Change below variables for custome variations
    file.first_column_name = "N"
    file.divider_filler = "-"
    file.separator = "|"
    file.left_padding = 4  # padding left of separator
    file.right_padding = 1  # padding right of separator
    file.padding_filler = " "  # padding / free space filler, only 1 character
    file.column_length = 10  # actual width of column will be (right_padding + column_length + left_padding)
    file.text_align = (
        "left"  # right | left | mid , it will align the text with in column_length
    )
    # Change above variables
    for recipe in recipes:
        recipe.generate_combinations()
        file.write_recipe_combinations(recipe)


if __name__ == "__main__":
    main()
