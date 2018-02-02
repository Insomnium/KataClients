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
            _socket.Opened += new EventHandler(onOpened);
            _socket.Error += new EventHandler<SuperSocket.ClientEngine.ErrorEventArgs>(onError);
            _socket.Closed += new EventHandler(onClose);
		}

        private void onOpened(object sender, EventArgs e)
        {
            Console.WriteLine("Connection established");
        }

        private void onError(object sender, EventArgs e)
        {
            Console.WriteLine("### error ###\n" + e.ToString());
        }

        private void onClose(object sender, EventArgs e)
        {
            Console.WriteLine("### disconnected ###");
        }

        public void Run(Action handler)
		{
			OnUpdate += handler;
			_socket.Open();
		}

        public void StartNextLevel()
        {
            send("StartNextLevel");
        }

        public void SkipThisLevel()
        {
            send("SkipThisLevel");
        }

        public void SendAnswers(IList<string> answers)
        {
            string msg = JsonConvert.SerializeObject(answers);
            send(msg);
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
