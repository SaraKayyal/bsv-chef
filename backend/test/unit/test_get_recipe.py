import pytest
from unittest.mock import patch, MagicMock
from src.controllers.recipecontroller import RecipeController
from src.static.diets import Diet
from src.util.dao import DAO

@pytest.fixture
def recipe_controller():
    # Use mocking to ensure no other dependency can effect the testing.
    with patch('src.util.dao.DAO.__init__', return_value=None):
        dao = DAO('items')
        controller = RecipeController(dao)
        return controller

## Test ID 1 *
@pytest.mark.unit
@patch.object(RecipeController, 'get_readiness_of_recipes')
def test_get_recipe_optimal_selection(mock_get_readiness_of_recipes, recipe_controller):
    # Mock a dict with the readiness values.
    mock_get_readiness_of_recipes.return_value = {
        'Vegan Salad': 0.85,
        'Vegan Soup': 0.95,
        'Vegan Cake': 0.75
    }

    # The take_best is set to true, expect the highest readiness to be returned.
    diet = Diet.VEGAN
    expected_recipe = 'Vegan Soup'
    result = recipe_controller.get_recipe(diet, take_best=True)

    assert result == expected_recipe

## Test ID 2
@pytest.mark.unit
@patch.object(RecipeController, 'get_readiness_of_recipes')
@patch('random.randint', return_value=0) 
def test_get_recipe_random_selection(mock_randint, mock_get_readiness_of_recipes, recipe_controller):
    mock_get_readiness_of_recipes.return_value = {
        'Vegan Burger': 0.8,
        'Vegan Smoothie': 0.9,
        'Vegan Taco': 0.7
    }

    # 'take_best' is False, we should expect a random recipe, but we used mock since it is difficult to test randomly.
    diet = Diet.VEGAN
    expected_recipe = 'Vegan Burger'
    result = recipe_controller.get_recipe(diet, take_best=False)

    assert result == expected_recipe

## Test ID 3 *
@pytest.mark.unit
@patch.object(RecipeController, 'get_readiness_of_recipes')
def test_get_recipe_below_threshold_none_returned(mock_get_readiness_of_recipes, recipe_controller):
    mock_get_readiness_of_recipes.return_value = {
        # Here is the Readniess below the readiness value of 0.1, we should expect None as a return.
        'Vegan Burger': 0.05,
        'Vegan Smoothie': 0.09,
        'Vegan Taco': 0.08
    }

    diet = Diet.VEGAN

    result_optimal = recipe_controller.get_recipe(diet, take_best=True)
    assert result_optimal is None

## Test ID 4
@pytest.mark.unit
@patch.object(RecipeController, 'get_readiness_of_recipes')
def test_get_recipe_returns_highest_readiness_recipe(mock_get_readiness_of_recipes, recipe_controller):
    mock_get_readiness_of_recipes.return_value = {
        'Low Readiness Meal': 0.3,
        'High Readiness Meal': 0.9,
        'Medium Readiness Meal': 0.5
    }

    diet = Diet.VEGAN
    result = recipe_controller.get_recipe(diet, take_best=True)

    # Assert the function returns the recipe with the highest readiness value
    assert result == 'High Readiness Meal'

## Test ID 5
@pytest.mark.unit
@patch.object(RecipeController, 'get_readiness_of_recipes')
def test_get_recipe_no_recipes_available(mock_get_readiness_of_recipes, recipe_controller):
    mock_get_readiness_of_recipes.return_value = {}

    # The Diet does not matter here.
    diet = Diet.VEGAN

    result_optimal = recipe_controller.get_recipe(diet, take_best=True)
    assert result_optimal is None

## Test ID 6
@pytest.mark.unit
@patch.object(RecipeController, 'get_readiness_of_recipes', return_value={})
def test_get_recipe_invalid_input(mock_get_readiness_of_recipes, recipe_controller):
    # We are using invalid data for the Diet.
    invalid_diet = 'invalid_diet'

    result_random = recipe_controller.get_recipe(invalid_diet, take_best=False)

    assert result_random is None