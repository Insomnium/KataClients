package ru.codebattle.client;


import lombok.SneakyThrows;

import java.util.List;

import static java.util.stream.Collectors.toList;

public class CodeBattleJava {

    private static final String SERVER_ADDRESS = "epruizhw0172.moscow.epam.com:8080";
    private static final String PLAYER_NAME = "java@mail.org";
    private static final String AUTH_CODE = "2980396691258897741";

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
                switch (question) {
                    case "hello":
                        return "world";
                    case "world":
                        return "hello";
                    default:
                        return question;
                }
            default:
                return "TODO: solve quiz";
        }
    }
}
