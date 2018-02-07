from kataclient.CodeBattlePythonLibrary import GameClient
import kataclient.CodeBattlePythonSolvers as solvers
import random
import logging
import click

logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


SERVER_ADDRESS = 'localhost:8080'
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
    """
    TODO: solve the quizz here
    Solvers are placed in file CodeBattlePythonSolvers.
    Each level in separate function.
    Function name must be in format "level_<level_number>"
    :param level: level number
    :param question: exact value for current step
    :return: answer for exact value
    """
    solver = getattr(solvers, 'level_{}'.format(level), None)
    if solver:
        return solver(question)
    else:
        logger.error("Solver for level {} not found".format(level))
        return 'TODO: solve quiz'


@click.command()
@click.option('--address', default=SERVER_ADDRESS, help='Server address.')
@click.option('--name', default=PLAYER_NAME, help='Player name.')
@click.option('--auth', default=AUTH_CODE, help='Auth code.')
@click.option('--description/--no-description', default=False,
              help='View only task description and close')
def main(address, name, auth, description):
    random.seed()
    gcb = GameClient(address, name, auth, description)
    gcb.run(turn)


if __name__ == '__main__':
    main()
