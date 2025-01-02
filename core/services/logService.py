import os
import json
import datetime


class LogException:
    filePath = os.environ.get("LOCALAPPDATA") + "\\LogEstheticApp"

    @staticmethod
    def write_data(errorText, line=None, app=None, type=None, nameFunc=None, classError=None, data=None, rout=None, method=None, code=None) -> None:
        """
        key default:
        errorText - Текст ошибки
        line - строка, в которой возникла обработка ошибки
        app - приложение, в котором возникла ошибка
        type - Тип исключения
        stage - Этап работы приложения
        classError - Важность ошибки
        data - Дополнительная информация
        rout - Роут, по которому сделан запрос
        method - Метод, по которому сделан запрос
        code - Код ошибки, который был возвращен
        """
        if not LogException.__is_file():
            with open(LogException.filePath, "w") as file:
                file.write(f"{'--|' * 10}")


        current_datetime = str(datetime.datetime.now().date()).replace("-", ".") + " -- " + str(datetime.datetime.now().time())
        formatWrite = f"""
{current_datetime} <> {classError} : {errorText}
{rout} <> {method} <> {app}
{nameFunc} <> {line}
{type} <> {code}
Information : {data}

{'--|' * 10}
"""
        with open(LogException.filePath, "a") as file:
            file.write(formatWrite)

        return True



    
    @staticmethod
    def read_log():
        pass



    @staticmethod
    def __is_file():
        return os.path.isfile(LogException.filePath)


    