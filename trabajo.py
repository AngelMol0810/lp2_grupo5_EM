class Correo:
    def __init__(self, remitente, asunto, cuerpo): 
        self.__remitente = remitente
        self.__asunto = asunto
        self.__cuerpo = cuerpo
        self.__es_spam = False
        self.__puntaje = 0
        
