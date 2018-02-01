using System;
using WebSocket4Net;
using Newtonsoft.Json;
using System.Collections.Generic;

namespace CodeBattleNetLibrary
{
	public class GameClientKata
	{
		private readonly WebSocket _socket;
		private event Action OnUpdate;
        public int Level { get; private set; }
        public IList<string> Questions { get; private set; }

        public GameClientKata(string server, string user, string code)
		{
			_socket =
				new WebSocket(
					$"ws://{server}/codenjoy-contest/ws?user={user}&code={code}");
			        _socket.MessageReceived += (s, e) => { ParseField(e.Message); };
		}

		public void Run(Action handler)
		{
			OnUpdate += handler;
			_socket.Open();
		}

		public void Blank()
		{
			_socket.Send("");
		}

        public void sendAnswers(IList<string> answers)
        {
            string msg = JsonConvert.SerializeObject(answers);
            Console.WriteLine(msg);
        }

        private void send(string answer)
        {
            var msg = $"message('{answer}')";
            Console.WriteLine($"Sending: {msg}");
            this._socket.Send(msg);
        }

		private void ParseField(string rawField)
		{
            Quizz quizz = JsonConvert.DeserializeObject<Quizz>(rawField.Substring(6));
            Level = quizz.Level;
            Questions = quizz.Questions;

			OnUpdate?.Invoke();
		}
	}
}
