"""
Socket клиент для получения и отправки метрик
"""

from typing import Union

import socket
from time import time

class Client():
    def __init__(self, host: str, port: int, timeout: Union[int, None] = None) -> None:
        """ Задаём значения host, port и необязательный параметр timeout для подключения к серверу """
        self.host = host
        self.port = port
        self.timeout = timeout
    
    def put(self, key: str, value: float, timestamp: Union[int, None]) -> None:
        """ Метод put отправляет на сервер имя клиента и его параметр через точку, 
            значение параметра и время, когда были полученны данные
            
            Если timestamp не задан, то к timestamp приравнивается текущее время системы в секундах 
        """
        if timestamp == None:
            timestamp = int(time())
        
        """ Подключаемся к серверу и отправляем данные """
        with socket.create_connection((self.host, self.port), self.timeout) as connect:
            connect.sendall( f"put {key} {value} {timestamp}\n".encode('utf-8'))
            answer = connect.recv(1024)
        
        """ Проверяем, что сервер отработал запрос корректно 
            Вызываем исключение если нет
        """
        if answer.decode('utf-8').split('\n')[0] != 'ok':
            raise ClientError("Bad Request")
    
    def get(self, key: str) -> dict[str, tuple[float, int]]:
        """ Метод get принимает метрики с сервера и возвращает словарь
            Ключём словаря является сервер и его параметр через точку, а значением - кортеж
            В каждом кортеже находится значение параметра и время в секундах, когда он был получен 

            Подключаемся к серверу и отправляем ключ (имя сервера, данные с которого хотим получить)
        """
        with socket.create_connection((self.host, self.port), self.timeout) as connect:
            connect.sendall(f"get {key}\n".encode('utf-8'))
            answer = connect.recv(1024).decode('utf-8')
        
        """Парсим ответ от сервера"""
        ansObjs = answer.split('\n')

        """Проверяем что сервер отработал корректно, иначе вызываем исключение"""
        if ansObjs[0] != 'ok':
            raise ClientError("Bad Request")
        
        """Создаём словарь и заполняем его данными, которые вернул нам сервер"""
        metrics = {}
        for m in ansObjs:
            if(m == 'ok' or m == ''): continue
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
