package main

import (
	"log"
	"bufio"
	"os"
	"lib"
)

const (
	//server_address = "epruizhw0172.moscow.epam.com:8080"
	SERVER_ADDRESS = "localhost:8080"
	PLAYER_NAME    = "go1@mail.org"
	AUTH_CODE      = "20488755882143699524"
)

func turn(gc lib.GameClient, level int, questions []string) {
	switch len(questions) {
	case 0:
		gc.StartNextLevel()
		break
	default:
		answers := make([]string, 0)
		for _, q := range questions {
			answers = append(answers, solve(level, q))
		}
		gc.SendAnswers(answers)
	}
}

func solve(level int, question string) string {
	switch level {
	case 0:
		switch question {
		case "hello":
			return "world"
		case "world":
			return "hello"
		default:
			return question
		}
	default:
		return "TODO: solve quiz"
	}
}

func main() {
	if c, e := lib.NewGameClient(SERVER_ADDRESS, PLAYER_NAME, AUTH_CODE); e == nil {
		c.Run(turn)
		defer c.Close()
	} else {
		log.Fatal("### error ###", e)
	}

	bufio.NewReader(os.Stdin).ReadByte()
}
