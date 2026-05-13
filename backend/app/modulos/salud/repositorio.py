from ..monitoreo.repositorio import repositorio_monitoreo
from .modelos import EstadoSalud


class RepositorioSalud:
    def __init__(self, repositorio_monitoreo_instancia= repositorio_monitoreo) -> None:
        self.repositorio_monitoreo = repositorio_monitoreo_instancia

    def obtener_estado(self) -> EstadoSalud:
        datos = self.repositorio_monitoreo.obtener_estado()
        return EstadoSalud(
            estado=datos["estado"],
            detalle=datos["detalle"],
            actualizado_en=datos["actualizado_en"],
        )


repositorio_salud = RepositorioSalud()
