answer_dict = {
    # Запрос выполнен успешно.
    200 : {
        "status" : 200,
        "message" : "ok"
    },
    
    # Объект успешно создан в коллекции.
    201 : {
        "status" : 201,
        "message" : "Succeful created"
    },
    
    # Запрос принят, но еще выполняется.
    202 : {
        "status" : 202,
        "message" : "Request Accepted"
    },
    
    # Неавторитетная (не из оффициального источника) информация 
    203 : {
        "status": 203,
        "message" : "Non-Authoritative Information"
    },
    
    # Отсутсвует контент в запросе
    204 : {
        "status" : 204,
        "message" : "No Content"
    },

    # Запрос обработан, необходимо обновить данные.
    205 : {
        "status" : 205,
        "message" : "Reset Content"
    },

    # Запрос выполнен частично
    206 : {
        "status" : 206,
        "message" : "Partial Content"
    },

    # Несколько вариантов ответов
    300 : {
        "status" : 300,
        "message" : "Multiple Choise"
    },

    # URL перемещен на новый ROUT навсегда
    301 : {
        "status" : 301,
        "message" : "Moved Permanently"
    },

    # Перенаправление на другой URL
    302 : {
        "status" : 302,
        "message" : "Found"
    },

    # URL закрыт (должен предоставляться другой URL)
    303 : {
        "status" : 303,
        "message" : "See Other"
    },

    # Неизменяемые данные в коллекции
    304 : {
        "status" : 304,
        "message" : "Not Modified"
    },

    # Запрос должен осуществляться через прокси 
    305 :{
        "status" : 305,
        "message" : "Use Proxy"
    },

    # Единоразовое перенаправление (необходимо добавить поле "Location")
    # Однако дальнейшие запросы необходимо направлять на этот URL.
    307 :{
        "status" : 307,
        "message" : "Temporary Redirect"
    },

    # Повторить запрос на новый URL, без изменения метода запроса.
    308 :{
        "status" : 308,
        "message" : "Permanent Redirect"
    },

    # Ошибка на стороне клиента
    400 : {
        "status" : 400,
        "message" : "Bad Request"
    },

    # Попытка использовать ROUT без обязательной авторизации
    401 : {
        "status" : 401,
        "message" : "Not authorization"
    },

    # Необходима оплата для продолжения
    402 : {
        "status" : 402,
        "message" : "Payment Required"
    },

    # Запрещен доступ для клиента
    403 :{
        "status" : 403,
        "message" : "Forbidden"
    },

    # Запрошенных данных не найдено
    404 : {
        "status" : 404,
        "message" : "Not Found"
    },

    # Метод для данного ROUT запрещен
    405 : {
        "status" : 405,
        "message" : "Method Not Allowed"
    },
    
    # Неприемлимый тип данных
    406 :{
        "status" : 406,
        "message" : "Not Acceptable"
    },

    # Требуется прокси-ауентификация
    407 : {
        "status" : 407,
        "message" : "Proxy Authentication Required"
    },

    # Тайм-аут запроса
    408 :{
        "status" : 408,
        "message" : "Request Timeout"
    },

    # Конфликт, невозможно обработать запрос
    409 :{
        "status" : 409,
        "message" : "Conflict"
    },

    # Данные были, но сейчас их нет
    410 : {
        "status" : 410,
        "message" : "Gone"
    },

    # Требуется длина, укажите при повтороном запросе
    411 :{
        "status" : 411,
        "message" : "Length Required"
    },

    # Предварительное условие не выполнено
    412 :{
        "status" : 412,
        "message" : "Precondition Failed"
    },

    # Сущность запроса слишком длинная
    413 :{
        "status" : 413,
        "message" : "Request Entity Too Large"
    },

    # URL слишком длинный
    414 :{
        "status" : 414,
        "message" : "Request-URI Too Long"
    },

    # Неподдерживаемый тип контента
    415 :{
        "status" : 415,
        "message" : "Unsupported Media Type"
    },

    # Требуется предварительное условие
    428 :{
        "status" : 428,
        "message" : "Precondition Required"
    },

    # Слишком много запросов, повторите позже
    429 :{
        "status" : 429,
        "message" : "Too Many Requests"
    },

    # Слишком большие поля заголовков запроса
    431 :{
        "status" : 431,
        "message" : "Request Header Fields Too Large"
    },

    # Нет ответа от сервера
    444 :{
        "status" : 444,
        "message" : "No Response - Нет ответа"
    },

    # Нет доступа по юридечиским причинам
    451 :{
        "status" : 451,
        "message" : "Unavailable For Legal Reasons"
    },

    # Внутренняя ошибка сервера
    500 :{
        "status" : 500,
        "message" : "Internal Server Error"
    },

    # Данный метод не реализован
    501 :{
        "status" : 501,
        "message" : "Not Implemented"
    },

    # Плохой шлюз
    502 :{
        "status" : 502,
        "message" : "Bad Gateway"
    },

    # Служба недоступна
    503 :{
        "status" : 503,
        "message" : "Service Unavailable"
    },

    # Тайм-аут шлюза
    504 :{
        "status" : 504,
        "message" : "Gateway Timeout"
    },

    # Версия HTTP не поддерживается
    505 :{
        "status" : 505,
        "message" : "HTTP Version Not Supported"
    },

    # Отсутсвует доступ (Необходимо вернуть информацию, которой не достаточно)
    510 : {
        "status" : 510,
        "message" : "Not Extended"
    }
}