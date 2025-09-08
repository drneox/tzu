# MASVS Controls (Mobile Application Security Verification Standard) - Versión 1.4.2

MASVS_CONTROLS = {
    # V1: Architecture, Design and Threat Modeling
    "ARCH-1": {
        "title": "Arquitectura Documentada",
        "description": "La arquitectura de la aplicación está documentada y considera modelos de amenazas, activos, actores y límites de confianza.",
        "category": "Architecture"
    },
    "ARCH-2": {
        "title": "Principio de Privilegios Mínimos",
        "description": "La aplicación sigue el principio de mínimo privilegio y separación de responsabilidades en todos sus componentes.",
        "category": "Architecture"
    },
    "ARCH-3": {
        "title": "Protección de Secretos",
        "description": "Los secretos (claves, tokens) no se exponen en el código y se gestionan en almacenes seguros.",
        "category": "Architecture"
    },
    "ARCH-4": {
        "title": "Uso de APIs de Plataforma Seguras",
        "description": "Se utilizan únicamente APIs seguras y soportadas por la plataforma, siguiendo las mejores prácticas.",
        "category": "Architecture"
    },

    # V2: Authentication and Session Management
    "AUTH-1": {
        "title": "Autenticación Segura",
        "description": "La aplicación implementa un mecanismo de autenticación robusto para acceder a servicios remotos.",
        "category": "Authentication"
    },
    "AUTH-2": {
        "title": "Autenticación Multifactor",
        "description": "Las operaciones sensibles requieren MFA seguro (ej. notificación push o app de autenticación, no SMS).",
        "category": "Authentication"
    },
    "AUTH-3": {
        "title": "Gestión Segura de Sesiones",
        "description": "Las sesiones usan tokens de corta vida, rotación y revocación; se valida audiencia, emisor y expiración.",
        "category": "Authentication"
    },
    "AUTH-4": {
        "title": "Política de Contraseñas",
        "description": "Se aplican requisitos de longitud, complejidad, historial y bloqueo progresivo ante intentos fallidos.",
        "category": "Authentication"
    },
    "AUTH-5": {
        "title": "Protección contra Enumeración",
        "description": "Los mensajes de error no permiten inferir la validez de usuarios o estados de cuenta.",
        "category": "Authentication"
    },
    "AUTH-6": {
        "title": "Cierre de Sesión Seguro",
        "description": "El cierre de sesión invalida y elimina credenciales/tokens de manera segura en el cliente y servidor.",
        "category": "Authentication"
    },
    "AUTH-7": {
        "title": "Revocación de Sesiones",
        "description": "La aplicación permite revocar tokens de forma remota e inmediata ante compromiso de credenciales.",
        "category": "Authentication"
    },
    "AUTH-8": {
        "title": "Inactividad y Expiración",
        "description": "Las sesiones expiran tras un periodo razonable de inactividad, evitando uso indebido.",
        "category": "Authentication"
    },

    # V3: Data Storage and Privacy
    "STORAGE-1": {
        "title": "Uso de Almacenamiento Seguro",
        "description": "Los datos sensibles se almacenan usando funciones seguras del sistema (ej. Keychain, Keystore).",
        "category": "Data Storage"
    },
    "STORAGE-2": {
        "title": "No Filtración de Datos",
        "description": "Los datos sensibles no se filtran a logs, vistas recientes, copias de seguridad o caches.",
        "category": "Data Storage"
    },
    "STORAGE-3": {
        "title": "Protección de Datos en Reposo",
        "description": "Los datos sensibles en reposo se cifran con claves protegidas por hardware cuando sea posible.",
        "category": "Data Storage"
    },
    "STORAGE-4": {
        "title": "Borrado Seguro",
        "description": "Los datos sensibles se eliminan de forma segura al cerrar sesión o desinstalar la app.",
        "category": "Data Storage"
    },

    # V4: Cryptography
    "CRYPTO-1": {
        "title": "Gestión de Claves",
        "description": "La app no depende de claves simétricas codificadas en el binario; se gestionan en enclaves seguros.",
        "category": "Cryptography"
    },
    "CRYPTO-2": {
        "title": "Algoritmos Seguros",
        "description": "Se emplean algoritmos/métodos fuertes (AES-GCM, PBKDF2/Argon2) y longitudes de clave recomendadas.",
        "category": "Cryptography"
    },
    "CRYPTO-3": {
        "title": "Gestión de Entropía",
        "description": "La generación de claves/OTP utiliza PRNG seguros y fuentes de entropía adecuadas.",
        "category": "Cryptography"
    },
    "CRYPTO-4": {
        "title": "Ciclo de Vida de Claves",
        "description": "Claves con rotación, expiración y revocación definidas; no se reutilizan para múltiples fines.",
        "category": "Cryptography"
    },

    # V5: Network Communication
    "NETWORK-1": {
        "title": "Cifrado de Comunicaciones",
        "description": "Los datos se cifran en tránsito usando TLS, consistente en toda la app.",
        "category": "Network Communication"
    },
    "NETWORK-2": {
        "title": "Validación de Certificados",
        "description": "Se valida la cadena de certificados y hostname; no se permite `accept all certs`.",
        "category": "Network Communication"
    },
    "NETWORK-3": {
        "title": "Pinning de Certificados/Claves",
        "description": "Se aplica certificate/key pinning en servicios críticos, con plan de rotación.",
        "category": "Network Communication"
    },
    "NETWORK-4": {
        "title": "Políticas de Transporte",
        "description": "Se aplica TLS 1.2+ (ideal 1.3), cipher suites seguras y ATS/HSTS.",
        "category": "Network Communication"
    },

    # V6: Platform Interaction
    "PLATFORM-1": {
        "title": "Uso Seguro de APIs",
        "description": "La aplicación utiliza únicamente APIs seguras y soportadas por la plataforma.",
        "category": "Platform Interaction"
    },
    "PLATFORM-2": {
        "title": "Permisos Mínimos",
        "description": "Los permisos de la app son mínimos y justificados según la funcionalidad.",
        "category": "Platform Interaction"
    },
    "PLATFORM-3": {
        "title": "Protección de Intents/Deep Links",
        "description": "Se protegen intents y deep links contra hijacking, validando origen y destino.",
        "category": "Platform Interaction"
    },
    "PLATFORM-4": {
        "title": "Gestión de Ciclo de Vida",
        "description": "La app maneja correctamente background/foreground y borra datos temporales al bloquear pantalla.",
        "category": "Platform Interaction"
    },

    # V7: Code Quality and Build Settings
    "CODE-1": {
        "title": "Code Signing",
        "description": "La app está firmada con un certificado válido, cuya clave privada está protegida.",
        "category": "Code Quality"
    },
    "CODE-2": {
        "title": "Configuración Segura de Compilación",
        "description": "En builds de producción se eliminan logs de depuración, símbolos y se aplica ofuscación si corresponde.",
        "category": "Code Quality"
    },
    "CODE-3": {
        "title": "Revisión de Dependencias",
        "description": "Se revisan dependencias de terceros y se mantienen actualizadas.",
        "category": "Code Quality"
    },

    # V8: Resilience
    "RESILIENCE-1": {
        "title": "Anti-Debugging",
        "description": "La app detecta y responde a intentos de depuración mediante APIs o técnicas alternativas.",
        "category": "Resilience"
    },
    "RESILIENCE-2": {
        "title": "Detección Root/Jailbreak",
        "description": "La app detecta dispositivos comprometidos y aplica políticas de mitigación.",
        "category": "Resilience"
    },
    "RESILIENCE-3": {
        "title": "Protección contra Ingeniería Inversa",
        "description": "Se aplican ofuscación, detección de hooking y comprobación de integridad del binario.",
        "category": "Resilience"
    },
    "RESILIENCE-4": {
        "title": "Defensas en Tiempo de Ejecución",
        "description": "Se monitorean e impiden inyecciones de código, hooking y tampering en runtime.",
        "category": "Resilience"
    }
}

# Lista de tags para compatibilidad hacia atrás
MASVS_TAGS = sorted(MASVS_CONTROLS.keys())
