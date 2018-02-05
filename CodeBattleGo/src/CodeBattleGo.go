package main

import (
	"fmt"
	"github.com/gorilla/websocket"
	"log"
	"bufio"
	"os"
	"encoding/json"
)

const (
	//server_address = "epruizhw0172.moscow.epam.com:8080"
	server_address = "localhost:8080"
	player_name    = "go@mail.org"
	auth_code      = "4649363151970985220"
)

type Quiz struct {
	Level     int
	Questions []string
}

func (q Quiz) String() string {
	return fmt.Sprintf("Level: %d; Questions: %s", q.Level, q.Questions)
}

func main() {
	url := fmt.Sprintf("ws://%s/codenjoy-contest/ws?user=%s&code=%s", server_address, player_name, auth_code)

	log.Printf("connecting ... %s", url)
	conn, _, e := websocket.DefaultDialer.Dial(url, nil)
	defer conn.Close()

	if e != nil {
		log.Fatal("dial: ", e)
	}
	log.Println("Connection established ")

	done := make(chan Quiz)
	defer close(done)

	go func() {
		//defer conn.Close()
		//defer close(done)

		for {
			_, msg, err := conn.ReadMessage()
			if err != nil {
				fmt.Println("### error ###", err)
			}
			var quiz Quiz
			json.Unmarshal(msg[6:], &quiz)
			done <- quiz
		}
	}()

	go func() {
		for {
			quiz := <-done
			log.Printf("Received: %s", quiz)

			switch len(quiz.Questions) {
			case 0:
				//	TODO: start next level
				log.Println("About to start next level")
				break;
			default:
				answers := make([]string, 0)
				for _, q := range quiz.Questions {
					answers = append(answers, solve(quiz.Level, q))
				}
				//	TODO: send answers
				log.Printf("About to send answers: %s", answers)
			}
		}
	}()

	bufio.NewReader(os.Stdin).ReadByte()
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
