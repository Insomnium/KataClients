#pragma once

#include <string>
#include <thread>
#include "easywsclient\easywsclient.hpp"
#ifdef _WIN32
#pragma comment( lib, "ws2_32" )
#include <WinSock2.h>
#endif
#include <assert.h>
#include <stdio.h>
#include <iostream> 
#include <string>
#include <list>
#include <memory>


class GameClientLibrary
{

	easywsclient::WebSocket *web_socket;
	std::string path;

	uint32_t level;
	std::list<std::string> questions;

	bool is_running;
	std::thread *work_thread;
	void update_func(std::function<void()> _message_handler);

public:
	GameClientLibrary(std::string _server, std::string _user, std::string _code);
	~GameClientLibrary();

	void Run(std::function<void()> _message_handler);	

	void StartNextLevel() {
		_send("StartNextLevel");
	}

	void SkipThisLevel() {
		_send("SkipThisLevel");
	}

	void SendAnswers(std::list<std::string> answers) {		
		_send(prepareArray(answers));
	}

	uint32_t GetLevel() { return level; }
	std::list<std::string> GetQuestions() { return questions; }
private:

	void _send(std::string msg) 
	{
		msg = "message('" + msg + "')";
		std::cout << "Sending: " << msg << std::endl;
		web_socket->send(msg);
	}

	std::string prepareArray(std::list<std::string> _answers)
	{
		std::string jsonArray = "[";
		for (std::list<std::string>::iterator it = _answers.begin(); it != _answers.end(); ++it)
		{
			jsonArray += "'" + *it + "'";
			if (_answers.begin() != _answers.end() && std::next(it) != _answers.end()) {
				jsonArray += ",";
			}
		}
		return jsonArray + "]";
	}
};
