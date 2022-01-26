from setuptools import setup, find_packages


setup(
    name="wordle_strategy_evaluation",
    packages=find_packages(),
    version="0.0.1",
    entry_points={
        "console_scripts": [
            "wordle_strategy_evaluation = wordle_strategy_evaluation.__main__:main"
        ]
    },
    url="https://github.com/Seth-Rothschild/wordle_strategy_evaluation.git",
    author="Seth Rothschild",
    author_email="seth.j.rothschild@gmail.com",
    description="A package to enable evaluating wordle strategies",
    install_requires=[],
    tests_require=["pytest"],
    test_suite="pytest",
)
