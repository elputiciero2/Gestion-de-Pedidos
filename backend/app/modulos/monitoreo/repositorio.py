from .modelos import EstadoNodo


class RepositorioMonitoreo:
    def __init__(self, estado: EstadoNodo | None = None) -> None:
        self.estado = estado or EstadoNodo()

    def obtener_estado(self) -> dict[str, object]:
        return self.estado.como_diccionario()

    def registrar_falla(self, servicio: str, detalle: str | None = None) -> dict[str, object]:
        self.estado.registrar_falla(servicio, detalle)
        return self.obtener_estado()

    def recuperar(self, servicio: str | None = None) -> dict[str, object]:
        self.estado.recuperar(servicio)
        return self.obtener_estado()


repositorio_monitoreo = RepositorioMonitoreo()
