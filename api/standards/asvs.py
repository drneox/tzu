# ASVS Controls (Application Security Verification Standard) - Version 4.0.3

ASVS_CONTROLS = {
    # V1: Architecture, Design and Threat Modeling
    "V1.1.1": {
        "title": "Secure SDLC",
        "description": "Verificar el uso de un ciclo de vida de desarrollo de software seguro que aborde la seguridad en todas las etapas del desarrollo.",
        "category": "Architecture"
    },
    "V1.1.2": {
        "title": "Threat Modeling",
        "description": "Verificar el uso de modelado de amenazas para cada cambio de diseño o planificación de sprint para identificar amenazas, planificar contramedidas, facilitar respuestas apropiadas a riesgos, y guiar las pruebas de seguridad.",
        "category": "Architecture"
    },
    "V1.2.1": {
        "title": "Security Architecture",
        "description": "Verificar el uso de un patrón arquitectónico de seguridad estándar que aborde la separación de componentes o niveles.",
        "category": "Architecture"
    },
    "V1.4.1": {
        "title": "Trusted Communications",
        "description": "Verificar que las comunicaciones entre componentes de aplicación, incluidas las APIs, middleware y capas de datos, se autentiquen. Los componentes deben tener los mínimos privilegios necesarios.",
        "category": "Architecture"
    },
    "V1.14.1": {
        "title": "Build Pipeline Security",
        "description": "Verificar que el pipeline de construcción advierte sobre componentes desactualizados o inseguros y toma las acciones apropiadas.",
        "category": "Architecture"
    },

    # V2: Authentication
    "V2.1.1": {
        "title": "Password Security",
        "description": "Verificar que las credenciales por defecto del sistema, o del usuario, se hayan cambiado antes de implementar el sistema en producción.",
        "category": "Authentication"
    },
    "V2.1.2": {
        "title": "Password Strength",
        "description": "Verificar que los controles de resistencia de credenciales, tales como la longitud de contraseñas, complejidad o patrones de passphrases, sean aplicados de acuerdo con NIST 800-63B sección 5.1.1 para secretos memorizados o otros estándares de contraseñas modernas.",
        "category": "Authentication"
    },
    "V2.1.3": {
        "title": "Password Recovery",
        "description": "Verificar que la funcionalidad de recuperación de credenciales no revele la contraseña actual y que la nueva contraseña no sea enviada en texto claro al usuario.",
        "category": "Authentication"
    },
    "V2.2.1": {
        "title": "Anti-automation",
        "description": "Verificar que los controles de anti-automatización estén en vigor para prevenir el rompimiento por fuerza bruta de credenciales comunes.",
        "category": "Authentication"
    },
    "V2.2.2": {
        "title": "Account Lockout",
        "description": "Verificar que existan controles para evitar ataques de enumeración de cuentas, por ejemplo mediante el uso de mensajes genéricos en respuestas a intentos de autenticación no válidos.",
        "category": "Authentication"
    },
    "V2.2.3": {
        "title": "Rate Limiting",
        "description": "Verificar que se implementen controles de limitación de velocidad de credenciales, como bloqueo de cuenta después de un número de intentos fallidos consecutivos o retrasos crecientes.",
        "category": "Authentication"
    },
    "V2.3.1": {
        "title": "Lifecycle Authenticators",
        "description": "Verificar que las contraseñas generadas por el sistema tengan al menos 112 bits de entropía (por ejemplo, 19 caracteres alfanuméricos totalmente aleatorios), o al menos 64 bits de entropía (por ejemplo, 8 caracteres alfanuméricos totalmente aleatorios) si también tienen una fecha de caducidad inferior a 24 horas.",
        "category": "Authentication"
    },
    "V2.4.1": {
        "title": "Generic Authentication",
        "description": "Verificar que las contraseñas, identificadores de sesión y otros elementos de autenticación se transmitan mediante canales cifrados únicamente.",
        "category": "Authentication"
    },
    "V2.5.1": {
        "title": "Credential Recovery",
        "description": "Verificar que se implementen mecanismos para permitir a los usuarios recuperar su acceso de forma segura sin revelar la contraseña actual.",
        "category": "Authentication"
    },

    # V3: Session Management
    "V3.1.1": {
        "title": "Session Security",
        "description": "Verificar que la aplicación nunca revele tokens de sesión en parámetros URL.",
        "category": "Session Management"
    },
    "V3.2.1": {
        "title": "Session Generation",
        "description": "Verificar que la aplicación genere un nuevo token de sesión al autenticarse el usuario.",
        "category": "Session Management"
    },
    "V3.2.2": {
        "title": "Session Invalidation",
        "description": "Verificar que los tokens de sesión posean al menos 64 bits de entropía.",
        "category": "Session Management"
    },
    "V3.2.3": {
        "title": "Session Storage",
        "description": "Verificar que la aplicación solo almacene tokens de sesión en el navegador usando métodos seguros como cookies seguras con httpOnly y secure, o almacenamiento de sesión HTML 5.",
        "category": "Session Management"
    },
    "V3.3.1": {
        "title": "Session Logout",
        "description": "Verificar que cerrar sesión y caducar invaliden efectivamente el token de sesión, de tal forma que el botón de retroceso o una parte que confíe en la sesión no reanude una sesión autenticada, incluso en páginas públicas.",
        "category": "Session Management"
    },
    "V3.3.2": {
        "title": "Session Timeout",
        "description": "Si los autenticadores permiten a los usuarios permanecer autenticados, verificar que la re-autenticación ocurra periódicamente tanto cuando está activa como inactiva.",
        "category": "Session Management"
    },

    # V4: Access Control
    "V4.1.1": {
        "title": "Access Control Design",
        "description": "Verificar que la aplicación imponga las reglas de control de acceso en una capa de servicio confiable.",
        "category": "Access Control"
    },
    "V4.1.2": {
        "title": "Attribute-based Access Control",
        "description": "Verificar que todos los controles de acceso de usuario y datos sean aplicados del lado del servidor y no del lado del cliente.",
        "category": "Access Control"
    },
    "V4.1.3": {
        "title": "Principle of Least Privilege",
        "description": "Verificar que la aplicación tiene un mecanismo de control de acceso por defecto que deniega por defecto.",
        "category": "Access Control"
    },
    "V4.1.4": {
        "title": "Attribute Access Control",
        "description": "Verificar que el control de acceso falle de forma segura incluyendo cuando ocurre una excepción.",
        "category": "Access Control"
    },
    "V4.1.5": {
        "title": "Access Control Enforcement",
        "description": "Verificar que el control de acceso se aplique en una capa de servicio de confianza, especialmente para aplicaciones del lado del cliente y para el lado del servidor.",
        "category": "Access Control"
    },
    "V4.2.1": {
        "title": "Operation Level Access Control",
        "description": "Verificar que los datos sensibles y APIs estén protegidos contra ataques de referencia directa a objetos inseguros (IDOR) dirigidos a la creación, lectura, actualización y eliminación de registros.",
        "category": "Access Control"
    },
    "V4.2.2": {
        "title": "Directory Traversal",
        "description": "Verificar que la aplicación o framework imponga un fuerte mecanismo de control de acceso anti-CSRF para proteger la funcionalidad autenticada, y efectivo control de acceso anti-automatización o anti-CSRF para proteger la funcionalidad no autenticada.",
        "category": "Access Control"
    },
    "V4.3.1": {
        "title": "Administrative Interfaces",
        "description": "Verificar que las interfaces administrativas usen autenticación multifactor apropiada para prevenir el uso no autorizado.",
        "category": "Access Control"
    },
    "V4.3.2": {
        "title": "Administrative Functions",
        "description": "Verificar que la navegación de directorios está deshabilitada a menos que sea deliberadamente deseada. Adicionalmente, las aplicaciones no deberían permitir el descubrimiento o divulgación de metadatos de archivos o directorios.",
        "category": "Access Control"
    },

    # ... Continue with V5 to V14 (truncated for brevity in this snippet)
}

# Tag list for backward compatibility
ASVS_TAGS = list(ASVS_CONTROLS.keys())
