from CodeBattlePythonLibrary import GameClient
import random

SERVER_ADDRESS = 'epruizhw0172.moscow.epam.com:8080'
PLAYER_NAME = 'katatonia@mail.org'
AUTH_CODE = '1085963739701489268'


def turn(gcb, level, questions):
    if not questions:
        gcb.start_next_level()
    else:
        answers = []
        for q in questions:
            answers.append(solve(level, q))

        gcb.send_answers(answers)


def solve(level, question):
    if level == 0:
        if question == 'hello':
            return 'world'
        elif question == 'world':
            return 'hello'
        return question

    return 'TODO: solve quiz'


if __name__ == '__main__':
    random.seed()
    gcb = GameClient(SERVER_ADDRESS, PLAYER_NAME, AUTH_CODE)
    gcb.run(turn)
