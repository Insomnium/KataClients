class GameClient {

    constructor(server, user, code) {
        this.path = "ws://" + server + "/codenjoy-contest/ws?user=" + user + "&code=" + code
    }

    run(callback) {
        this.socket = new WebSocket(this.path);
        this.socket.onopen = this.onOpen;
        this.socket.onerror = this.onError;
        this.socket.onclose = this.onClose;
        this.socket.onmessage = function (event) {
            let data = JSON.parse(event.data.substring(6));
            callback(data.level, data.questions);
        }
    }

    __send(answer) {
        let msg = 'message(\'' + answer + '\')';
        text.value += 'Sending: ' + msg + '\n';
        this.socket.send('message(\'' + answer + '\')');
    };

    startNextLevel() {
        this.__send('StartNextLevel')
    }

    skipThisLevel() {
        this.__send('SkipThisLevel')
    }

    sendAnswers(answers = []) {
        this.__send(JSON.stringify(answers))
    }

    set textArea(text) {
        this.text = text
    }

    onOpen() {
        text.value += "Connection established\n";
    }

    onClose(event) {
        if (event.wasClean) {
            text.value += "### disconnected ###\n"
        } else {
            text.value += "### accidentally disconnected ###\n";
            text.value += " - Err code: " + event.code + ", Reason: " + event.reason + "\n";
        }
    }

    onError(error) {
        text.value += "### error ###\n" + error.message + "\n";
    }
}
