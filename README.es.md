# TZU - Threat Zero Utility 🛡️

[![Version](https://img.shields.io/github/v/release/drneox/tzu?include_prereleases)](https://github.com/drneox/tzu/releases)
[![Estado de Compilación](https://img.shields.io/github/actions/workflow/status/drneox/tzu/python-app-test.yml)](https://github.com/drneox/tzu/actions/workflows/python-app-test.yml)
[![Licencia: MIT](https://img.shields.io/badge/Licencia-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.68+-green.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18+-blue.svg)](https://reactjs.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)
[![OWASP](https://img.shields.io/badge/OWASP-Compliant-red.svg)](https://owasp.org/)

<img src="tzu.png" alt="TZU Logo" width="200">

Una aplicación web impulsada por IA diseñada para ayudar a identificar amenazas y gestionar planes de acción, siguiendo estándares de ciberseguridad de la industria incluyendo OWASP Risk Rating, STRIDE, OWASP ASVS/MASVS.

## 🤔 ¿Por qué TZU?

**TZU** está inspirado en **Sun Tzu**, el estratega militar y filósofo chino, autor de *"El Arte de la Guerra"*, una de las obras más influyentes sobre estrategia y táctica.

> "Los guerreros victoriosos ganan primero y luego van a la guerra; los guerreros derrotados van a la guerra primero y luego buscan ganar." — Sun Tzu

Así como Sun Tzu enfatiza conocer al enemigo — y conocerte a ti mismo — para lograr la victoria, TZU empodera a los equipos de ciberseguridad para:

- 🧭 **Conócete a Ti Mismo:** Inventariar activos y datos; identificar joyas de la corona; mapear límites de confianza y flujos de datos.
- 🎯 **Perfilar Adversarios:** Capturar habilidad, motivo, oportunidad/exposición y tamaño.  
  _OWASP RR → completa **Factores del Agente de Amenaza**, impulsando **Probabilidad**._
- 🔍 **Conoce Tus Amenazas:** Derivar amenazas de **diagramas de arquitectura/DFD** y **casos de uso**, respaldado por análisis asistido por IA.
- 🛡️ **Conoce Tus Defensas:** Evaluar tu postura actual y **vulnerabilidades**; mapear **controles** a **OWASP ASVS/MASVS**.
- ⚔️ **Planificación Estratégica:** Definir **planes de mitigación priorizados por nivel de riesgo**; aplicar un **modelo de riesgo consistente (Probabilidad × Impacto)** para **calcular y rastrear** **riesgo inherente, actual y residual**.

En ciberseguridad—como en la guerra antigua—**la preparación y la inteligencia marcan la diferencia**. TZU entrega las herramientas y trazabilidad para mantenerse adelante de las amenazas y proteger sus activos digitales aplicando la sabiduría estratégica de Sun Tzu a los desafíos de seguridad modernos.

## 🚀 Inicio Rápido

### 🐳 Despliegue con Docker (Recomendado)

La forma más rápida de ejecutar TZU es con nuestro script de configuración automatizada:

```bash
# 1. Clonar el repositorio
git clone https://github.com/drneox/tzu
cd tzu

# 2. Configurar entorno (opcional pero recomendado)
# Editar archivo .env para agregar tu clave API y zona horaria
cp .env.example .env
# Luego editar .env y configurar:
# - Configurar la clave del proveedor de IA:
#   * AI_API_KEY=tu_clave_api_aqui
# - TZ=tu_zona_horaria (ej. America/New_York, Europe/London, America/Lima)

# 3. Ejecutar el script de configuración automatizada
./start.sh
```

El script automáticamente:
- 🔧 Construye e inicia todos los servicios (nginx, backend, postgresql)
- 🔐 Genera credenciales de administrador seguras
- 📋 Muestra información de acceso

**⚙️ Notas de Configuración:**
- **Funciones de IA**: Elige UN proveedor de IA - ya sea OpenAI O clave API de Anthropic (no ambas)
- **Zona Horaria**: Configura tu zona horaria local para marcas de tiempo precisas en reportes y logs

**Acceder a la aplicación:**
- **App Web**: http://localhost:3434
- **Documentación API**: http://localhost:3434/api/docs
- **Credenciales**: Se muestran después de completar la configuración

## ✨ Características

### Funcionalidad Principal
- **Identificación de Amenazas con IA**: Capacidades inteligentes de detección y análisis de amenazas
- **Gestión de Planes de Acción**: Gestión integral de planes de acción de seguridad y estrategias de remediación
- **OWASP Risk Rating**: Implementación completa para categorización de niveles de riesgo con factores de agentes de amenaza, factores de vulnerabilidad y cálculos de impacto
- **Cumplimiento de Estándares de la Industria**: Construido siguiendo los estándares de ciberseguridad OWASP Risk Rating, STRIDE, OWASP ASVS y MASVS
- **Modelado de Amenazas**: Subida interactiva de diagramas e identificación de amenazas
- **Evaluación de Riesgos**: Cálculo automatizado de puntuaciones de probabilidad e impacto para determinar niveles de riesgo
- **Reportes PDF**: Generación de reportes profesionales con análisis detallado y recomendaciones de seguridad
- **Soporte Multi-idioma**: Localización en inglés y español

## 🔐 Autenticación y Seguridad

### Credenciales Predeterminadas
Después del despliegue, genera credenciales seguras:

```bash
docker exec docker-backend-1 python show_credentials.py
```

Esto mostrará:
- **Usuario**: `admin`
- **Contraseña**: Contraseña segura auto-generada

### Estándares de Ciberseguridad Soportados

- **OWASP Risk Rating**: Metodología completa para categorización y evaluación de niveles de riesgo
- **STRIDE**: Categorización de amenazas de Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service y Elevation of Privilege
- **OWASP ASVS**: Estándar de Verificación de Seguridad de Aplicaciones para cobertura integral de requisitos de seguridad
- **OWASP MASVS**: Estándar de Verificación de Seguridad de Aplicaciones Móviles para evaluación de seguridad móvil y generación de recomendaciones de seguridad

## 🤝 Contribuir

1. Hacer fork del repositorio
2. Crear tu rama de característica (`git checkout -b feature/caracteristica-increible`)
3. Confirmar tus cambios (`git commit -m 'feat: agregar característica increíble'`)
4. Empujar a la rama (`git push origin feature/caracteristica-increible`)
5. Abrir un Pull Request

### Pautas de Desarrollo

- Seguir mensajes de commit convencionales
- Mantener cobertura de pruebas por encima del 80%
- Usar ESLint para formato de código
- Escribir documentación integral

## 📝 Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## 👥 Autores

- **Carlos Ganoza (drneox)** - *Trabajo inicial* - [@drneox](https://github.com/drneox)

## 🙏 Reconocimientos

- [Fundación OWASP](https://owasp.org/) por los frameworks y metodologías de ciberseguridad
- [Capítulo OWASP Lima](https://owasp.org/www-chapter-lima/) por el apoyo y orientación de la comunidad de ciberseguridad
- Colaboradores y la comunidad de código abierto

## 📧 Soporte

Si tienes preguntas o necesitas soporte, por favor:

1. Revisa la [documentación](README.md)
2. Busca en [issues](https://github.com/drneox/tzu/issues) existentes
3. Crea un nuevo issue si es necesario

---

*[English Version](README.md) | Versión en Español*
