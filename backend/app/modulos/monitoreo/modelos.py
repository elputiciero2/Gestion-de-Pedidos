from dataclasses import dataclass, field
from datetime import datetime, timezone


def _ahora_utc() -> datetime:
    return datetime.now(timezone.utc)


@dataclass(slots=True)
class ServicioMonitoreado:
    nombre: str
    tipo: str
    ruta: str
    estado: str = "ok"
    detalle: str = "operativo"
    ultimo_evento: datetime = field(default_factory=_ahora_utc)

    def marcar_falla(self, detalle: str | None = None) -> None:
        self.estado = "falla"
        self.detalle = detalle or f"{self.nombre} no responde"
        self.ultimo_evento = _ahora_utc()

    def recuperar(self) -> None:
        self.estado = "ok"
        self.detalle = "operativo"
        self.ultimo_evento = _ahora_utc()

    def como_diccionario(self) -> dict[str, object]:
        return {
            "nombre": self.nombre,
            "tipo": self.tipo,
            "ruta": self.ruta,
            "estado": self.estado,
            "detalle": self.detalle,
            "ultimo_evento": self.ultimo_evento.isoformat(),
        }


def _crear_servicios() -> dict[str, ServicioMonitoreado]:
    servicios = [
        ServicioMonitoreado("nginx", "proxy", "http://nginx"),
        ServicioMonitoreado("backend-nodo-1", "api", "http://backend-nodo-1:8001/api/salud"),
        ServicioMonitoreado("backend-nodo-2", "api", "http://backend-nodo-2:8002/api/salud"),
        ServicioMonitoreado("mysql-nodo-1", "base_datos", "mysql-nodo-1:3306"),
        ServicioMonitoreado("mysql-nodo-2", "base_datos", "mysql-nodo-2:3306"),
        ServicioMonitoreado("mysql-nodo-3", "base_datos", "mysql-nodo-3:3306"),
        ServicioMonitoreado("phpmyadmin", "herramienta", "http://localhost:8081"),
    ]
    return {servicio.nombre: servicio for servicio in servicios}


@dataclass(slots=True)
class EstadoNodo:
    servicios: dict[str, ServicioMonitoreado] = field(default_factory=_crear_servicios)
    servicio_afectado: str | None = None
    incidencia_actual: dict[str, object] | None = None
    ultima_incidencia: dict[str, object] | None = None
    actualizado_en: datetime = field(default_factory=_ahora_utc)

    def _actualizar(self) -> None:
        self.actualizado_en = _ahora_utc()

    def _servicio_o_error(self, nombre: str) -> ServicioMonitoreado:
        if nombre not in self.servicios:
            raise ValueError(f"Servicio no monitoreado: {nombre}")
        return self.servicios[nombre]

    def registrar_falla(self, servicio: str, detalle: str | None = None) -> None:
        servicio_monitoreado = self._servicio_o_error(servicio)
        servicio_monitoreado.marcar_falla(detalle)
        self.servicio_afectado = servicio
        self.incidencia_actual = {
            "servicio": servicio,
            "detalle": servicio_monitoreado.detalle,
            "estado": "activa",
            "detectado_en": self.actualizado_en.isoformat(),
        }
        self.ultima_incidencia = self.incidencia_actual.copy()
        self._actualizar()
        self.incidencia_actual["detectado_en"] = self.actualizado_en.isoformat()
        self.ultima_incidencia["detectado_en"] = self.actualizado_en.isoformat()

    def recuperar(self, servicio: str | None = None) -> None:
        objetivo = servicio or self.servicio_afectado
        if objetivo:
            servicio_monitoreado = self._servicio_o_error(objetivo)
            servicio_monitoreado.recuperar()
            if self.incidencia_actual and self.incidencia_actual.get("servicio") == objetivo:
                self.incidencia_actual = None
            self.servicio_afectado = None
            if self.ultima_incidencia and self.ultima_incidencia.get("servicio") == objetivo:
                self.ultima_incidencia["estado"] = "resuelta"
                self.ultima_incidencia["resuelta_en"] = _ahora_utc().isoformat()
        else:
            for servicio_monitoreado in self.servicios.values():
                servicio_monitoreado.recuperar()
            self.servicio_afectado = None
            self.incidencia_actual = None
        self._actualizar()

    def _resumen(self) -> dict[str, int]:
        total = len(self.servicios)
        caidos = sum(1 for servicio in self.servicios.values() if servicio.estado != "ok")
        return {
            "total": total,
            "operativos": total - caidos,
            "caidos": caidos,
        }

    def _diagnostico(self) -> str:
        if self.incidencia_actual:
            return f"{self.incidencia_actual['servicio']} presenta una incidencia activa"
        caidos = [servicio.nombre for servicio in self.servicios.values() if servicio.estado != "ok"]
        if caidos:
            return f"Servicios caídos: {', '.join(caidos)}"
        return "Todos los servicios operativos"

    def _recomendaciones(self) -> list[str]:
        recomendaciones = [
            "Revisar el panel de servicios para identificar el nodo caído.",
            "Confirmar conectividad entre NGINX, los dos backends y el clúster MySQL.",
        ]
        if self.incidencia_actual:
            recomendaciones.append(
                f"Revisar la incidencia activa en {self.incidencia_actual['servicio']} y validar la ruta {self.servicios[self.incidencia_actual['servicio']].ruta}."
            )
        return recomendaciones

    def como_diccionario(self) -> dict[str, object]:
        estado = "falla" if self._resumen()["caidos"] else "ok"
        return {
            "estado": estado,
            "detalle": self._diagnostico(),
            "actualizado_en": self.actualizado_en.isoformat(),
            "resumen": self._resumen(),
            "servicio_afectado": self.servicio_afectado,
            "servicios": [servicio.como_diccionario() for servicio in self.servicios.values()],
            "incidencia_actual": self.incidencia_actual,
            "ultima_incidencia": self.ultima_incidencia,
            "recomendaciones": self._recomendaciones(),
        }
