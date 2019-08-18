import pytest
from sauron.engine import Engine
from pprint import pprint

engine = Engine()


@engine.job("First Condition")
def first_condition(session, lower_number=0, greater_number=10):
    result = lower_number < greater_number
    print("#" * 40)
    print("Function called: first_condition")
    print("Function ARGS: ")
    print(f" - lower_number: {lower_number}")
    print(f" - greater_number: {greater_number}")
    print(f"Result EXPECTED: {result}")
    print("#" * 40)
    return result


@engine.job("Second Condition")
def second_condition(session, lower_number=0, greater_number=10):
    result = lower_number
    print("#" * 40)
    print("Function called: second_condition")
    print("Function ARGS: ")
    print(f" - lower_number: {lower_number}")
    print(f" - greater_number: {greater_number}")
    print(f"Result EXPECTED: {result}")
    print("#" * 40)
    return result


@engine.job("The Action")
def print_the_equation(session, lower_number=10, greater_number=20):
    result = None
    print("#" * 40)
    print("Function called: print_the_equation")
    print("Function ARGS: ")
    print(f" - lower_number: {lower_number}")
    print(f" - greater_number: {greater_number}")
    print(f"Result EXPECTED: {result}")
    print("#" * 40)


class TestFirstEngineCases:

    test_string = """
    [
        {
            "name": "first_condition",
            "args": {"lower_number": 3, "greater_number": 10},
            "job_type": "condition"
        },
        {
            "name": "print_the_equation",
            "args": {"lower_number": 3, "greater_number": 10},
            "job_type": "action"
        }
    ]
    """

    def setup(self):
        session = {"foo": "bar"}
        engine = Engine()
        engine.run(self.test_string, session)
        return engine

    def test_parsed_rules(self):
        engine = self.setup()
        result = engine.parsed_rule
        assert result[1].name == "print_the_equation"
        assert result[1].args == {"lower_number": 3, "greater_number": 10}
        assert result[1].job_type == "action"

    def test_session_content_at_the_end_includes_inital_data(self):
        engine = self.setup()
        assert engine.session.get("foo") == "bar"

    def test_session_includes_all_operations_results_at_the_end(self):
        engine = self.setup()
        assert engine.session.get("results").pop() == {
            "job": "print_the_equation",
            "return": None,
        }
        assert engine.session.get("results").pop() == {
            "job": "first_condition",
            "return": True,
        }
