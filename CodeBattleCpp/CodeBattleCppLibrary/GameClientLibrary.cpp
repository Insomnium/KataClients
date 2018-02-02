#include "GameClientLibrary.h"
#include "rapidjson/document.h"
#include "rapidjson/stringbuffer.h"

#include <iostream>

using namespace rapidjson;

GameClientLibrary::GameClientLibrary(std::string _server, std::string _user, std::string _code)
{
	path = "ws://" + _server + "/codenjoy-contest/ws?user=" + _user + "&code=" + _code;
	is_running = false;
}

GameClientLibrary::~GameClientLibrary()
{
	is_running = false;
	work_thread->join();
}

void GameClientLibrary::Run(std::function<void()> _message_handler)
{
	is_running = true;
	work_thread = new std::thread(&GameClientLibrary::update_func, this, _message_handler);
}

void GameClientLibrary::update_func(std::function<void()> _message_handler)
{
#ifdef _WIN32
	WSADATA wsaData;

	if (WSAStartup(MAKEWORD(2, 2), &wsaData))
		throw new std::exception("### error ###");
	else
		std::cout << "Connection established" << std::endl;
#endif

	web_socket = easywsclient::WebSocket::from_url(path);
	if (web_socket == nullptr)is_running = false;
	while (is_running)
	{
		web_socket->poll();
		web_socket->dispatch([&](const std::string &message)
		{
			std::string msg = message.substr(6, message.length());
			const char *cstr = msg.c_str();
			Document d;
			d.Parse(cstr);
			level = d["level"].GetInt();
			Value& qArray = d["questions"];
			questions.clear();
			if (qArray.IsArray()) {
				for (SizeType i = 0; i < qArray.Size(); i++) {
					std::string q = qArray[i].GetString();
					questions.push_back(q);
				}
			}

			_message_handler();
		});
	}
	if (web_socket)web_socket->close();

#ifdef _WIN32
	WSACleanup();
#endif
}
