import re


class Ingredient:
    def __init__(self, name: str, amounts):
        self.name = name
        self.amounts = amounts
        self.minLength = max(max(len(amount) for amount in amounts), len(name))

    # def get_header(self ,align, filler, separator):
    #     return f"{self.name.center(self.length, filler)}{separator}"
    def get_header(
        self,
        left_padding,
        right_padding,
        padding_filler,
        separator,
        column_length,
        text_align,
    ):
        def get_heder_text():
            if text_align == "left":
                return self.name.ljust(
                    max(self.minLength, column_length), padding_filler
                )
            elif text_align == "right":
                return self.name.rjust(
                    max(self.minLength, column_length), padding_filler
                )
            else:
                return self.name.center(
                    max(self.minLength, column_length), padding_filler
                )

        return f"{get_heder_text()}{padding_filler * right_padding}{separator}{padding_filler * left_padding}"

    def get_divider(
        self, filler, left_padding, right_padding, separator, column_length
    ):
        return f"{filler * (max(self.minLength, column_length) + left_padding + right_padding)}{separator}"

    def get_special_divider(self, filler):
        filler_length = len(filler)
        repeated_fillers = filler * (self.length // filler_length)
        remaining_length = self.length % filler_length
        result = repeated_fillers + filler[:remaining_length]
        return result

    def get_length(self, length):
        if length < self.minLength:
            return self.minLength
        else:
            return length


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


def write_recipe_combinations(
    recipe,
    first_column_name="Combos",
    divider_filler="-",
    separator="|",
    left_padding=0,
    right_padding=0,
    padding_filler=" ",
    column_length=10,
    text_align="min",
):
    def get_first_column_length():
        length = len(recipe.combinations)
        digitCount = 0
        while length:
            digitCount += 1
            length //= 10
        return max(len(first_column_name), digitCount, column_length)

    def get_first_column_aligned_text():
        if text_align == "left":
            return first_column_name.ljust(get_first_column_length(), padding_filler)
        elif text_align == "right":
            return first_column_name.rjust(get_first_column_length(), padding_filler)
        else:
            return first_column_name.center(get_first_column_length(), padding_filler)

        pass

    output_file = f"{recipe.name}_recipe_combos.txt"

    with open(output_file, "w") as file:
        # header = f"{separator}{first_column_name.center((left_padding+right_padding+get_first_column_length()), padding_filler)}{separator}"
        header = f"{separator}{left_padding * padding_filler}{get_first_column_aligned_text()}{left_padding * padding_filler}{separator}{right_padding * padding_filler}"
        divider1 = f"{separator}{''.center(len(header) - 2 -left_padding,divider_filler)}{separator}"

        for ingredient in recipe.ingredients:
            ingredient_name = ingredient.name
            header += ingredient.get_header(
                left_padding,
                right_padding,
                padding_filler,
                separator,
                column_length,
                text_align,
            )
            divider1 += ingredient.get_divider(
                divider_filler, left_padding, right_padding, separator, column_length
            )

        # file.write(f"{divider3}\n")
        file.write(f"{header}\n")
        file.write(f"{divider1}\n")

        def get_first_column_aligned_index():
            if text_align == "left":
                return str(index).ljust(get_first_column_length(), padding_filler)
            elif text_align == "right":
                return str(index).rjust(get_first_column_length(), padding_filler)
            else:
                return str(index).center(get_first_column_length(), padding_filler)

        def get_aligned_amount(amount, length):
            if text_align == "left":
                return amount.ljust(length, padding_filler)
            elif text_align == "right":
                return amount.rjust(length, padding_filler)
            else:
                return amount.center(length, padding_filler)

        for index, combination in enumerate(recipe.combinations, 1):
            row = f"{separator}{padding_filler * right_padding}{get_first_column_aligned_index()}{padding_filler * left_padding}{separator}{padding_filler * right_padding}"
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
                    max_length = max(current_ingredient.minLength, column_length)
                    row += f"{get_aligned_amount(amount,max_length)}{padding_filler * left_padding}{separator}{padding_filler * right_padding}"
            file.write(f"{row}\n")

    print(f"Generated recipe combinations for {recipe.name} in {output_file}")


def main():
    input_file = "recipes_input_data.txt"
    recipes = extract_recipe_data(input_file)
    # Change below variables for custome variations
    first_column_name = "N"
    divider_filler = "-"
    separator = "|"
    left_padding = 0  # padding left of separator
    right_padding = 1  # padding right of separator
    padding_filler = " "
    column_length = 15  # actual width of column will be (right_padding + column_length + left_padding)
    text_align = "right"  # right | left | mid , it will align the text with in column_length
    # Change above variables
    for recipe in recipes:
        recipe.generate_combinations()
        write_recipe_combinations(
            recipe,
            first_column_name,
            divider_filler,
            separator,
            left_padding,
            right_padding,
            padding_filler,
            column_length,
            text_align,
        )


if __name__ == "__main__":
    main()
