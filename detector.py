class DetectorSpam:
    """
    Motor encargado de gestionar las reglas de filtrado
    y evaluar si un correo supera el umbral de spam.
    """
    def __init__(self, umbral=5.0):
        # Encapsulamiento con atributos privados
        self.__umbral = float(umbral)
        self.__reglas = []  # Estructura de datos: lista de reglas

    # --- Getters y Setters ---
    def get_umbral(self):
        return self.__umbral

    def set_umbral(self, nuevo_umbral):
        if nuevo_umbral >= 0:
            self.__umbral = float(nuevo_umbral)
        else:
            print("El umbral debe ser un valor positivo.")

    def get_reglas(self):
        return self.__reglas

    # --- Métodos principales ---
    def agregar_regla(self, regla):
        """Agrega un objeto de tipo Regla a la lista del detector."""
        self.__reglas.append(regla)

    def analizar(self, correo):
        """
        Evalúa el correo contra todas las reglas registradas.
        Calcula el puntaje acumulado, registra los motivos y 
        determina si es clasificado como spam.
        """
        puntaje_total = 0.0
        motivos = []

        # Recorrido polimórfico de las reglas
        for regla in self.__reglas:
            puntos, motivo = regla.evaluar(correo)
            if puntos > 0:
                puntaje_total += puntos
                motivos.append(f"{motivo} (+{puntos} pts)")

        # Asignamos el puntaje final al correo mediante su setter
        correo.set_puntaje(puntaje_total)

        # Si supera o iguala el umbral, se clasifica como spam
        if puntaje_total >= self.__umbral:
            correo.marcar_como_spam(motivos)
            return True
        return False