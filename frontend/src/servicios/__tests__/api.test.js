import { CircuitBreaker, RetryManager } from '../api.js';

describe('CircuitBreaker', () => {
  test('debe estar en estado CERRADO inicialmente', () => {
    const breaker = new CircuitBreaker(3, 5000);
    expect(breaker.obtenerEstado()).toBe('CERRADO');
  });

  test('debe cambiar a ABIERTO después de 3 fallos', () => {
    const breaker = new CircuitBreaker(3, 5000);
    breaker.registrarFallo();
    breaker.registrarFallo();
    breaker.registrarFallo();
    expect(breaker.obtenerEstado()).toBe('ABIERTO');
  });

  test('debe permitir intento en estado CERRADO', () => {
    const breaker = new CircuitBreaker(3, 5000);
    expect(breaker.puedeIntentarAhora()).toBe(true);
  });

  test('no debe permitir intento en estado ABIERTO', () => {
    const breaker = new CircuitBreaker(1, 5000);
    breaker.registrarFallo();
    expect(breaker.puedeIntentarAhora()).toBe(false);
  });

  test('debe resetear en CERRADO después de éxito', () => {
    const breaker = new CircuitBreaker(3, 5000);
    breaker.registrarFallo();
    breaker.registrarExito();
    expect(breaker.obtenerEstado()).toBe('CERRADO');
  });
});

describe('RetryManager', () => {
  test('debe calcular backoff exponencial correcto', () => {
    const manager = new RetryManager();
    expect(manager.calcularDelay(0)).toBe(1000);
    expect(manager.calcularDelay(1)).toBe(2000);
    expect(manager.calcularDelay(2)).toBe(4000);
    expect(manager.calcularDelay(3)).toBe(8000);
    expect(manager.calcularDelay(4)).toBe(16000);
    expect(manager.calcularDelay(5)).toBe(60000);
  });

  test('debe resetearse después de éxito', () => {
    const manager = new RetryManager();
    manager.registrarIntento();
    manager.registrarIntento();
    manager.registrarExito();
    expect(manager.obtenerIntentos()).toBe(0);
  });
});
