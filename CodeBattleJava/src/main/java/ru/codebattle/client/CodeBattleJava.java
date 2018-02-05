package ru.codebattle.client;


import lombok.SneakyThrows;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

import static java.util.Collections.unmodifiableMap;
import static java.util.stream.Collectors.toList;

public class CodeBattleJava {

    private static final String SERVER_ADDRESS = "localhost:8080";
    private static final String PLAYER_NAME = "katatonia@mail.org";
    private static final String AUTH_CODE = "1085963739701489268";
    private static final Map<String, String> ANSWERS_STUB = unmodifiableMap(
            new HashMap<String, String>() {{
                put("hello", "world");
                put("world", "hello");
            }}
    );

    @SneakyThrows
    public static void main(String[] args) {
        CodeBattleJavaLibrary client = new CodeBattleJavaLibrary(SERVER_ADDRESS, PLAYER_NAME, AUTH_CODE);
        client.run((level, questions) -> {
            if (questions.isEmpty()) {
                client.startNextLevel();
            } else {
                List<String> answers = questions
                        .stream()
                        .map(q -> solve(level, q))
                        .collect(toList());
                client.sendAnswers(answers);
            }
        });
    }

    private static String solve(Integer level, String question) {
        switch (level) {
            case 0:
                return ANSWERS_STUB.getOrDefault(question, question);
            default:
                return "TODO: solve quiz";
        }
    }
}
