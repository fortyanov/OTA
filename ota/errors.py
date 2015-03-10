# -*- coding: utf-8 -*-


class APIError(Exception):
    """
        Ошибка API
    """
    pass


class ServerDown(Exception):
    """
        Запрашиваемый сервер не отвечает
    """
    pass


class Exception403(Exception):
    """
        403
    """
    pass


class WrongContent(Exception):
    """
        Исключение для отсутствия нужного аудио-файла
    """
    pass


class NotUnique(Exception):
    """
        Исключение для попытки создать объект с повтором уникального поля
    """
    pass


class ObjectLocked(Exception):
    """
        Отказ от удаления, если объект занят в трансляции
    """


class STBNotExist(Exception):
    """
        На случай передачи неверного приемника
    """


class MessageNotExist(Exception):
    """
        На случай передачи неверного сообщения
    """


class GroupNotExist(Exception):
    """
        На случай передачи неверной группы
    """


class NoDefaultException(Exception):
    """
        Попытка удалить конфиг по-умолчанию
    """


class SimultaneousMessagesAddrOverlap(Exception):
    """
        Одновременные сообщения имеют пересечения адресов
    """


class SimultaneousMessagesConfigOverlap(Exception):
    """
        Одновременные сообщения имеют пересечения адресов
    """


class PriorityNotExists(Exception):
    """
        Не создано ни одного приоритета
    """


class AddressesOverlap(Exception):
    """
        Пеересечение адресов
    """
    def __init__(self, mask, addr):
        self.value = (mask, addr)


class WrongConfig(Exception):
    """
        Несуществующая конфигурация
    """


class WebSTBExists(Exception):
    """
        На вебе запрещаем добавлять с тем же серийником
    """


class ChannelNotExist(Exception):
    """
        Канал не существует
    """


class WrongGeneratorType(Exception):
    """
        Канал не существует
    """


class WrongGenerator(Exception):
    """
        Канал не существует
    """


class WrongAuthorisation(Exception):
    """
        Ошибка при авторизации на удаленный сервер
    """

class WrongServerSetting(Exception):
    """
    Файл настроек сервера отсутствует или некорректен
    """