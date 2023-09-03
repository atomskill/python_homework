"""
Socket клиент для получения и отправки метрик
"""

from typing import Optional

import socket
from time import time

class Client():
    """ Класс Client преднозначен для отправки и приёма метрик на стороне клиента
        Для этого используются методы put и get
    """

    def __init__(self, host: str, port: int, timeout: Optional[int] = None) -> None:
        """ Задаём кортеж server, включающий в себя host и port, и необязательный параметр timeout для подключения к серверу """
        self.server = (host, port)
        self.timeout = timeout
    
    def put(self, key: str, value: float, timestamp: Optional[int]) -> None:
        """ Метод put отправляет на сервер имя клиента и его параметр через точку, 
            значение параметра и время, когда были полученны данные
            
            Если timestamp не задан, то к timestamp приравнивается текущее время системы в секундах 
        """
        timestamp = timestamp or int(time())
        
        """ Подключаемся к серверу и отправляем данные """
        with socket.create_connection(self.server, self.timeout) as connect:
            connect.sendall( f"put {key} {value} {timestamp}\n".encode('utf-8'))
            answer = connect.recv(1024)
        
        """ Проверяем, что сервер отработал запрос корректно 
            Вызываем исключение если нет
        """
        if answer.decode('utf-8') != 'ok\n\n':
            raise ClientError("Bad Request")
    
    def get(self, key: str) -> dict[str, tuple[float, int]]:
        """ Метод get принимает метрики с сервера и возвращает словарь
            Ключём словаря является сервер и его параметр через точку, а значением - кортеж
            В каждом кортеже находится значение параметра и время в секундах, когда он был получен 

            Подключаемся к серверу и отправляем ключ (имя сервера, данные с которого хотим получить)
        """
        with socket.create_connection(self.server, self.timeout) as connect:
            connect.sendall(f"get {key}\n".encode('utf-8'))
            answer = connect.recv(1024).decode('utf-8')
        
        """ Парсим ответ от сервера
            Убираем последнюю пустую строку
        """
        ansObjs = answer.splitlines()[0:-1]

        """Проверяем что сервер отработал корректно, иначе вызываем исключение"""
        if ansObjs.pop(0) != 'ok':
            raise ClientError("Bad Request")
        
        """Создаём словарь и заполняем его данными, которые вернул нам сервер"""
        metrics = {}
        for m in ansObjs:
            ms = m.split()
            key = ms[0]
            timestamp = float(ms[1])
            value = float(ms[2])
            if key not in metrics:
                metrics[key] = [(value, timestamp)]
            else:
                metrics[key].append((value, timestamp))
        
        """Сортируем данные по параметру timestamp (от меньшего к большему)"""
        for key in metrics:
            metrics[key] = sorted(metrics[key], key=lambda x: x[1], reverse=True)
        return metrics

class ClientError(Exception):
    def __init__(self, message):
        super().__init__(message)
