from .repositorio import RepositorioSalud, repositorio_salud


class ServicioSalud:
    def __init__(self, repositorio: RepositorioSalud = repositorio_salud) -> None:
        self.repositorio = repositorio

    def verificar(self) -> dict[str, str]:
        estado = self.repositorio.obtener_estado()
        return {
            "estado": estado.estado,
            "detalle": estado.detalle,
            "actualizado_en": estado.actualizado_en,
        }

    def verificar_detalle(self) -> dict[str, str]:
        return self.verificar()


servicio_salud = ServicioSalud()
