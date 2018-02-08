using System;
using System.Collections.Generic;
using CodeBattleNetLibrary;

namespace CodeBattleNet
{
	internal static class Program
	{
		public static void Main()
		{
			var gcb = new GameClientKata("epruizhw0172.moscow.epam.com:8080", "farkhad_muminov@epam.com", "5298793271048750521");
            gcb.Run(() =>
            {
                if (gcb.Questions.Count == 0)
                {
                    gcb.StartNextLevel();
                }
                else
                {
                    var answers = new List<string>();
                    foreach (var q in gcb.Questions)
                    {
                        answers.Add(solve(gcb.Level, q));
                    }
                    gcb.SendAnswers(answers);
                }
			});

			Console.ReadKey();
		}

        private static string solve(int level, string question)
        {
            switch(level)
            {
                case 0:
                    {
                        if (question.Equals("hello"))
                        {
                            return "world";
                        }
                        if (question.Equals("world"))
                        {
                            return "hello";
                        }
                        return question;                
                    }
                default:
                    return "TODO: solve quiz";
            }
        }
	}
}
