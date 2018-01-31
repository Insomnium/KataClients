import websocket
import json


class GameClient:
    def __init__(self, server, user, code):
        path = "ws://%s/codenjoy-contest/ws?user=%s&code=%s" % (server, user, code)
        print("connecting... %s" % path)
        self.socket = websocket.WebSocketApp(path, on_message=self.on_message, on_error=self.on_error,
                                             on_close=self.on_close)

    # message('['world', 'hello']')
    # message('StartNextLevel')
    def __send(self, answer):
        msg = "message('%s')" % answer
        print('Sending:\n', msg)
        self.socket.send(msg)

    def run(self, on_turn=lambda x, y, z: print('TODO: do something')):
        self.on_turn = on_turn
        self.socket.run_forever()

    def on_message(self, ws, message):
        message = message[6:]
        data = json.loads(message)
        self.on_turn(self, data['level'], data['questions'])

    def on_error(self, ws, error):
        print("### error ###")
        print(error)

    def on_close(self, ws):
        print("### closed ###")

    def start_next_level(self):
        self.__send('StartNextLevel')

    def skip_this_level(self):
        self.__send('SkipThisLevel')

    def send_answers(self, answers=[]):
        answers = ','.join(list(map(lambda s: '\'%s\'' % s, answers)))
        self.__send("[%s]" % answers)
