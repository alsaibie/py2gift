# AUTOGENERATED! DO NOT EDIT! File to edit: 03_question.ipynb (unless otherwise specified).

__all__ = ['QuestionGenerator', 'NumericalQuestionGenerator', 'MultipleChoiceQuestionGenerator',
           'MultipleChoiceTheoreticalQuestionGenerator']

# Cell

import abc
import string
from typing import List, Union, Optional, Tuple

import numpy as np

# Cell

class QuestionGenerator(metaclass=abc.ABCMeta):

    def __init__(
            self, unprocessed_statement: string.Template, unprocessed_feedback: string.Template, time: Optional[int] = None,
            prng: np.random.RandomState = np.random.RandomState(42)) -> None:

        self.prng = prng
        self.unprocessed_statement = unprocessed_statement
        self.unprocessed_feedback = unprocessed_feedback
        self.time = time

        self.statement = None

        # try...
        try:

            # ...to get the final string with no substitutions
            self.feedback = self.unprocessed_feedback.substitute()

        # some substitutions are needed to get the final string
        except KeyError:

            self.feedback = None

    @property
    @abc.abstractmethod
    def class_name(self) -> str:

        pass

    # this is the method to be defined by the user
    @abc.abstractmethod
    def setup(self, **kwargs):

        pass

    def partially_assemble_question(self, statement: str, feedback: str) -> dict:

        question = dict()

        question['class'] = self.class_name
        question['statement'] = statement
        question['feedback'] = feedback

        if self.time:

            question['time'] = str(self.time)

        return question

    def __call__(self, **kwargs):

        # arguments are passed directly to `setup`
        self.setup(**kwargs)

        assert self.statement is not None
        assert isinstance(self.statement, str), f'statement {self.statement} is not a string'

        assert self.feedback is not None
        assert isinstance(self.feedback, str), f'feedback {self.feedback} is not a string'

# Cell

class NumericalQuestionGenerator(QuestionGenerator):

    def __init__(
            self, unprocessed_statement: string.Template, unprocessed_feedback: string.Template,  time: Optional[int] = None,
            prng: np.random.RandomState = np.random.RandomState(42)) -> None:

        super().__init__(unprocessed_statement, unprocessed_feedback, time, prng)

        self.solution = None
        self.error = None

    @property
    def class_name(self) -> str:

        return 'Numerical'

    def assemble_question(self, statement: str, feedback: str, solution: float, error: Optional[float] = None) -> dict:

        question = self.partially_assemble_question(statement, feedback)

        question['solution'] = dict()
        question['solution']['value'] = solution

        if error is None:

            error = solution * 0.1

        question['solution']['error'] = error

        return question

    def __call__(self, **kwargs):

        super().__call__(**kwargs)

        assert self.solution is not None
        assert self.error is not None

        return self.assemble_question(
            statement=self.statement, feedback=self.feedback, solution=self.solution, error=self.error)

# Cell

class MultipleChoiceQuestionGenerator(QuestionGenerator):

    def __init__(
            self, unprocessed_statement: Union[str, string.Template], unprocessed_feedback: Union[str, string.Template], time: Optional[int] = None,
            prng: np.random.RandomState = np.random.RandomState(42)) -> None:

        super().__init__(unprocessed_statement, unprocessed_feedback, time, prng)

        self.right_answer = None
        self.wrong_answers = None

    @property
    def class_name(self) -> str:

        return 'MultipleChoice'

    def assemble_question(
            self, statement: str, feedback: str, perfect_answer: str,
            wrong_answers: Union[List[str], List[Tuple[str, float]]]) -> dict:

        question = self.partially_assemble_question(statement, feedback)

        question['answers'] = dict()
        question['answers']['perfect'] = perfect_answer
        question['answers']['wrong'] = wrong_answers

        return question

    def __call__(self, **kwargs):

        super().__call__(**kwargs)

        assert self.right_answer is not None
        assert isinstance(self.right_answer, str), f'right answer {self.right_answer} is not a string'

        assert self.wrong_answers is not None
        assert all([isinstance(e, str) for e in self.wrong_answers]),\
            f'one or several elements in {self.wrong_answers} is not a string'

        return self.assemble_question(
            statement=self.statement, feedback=self.feedback, perfect_answer=self.right_answer,
            wrong_answers=self.wrong_answers)

# Cell

class MultipleChoiceTheoreticalQuestionGenerator(MultipleChoiceQuestionGenerator):

    def setup(self, right_answer: str, wrong_answers: List[str]):

        self.statement = self.unprocessed_statement.safe_substitute()
        self.feedback = self.unprocessed_feedback.safe_substitute()

        self.right_answer = right_answer
        self.wrong_answers = wrong_answers