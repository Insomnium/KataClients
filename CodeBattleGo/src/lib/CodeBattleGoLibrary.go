package lib

import (
	"github.com/gorilla/websocket"
	"fmt"
	"log"
	"encoding/json"
)

type quiz struct {
	Level     int
	Questions []string
}

type GameClient struct {
	conn *websocket.Conn
	msg  chan quiz
}

type Handler func(gc GameClient, level int, questions []string);

func (q quiz) String() string {
	return fmt.Sprintf("level: %d; Questions: %s", q.Level, q.Questions)
}

func NewGameClient(serverAddress, playerName, authCode string) (*GameClient, error) {
	url := fmt.Sprintf("ws://%s/codenjoy-contest/ws?user=%s&code=%s", serverAddress, playerName, authCode)
	log.Printf("connecting ... %s", url)

	if conn, _, e := websocket.DefaultDialer.Dial(url, nil); e == nil {
		log.Println("Connection established ")
		return &GameClient{
			conn: conn,
			msg:  make(chan quiz),
		}, nil
	} else {
		return nil, e
	}
}

func (c GameClient) Run(handler Handler) {
	go func() {
		for {
			_, msg, e := c.conn.ReadMessage()
			if e != nil {
				log.Println("### error ###", e)
			}
			var quiz quiz
			json.Unmarshal(msg[6:], &quiz)
			c.msg <- quiz
		}
	}()

	go func() {
		for {
			quiz := <-c.msg
			log.Printf("Received: %s", quiz)
			handler(c, quiz.Level, quiz.Questions)
		}
	}()
}

func (c GameClient) SendAnswers(answers []string) {
	msg, _ := json.Marshal(answers)
	c.send(string(msg))
}

func (c GameClient) send(answer string) {
	answer = fmt.Sprintf("message('%s')", answer)
	log.Printf("Sending: %s", answer)
	c.conn.WriteMessage(websocket.TextMessage, []byte(answer))
}

func (c GameClient) Close() {
	c.conn.Close()
	close(c.msg)
}

func (c GameClient) StartNextLevel() {
	c.send("StartNextLevel")
}

func (c GameClient) SkipThisLevel() {
	c.send("SkipThisLevel")
}
