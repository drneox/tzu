# Controles ASVS (Application Security Verification Standard) - Versión 4.0.3

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

    # V5: Validation, Sanitization and Encoding
    "V5.1.1": {
        "title": "Input Validation",
        "description": "Verificar que la aplicación tiene defensas contra ataques de inyección HTTP parameter pollution.",
        "category": "Input Validation"
    },
    "V5.1.2": {
        "title": "Input Validation Architecture",
        "description": "Verificar que los frameworks protejan contra ataques de asignación masiva de parámetros, o que la aplicación tenga contramedidas para proteger contra asignaciones de parámetros inseguros.",
        "category": "Input Validation"
    },
    "V5.1.3": {
        "title": "Input Validation Implementation",
        "description": "Verificar que todos los inputs (campos de formularios HTML, peticiones REST, parámetros URL, cabeceras HTTP, cookies, archivos batch, feeds RSS, etc.) sean validados usando validación positiva (lista blanca).",
        "category": "Input Validation"
    },
    "V5.1.4": {
        "title": "Structured Data Validation",
        "description": "Verificar que los datos estructurados están fuertemente tipados y validados contra un esquema definido incluyendo caracteres permitidos, longitud y patrón.",
        "category": "Input Validation"
    },
    "V5.1.5": {
        "title": "URL Validation",
        "description": "Verificar que la validación de redirección y reenvío de URL solo permita destinos que aparezcan en una lista blanca, o muestre una advertencia al redireccionar a contenido potencialmente hostil.",
        "category": "Input Validation"
    },
    "V5.2.1": {
        "title": "Sanitization",
        "description": "Verificar que toda entrada HTML no confiable de editores WYSIWYG o similares sea apropiadamente saneada con una librería de saneamiento HTML o característica de framework.",
        "category": "Input Validation"
    },
    "V5.2.2": {
        "title": "Unstructured Data",
        "description": "Verificar que los datos no estructurados sean saneados para hacer cumplir medidas de seguridad tales como caracteres permitidos y longitud.",
        "category": "Input Validation"
    },
    "V5.3.1": {
        "title": "Output Encoding",
        "description": "Verificar que la codificación de salida sea relevante para el intérprete y contexto requerido.",
        "category": "Input Validation"
    },
    "V5.3.2": {
        "title": "Output Encoding Implementation",
        "description": "Verificar que toda salida esté codificada para el contexto de destino o intérprete para evitar ataques de inyección.",
        "category": "Input Validation"
    },
    "V5.3.3": {
        "title": "Context-aware Output Encoding",
        "description": "Verificar que la codificación consciente del contexto, preferentemente automatizada - o en el peor caso, manual - sea aplicada para proteger contra la Cross Site Scripting reflejada, almacenada, y basada en DOM.",
        "category": "Input Validation"
    },

    # V6: Stored Cryptography
    "V6.1.1": {
        "title": "Data Classification",
        "description": "Verificar que los datos regulados están almacenados cifrados mientras están en reposo, tales como datos de tarjetas de crédito, PII o otros datos sensibles.",
        "category": "Stored Cryptography"
    },
    "V6.1.2": {
        "title": "Cryptographic Controls",
        "description": "Verificar que todos los datos criptográficos están almacenados en un formato que garantice la integridad de los datos o autenticación adicional.",
        "category": "Stored Cryptography"
    },
    "V6.2.1": {
        "title": "Algorithms",
        "description": "Verificar que todos los módulos criptográficos fallen de manera segura, y que los errores sean manejados de una manera que no permita ataques de padding oracle.",
        "category": "Stored Cryptography"
    },
    "V6.2.2": {
        "title": "Algorithm Strength",
        "description": "Verificar que se usen generadores de números aleatorios criptográficamente seguros donde se requiera entropía criptográfica, y que no fallen de forma predecible o con baja entropía.",
        "category": "Stored Cryptography"
    },
    "V6.3.1": {
        "title": "Random Values",
        "description": "Verificar que todas las operaciones criptográficas usen valores aleatorios, nonces, vectores de inicialización, y otros criptográficos de un solo uso apropiados para el algoritmo criptográfico y su uso.",
        "category": "Stored Cryptography"
    },
    "V6.4.1": {
        "title": "Secret Management",
        "description": "Verificar que un vault de secretos sea usado para almacenar de forma segura secretos criptográficos usados por la aplicación y que este vault no esté codificado en la aplicación o sus archivos de configuración.",
        "category": "Stored Cryptography"
    },

    # V7: Error Handling and Logging
    "V7.1.1": {
        "title": "Log Content Requirements",
        "description": "Verificar que la aplicación no registra credenciales o detalles de pago. Los tokens de sesión solo deben ser almacenados en logs de una forma irreversible, hasheada.",
        "category": "Error Handling and Logging"
    },
    "V7.1.2": {
        "title": "Log Processing",
        "description": "Verificar que la aplicación no registra otros datos sensibles según se define bajo las leyes de privacidad locales o políticas de seguridad relevantes.",
        "category": "Error Handling and Logging"
    },
    "V7.1.3": {
        "title": "Log Security",
        "description": "Verificar que la aplicación registra eventos relevantes para la seguridad de acuerdo a las funciones de la aplicación.",
        "category": "Error Handling and Logging"
    },
    "V7.2.1": {
        "title": "Error Messages",
        "description": "Verificar que toda la información de autenticación exitosa y fallida sea registrada de forma suficiente para identificar cuentas sospechosas o maliciosas, y se mantenga por un tiempo suficiente para permitir análisis forense retrasado.",
        "category": "Error Handling and Logging"
    },
    "V7.2.2": {
        "title": "Error Handling",
        "description": "Verificar que todos los errores se registren de forma apropiada para identificar actividad maliciosa o sospechosa.",
        "category": "Error Handling and Logging"
    },
    "V7.3.1": {
        "title": "Log Protection",
        "description": "Verificar que todos los componentes de logging implementen logging apropiado para detectar y alertar sobre actividades anómalas o maliciosas.",
        "category": "Error Handling and Logging"
    },
    "V7.4.1": {
        "title": "Time Sources",
        "description": "Verificar que una fuente de tiempo genérica y registrada es usada para permitir la correlación de logs entre múltiples sistemas.",
        "category": "Error Handling and Logging"
    },

    # V8: Data Protection
    "V8.1.1": {
        "title": "Data Protection",
        "description": "Verificar que la aplicación protege datos sensibles de ser almacenados en cachés del lado del cliente, como el navegador o el sistema operativo.",
        "category": "Data Protection"
    },
    "V8.1.2": {
        "title": "Data Storage",
        "description": "Verificar que todos los datos sensibles almacenados en cliente están cifrados y que cualquier descifrado no autorizado no revele los datos originales o tokens usables.",
        "category": "Data Protection"
    },
    "V8.1.3": {
        "title": "Personal Data",
        "description": "Verificar que los datos sensibles se conservan por el menor tiempo que sea requerido y que los datos antiguos o desactualizados se eliminan de una manera oportuna, automatizada, o al menos que se facilite la eliminación.",
        "category": "Data Protection"
    },
    "V8.2.1": {
        "title": "Client-side Data Protection",
        "description": "Verificar que la aplicación establece cabeceras HTTP apropiadas para evitar que información sensible sea almacenada en caché en navegadores modernos.",
        "category": "Data Protection"
    },
    "V8.2.2": {
        "title": "Server-side Data Protection",
        "description": "Verificar que los datos almacenados en almacenamiento del lado del servidor (por ejemplo, bases de datos, almacenes de datos, almacenes de archivos) no contengan información sensible innecesaria.",
        "category": "Data Protection"
    },
    "V8.3.1": {
        "title": "Sensitive Data Exposure",
        "description": "Verificar que los datos sensibles son enviados al servidor en el cuerpo del mensaje HTTP o cabeceras, y que los parámetros de cadena de consulta de cualquier verbo HTTP no contengan datos sensibles.",
        "category": "Data Protection"
    },

    # V9: Communication
    "V9.1.1": {
        "title": "Communications Security Architecture",
        "description": "Verificar que la aplicación use TLS para todas las conexiones del cliente, y que no caiga a comunicaciones inseguras o no cifradas.",
        "category": "Communication"
    },
    "V9.1.2": {
        "title": "TLS Configuration",
        "description": "Verificar usando pruebas en línea o herramientas TLS actualizadas que solo se habiliten suites de cifrado fuertes, con el algoritmo de cifrado más fuerte establecido como preferido.",
        "category": "Communication"
    },
    "V9.1.3": {
        "title": "Certificate Validation",
        "description": "Verificar que solo las versiones más recientes recomendadas del protocolo TLS estén habilitadas, tales como TLS 1.2 y TLS 1.3.",
        "category": "Communication"
    },
    "V9.2.1": {
        "title": "Server Communications Security",
        "description": "Verificar que las conexiones del servidor usen certificados TLS confiables. Donde se usen certificados autofirmados o emitidos internamente, el servidor debe ser configurado para confiar solo en CAs internas específicas y certificados autofirmados específicos.",
        "category": "Communication"
    },

    # V10: Malicious Code
    "V10.1.1": {
        "title": "Code Integrity",
        "description": "Verificar que un analizador de código fuente está en uso que puede detectar código potencialmente malicioso.",
        "category": "Malicious Code"
    },
    "V10.2.1": {
        "title": "Application Source Code Integrity",
        "description": "Verificar que el código fuente de la aplicación y bibliotecas de terceros no contengan capacidades no autorizadas, puertas traseras maliciosas, huevos de pascua, bombas de tiempo, malware, o otro código no autorizado.",
        "category": "Malicious Code"
    },
    "V10.3.1": {
        "title": "Deployed Application Integrity",
        "description": "Verificar que la aplicación tiene protección contra ataques de subdominios si la aplicación se basa en entradas DNS o subdominios DNS, tales como subdominios caducados, almacenamiento en la nube DNS o CDN caducados, etc.",
        "category": "Malicious Code"
    },

    # V11: Business Logic
    "V11.1.1": {
        "title": "Business Logic Security",
        "description": "Verificar que la aplicación solo procesará flujos de lógica de negocio para el mismo usuario en orden secuencial y sin omitir pasos.",
        "category": "Business Logic"
    },
    "V11.1.2": {
        "title": "Business Logic Data Validation",
        "description": "Verificar que la aplicación solo procesará flujos de lógica de negocio con datos realistas en tiempo realista y no procesará demasiadas transacciones concurrentes del mismo usuario.",
        "category": "Business Logic"
    },
    "V11.1.3": {
        "title": "Application Limits",
        "description": "Verificar que la aplicación tenga límites apropiados para acciones específicas o transacciones que sean correctamente aplicados por usuario.",
        "category": "Business Logic"
    },
    "V11.1.4": {
        "title": "Anti-automation",
        "description": "Verificar que la aplicación tenga controles anti-automatización para proteger contra llamadas excesivas de funciones de negocio y recursos.",
        "category": "Business Logic"
    },

    # V12: Files and Resources
    "V12.1.1": {
        "title": "File Upload",
        "description": "Verificar que la aplicación no acepta archivos grandes que podrían llenar el almacenamiento o causar una denegación de servicio.",
        "category": "Files and Resources"
    },
    "V12.1.2": {
        "title": "File Storage",
        "description": "Verificar que los archivos obtenidos de fuentes no confiables sean validados para ser del tipo esperado basándose en el contenido del archivo, no solo en su nombre, tipo MIME, o extensión de archivo.",
        "category": "Files and Resources"
    },
    "V12.1.3": {
        "title": "File Execution",
        "description": "Verificar que los nombres de archivo enviados se validen o ignoren para prevenir la revelación, creación, actualización o eliminación de archivos locales.",
        "category": "Files and Resources"
    },
    "V12.2.1": {
        "title": "File Integrity",
        "description": "Verificar que los archivos obtenidos de fuentes no confiables se almacenen fuera del directorio web, con permisos limitados.",
        "category": "Files and Resources"
    },

    # V13: API and Web Service
    "V13.1.1": {
        "title": "Generic Web Service Security",
        "description": "Verificar que todos los componentes de la aplicación usen las mismas codificaciones y parsers para evitar ataques de parseo que exploten diferentes comportamientos de parseo de URI o archivo que podrían ser usados en ataques SSRF y RFI.",
        "category": "API and Web Service"
    },
    "V13.1.2": {
        "title": "API Authentication",
        "description": "Verificar que la API solo acepta datos cifrados para funciones muy sensibles, y que estos datos estén firmados criptográficamente para proporcionar garantías adicionales de integridad sobre los datos recibidos.",
        "category": "API and Web Service"
    },
    "V13.2.1": {
        "title": "RESTful Web Service",
        "description": "Verificar que los métodos HTTP habilitados sean un conjunto necesario de métodos, tales como GET, POST, y PUT, y que los métodos no utilizados estén deshabilitados.",
        "category": "API and Web Service"
    },
    "V13.2.2": {
        "title": "REST Endpoint Security",
        "description": "Verificar que la validación del esquema RESTful esté en su lugar y verificada antes de aceptar inputs.",
        "category": "API and Web Service"
    },
    "V13.3.1": {
        "title": "SOAP Web Service",
        "description": "Verificar que la validación del esquema XSD tenga lugar para asegurar un documento XML apropiadamente formado, seguido por la validación de cada campo de input antes de que cualquier procesamiento de datos tenga lugar.",
        "category": "API and Web Service"
    },
    "V13.4.1": {
        "title": "GraphQL",
        "description": "Verificar que las consultas GraphQL o librerías de mapeo de datos tienen limitación de consulta o análisis de profundidad para prevenir ataques de Denegación de Servicio (DoS) GraphQL.",
        "category": "API and Web Service"
    },

    # V14: Configuration
    "V14.1.1": {
        "title": "Build and Deploy",
        "description": "Verificar que los componentes de la aplicación están segregados de manera segura de otros en el mismo servidor a través de cuentas, patrones de llave/directorio, y sandboxing.",
        "category": "Configuration"
    },
    "V14.1.2": {
        "title": "Configuration Architecture",
        "description": "Verificar que los framework, librerías, ejecutables, y archivos de configuración estén asegurados contra escritura no autorizada.",
        "category": "Configuration"
    },
    "V14.1.3": {
        "title": "Communication Security",
        "description": "Verificar que cada aplicación tenga un sandbox, containerizado o aislado de otras aplicaciones en el mismo sistema.",
        "category": "Configuration"
    },
    "V14.2.1": {
        "title": "Dependency",
        "description": "Verificar que todos los componentes estén actualizados, preferiblemente usando un dependency checker durante el tiempo de construcción o compilación.",
        "category": "Configuration"
    },
    "V14.2.2": {
        "title": "Third Party Components",
        "description": "Verificar que todas las características, documentación, samples, configuraciones y dependencias innecesarias hayan sido eliminadas.",
        "category": "Configuration"
    },
    "V14.2.3": {
        "title": "Application Assets",
        "description": "Verificar que si los assets de la aplicación, tales como librerías JavaScript, CSS o fuentes web, están alojados externamente en una red de distribución de contenido (CDN) o proveedor externo, que la integridad de subrecursos (SRI) sea usada para validar la integridad del asset.",
        "category": "Configuration"
    },
    "V14.3.1": {
        "title": "Unintended Security Disclosure",
        "description": "Verificar que los mensajes de error de seguridad o divulgación de información sensible no se filtren incluyendo que la aplicación no filtree números de versión, información del entorno, nombres de usuario, o información de rutas sensibles.",
        "category": "Configuration"
    },
    "V14.3.2": {
        "title": "HTTP Security Headers",
        "description": "Verificar que las cabeceras de seguridad HTTP que ofrecen un nivel apropiado de protección están presentes, tales como Strict-Transport-Security, Content-Security-Policy, X-Content-Type-Options, y X-Frame-Options.",
        "category": "Configuration"
    },
    "V14.4.1": {
        "title": "HTTP Request Header Validation",
        "description": "Verificar que cada respuesta HTTP contenga una cabecera Content-Type. También especificar un charset seguro (por ejemplo, UTF-8, ISO-8859-1) si los tipos de contenido son text/*, /+xml y application/xml. El contenido debe coincidir con la cabecera Content-Type proporcionada.",
        "category": "Configuration"
    },
    "V14.4.2": {
        "title": "HTTP Response Header Validation",
        "description": "Verificar que todas las respuestas de la API contengan una cabecera Content-Disposition: attachment; filename=\"api.json\" (o otro nombre de archivo apropiado para el tipo de contenido).",
        "category": "Configuration"
    },
    "V14.5.1": {
        "title": "HTTP Strict Transport Security",
        "description": "Verificar que la aplicación no use tecnologías del lado del cliente no compatibles, inseguras o depreciadas tales como plugins NSAPI, Flash, Shockwave, ActiveX, Silverlight, NACL, o applets Java del lado del cliente.",
        "category": "Configuration"
    }
}

# Lista de tags para compatibilidad hacia atrás
ASVS_TAGS = list(ASVS_CONTROLS.keys())
