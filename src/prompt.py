from prompt_toolkit import prompt
from prompt_toolkit.completion import Completer, Completion


class CustomCompleter(Completer):
    selections: list[str]

    def __init__(self, selections: list[str]):
        self.selections = selections

    def get_completions(self, document, complete_event):
        word_before_cursor = document.get_word_before_cursor()
        word = []
        for selection in self.selections:
            if word_before_cursor in selection:
                word.append(Completion(selection, -len(word_before_cursor)))
        return word


class Prompt:
    message: str
    selections: list[str]

    def __init__(self, message: str, selections: list[str]):
        self.message = message
        self.selections = selections

    def __call__(self) -> str:
        return prompt(
            self.message,
            completer=CustomCompleter(self.selections),
        )
