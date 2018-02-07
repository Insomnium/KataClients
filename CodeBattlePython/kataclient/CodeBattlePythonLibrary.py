import websocket
import json
import logging

logger = logging.getLogger(__name__)


class GameClient:
    def __init__(self, server, user, code, description):
        path = "ws://{}/codenjoy-contest/ws?user={}&code={}".format(
            server, user, code)
        logger.info("connecting... {}".format(path))
        self.description = description
        self.socket = websocket.WebSocketApp(path,
                                             on_message=self.on_message,
                                             on_error=self.on_error,
                                             on_close=self.on_close,
                                             on_open=self.on_open)

    # message('['world', 'hello']')
    # message('StartNextLevel')
    def __send(self, answer):
        msg = "message('{}')".format(answer)
        logger.info('Sending: {}'.format(msg))
        self.socket.send(msg)

    def run(self, on_turn):
        self.on_turn = on_turn
        self.socket.run_forever()

    def on_open(self, conn):
        logger.info('Connection established: {}'.format(conn))

    def on_message(self, ws, message):
        message = message[6:]
        data = json.loads(message)
        if self.description:
            print(data['description'].encode('latin1').decode('unicode_escape'))
            self.socket.close()
        else:
            self.on_turn(self, data['level'], data['questions'])

    def on_error(self, ws, error):
        logger.error(error)

    def on_close(self, ws):
        logger.info("### disconnected ###")

    def start_next_level(self):
        self.__send('StartNextLevel')

    def skip_this_level(self):
        self.__send('SkipThisLevel')

    def send_answers(self, answers=[]):
        self.__send(json.dumps(answers))
