from .repositorio import RepositorioMonitoreo, repositorio_monitoreo


class ServicioMonitoreo:
    def __init__(self, repositorio: RepositorioMonitoreo = repositorio_monitoreo) -> None:
        self.repositorio = repositorio

    def obtener_estado(self) -> dict[str, object]:
        return self.repositorio.obtener_estado()

    def registrar_falla(self, servicio: str, detalle: str | None = None) -> dict[str, object]:
        return self.repositorio.registrar_falla(servicio, detalle)

    def recuperar(self, servicio: str | None = None) -> dict[str, object]:
        return self.repositorio.recuperar(servicio)


estado_monitoreo = ServicioMonitoreo()
