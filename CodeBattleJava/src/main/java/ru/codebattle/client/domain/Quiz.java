package ru.codebattle.client.domain;


import lombok.Data;

import java.util.List;

import static java.util.Collections.emptyList;

@Data
public class Quiz {
    private int level;
    private List<String> questions = emptyList();
}
