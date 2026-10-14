import re


class Regla:
    """Clase base. Cada regla devuelve (puntaje, motivo)."""

    def __init__(self, nombre, peso=1):
        self._nombre = nombre
        self._peso = peso

    def get_nombre(self):
        return self._nombre

    def get_peso(self):
        return self._peso

    def evaluar(self, correo):
        raise NotImplementedError("Las reglas hijas deben implementar evaluar()")


class ReglaPalabrasClave(Regla):
    def __init__(self, palabras=None, peso=2):
        super().__init__("Palabras clave", peso)
        self._palabras = palabras or ["gratis", "premio", "urgente", "ganaste", "oferta"]

    def evaluar(self, correo):
        texto = (correo.get_asunto() + " " + correo.get_cuerpo()).lower()
        encontradas = [p for p in self._palabras if p in texto]
        if encontradas:
            return len(encontradas) * self._peso, f"contiene {', '.join(encontradas)}"
        return 0, ""


class ReglaRemitente(Regla):
    def __init__(self, lista_negra=None, peso=5):
        super().__init__("Remitente sospechoso", peso)
        self._lista_negra = lista_negra or ["promo-ya.com", "ganadores.net", "gratis.xyz"]

    def evaluar(self, correo):
        remitente = correo.get_remitente().lower()
        for dominio in self._lista_negra:
            if remitente.endswith(dominio):
                return self._peso, f"remitente en lista negra ({dominio})"
        return 0, ""


class ReglaEnlaces(Regla):
    def __init__(self, max_enlaces=2, peso=2):
        super().__init__("Enlaces", peso)
        self._max_enlaces = max_enlaces

    def evaluar(self, correo):
        enlaces = re.findall(r"https?://\S+", correo.get_cuerpo())
        if len(enlaces) > self._max_enlaces:
            return self._peso, f"tiene {len(enlaces)} enlaces"
        return 0, ""


class ReglaMayusculas(Regla):
    def __init__(self, peso=3):
        super().__init__("Mayúsculas y exclamaciones", peso)

    def evaluar(self, correo):
        asunto = correo.get_asunto()
        motivos = []
        if asunto.isupper() and len(asunto) > 3:
            motivos.append("asunto en mayúsculas")
        if asunto.count("!") >= 3:
            motivos.append("muchos signos de exclamación")
        if motivos:
            return self._peso, ", ".join(motivos)
        return 0, ""
