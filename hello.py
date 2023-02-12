from ice.recipe import recipe

def say_nihao():
    return "Nihao!"

async def say_hello():
    return say_nihao() + " Hello world!"


recipe.main(say_hello)