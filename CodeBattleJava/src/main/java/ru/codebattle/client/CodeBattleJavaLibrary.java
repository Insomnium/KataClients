package ru.codebattle.client;


import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;
import lombok.extern.slf4j.Slf4j;
import org.java_websocket.client.WebSocketClient;
import org.java_websocket.handshake.ServerHandshake;
import ru.codebattle.client.domain.Quiz;

import java.net.URI;
import java.net.URISyntaxException;
import java.util.List;
import java.util.function.BiConsumer;

import static java.lang.String.format;
import static java.util.Optional.ofNullable;

@Slf4j
public class CodeBattleJavaLibrary extends WebSocketClient {
    private final Gson gson = new Gson();
    private BiConsumer<Integer, List<String>> handler;

    public CodeBattleJavaLibrary(String serverAddress, String user, String code) throws URISyntaxException {
        super(new URI(format("ws://%s/codenjoy-contest/ws?user=%s&code=%s", serverAddress, user, code)));
    }

    @Override
    public void onOpen(ServerHandshake handShakeData) {
        log.info("Connection established");
    }

    @Override
    public void onClose(int code, String reason, boolean remote) {
        log.warn("### disconnected ###");
    }

    @Override
    public void onError(Exception ex) {
        log.error("### error ###", ex);
    }

    @Override
    public void onMessage(String message) {
        ofNullable(message)
                .filter(s -> message.length() >= 6)
                .map(s -> gson.fromJson(message.substring(6), Quiz.class))
                .map(quiz -> {
                    handler.accept(quiz.getLevel(), quiz.getQuestions());
                    return null;
                });
    }

    public void startNextLevel() {
        sendMsg("StartNextLevel");
    }

    public void skipThisLevel() {
        sendMsg("SkipThisLevel");
    }

    public void sendAnswers(List<String> answers) {
        sendMsg(gson.toJson(answers, new TypeToken<List<String>>() {}.getType()));
    }

    private void sendMsg(String msg) {
        msg = format("message('%s')", msg);
        log.info("Sending: {}", msg);
        send(msg);
    }

    public void run(BiConsumer<Integer, List<String>> handler) {
        this.handler = handler;
        connect();
    }

    @Override
    protected void finalize() throws Throwable {
        close();
    }
}
