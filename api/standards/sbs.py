# Controles SBS (Superintendencia de Banca, Seguros y AFP - Perú)
# Circular SBS G-504-2021: Gestión de Riesgos de Ciberseguridad
# Estructura basada en las funciones del NIST CSF + requisitos de gobernanza de la circular.

VERSION = "Circular G-504-2021"

SBS_CONTROLS = {

    # ─── GOBERNANZA ──────────────────────────────────────────────────────────────
    "SBS-504-1": {
        "title": "Marco de Gestión de Riesgos de Ciberseguridad",
        "description": "Las empresas deben implementar un Marco de Gestión de Riesgos de Ciberseguridad (MGRC) aprobado por el directorio, que defina políticas, roles, responsabilidades y objetivos de ciberseguridad alineados con el apetito de riesgo institucional.",
        "category": "Gobernanza"
    },
    "SBS-504-2": {
        "title": "Oficial de Ciberseguridad (CISO)",
        "description": "Las empresas deben designar un Oficial de Ciberseguridad (CISO) con independencia organizacional, nivel jerárquico adecuado y acceso directo al directorio y a la alta gerencia para reportar el estado de ciberseguridad.",
        "category": "Gobernanza"
    },
    "SBS-504-3": {
        "title": "Comité de Ciberseguridad",
        "description": "Las empresas deben constituir un comité de ciberseguridad con participación de la alta dirección y representantes de las áreas de TI, riesgo operacional y cumplimiento, responsable de aprobar la estrategia y supervisar la gestión de riesgos de ciberseguridad.",
        "category": "Gobernanza"
    },
    "SBS-504-4": {
        "title": "Reporte periódico al directorio",
        "description": "La alta gerencia debe reportar periódicamente al directorio el estado de los riesgos de ciberseguridad, los incidentes materiales y la efectividad de los controles implementados.",
        "category": "Gobernanza"
    },

    # ─── IDENTIFICAR ─────────────────────────────────────────────────────────────
    "SBS-504-5": {
        "title": "Inventario de Activos de Información",
        "description": "Las empresas deben mantener un inventario actualizado de activos de información (hardware, software, datos, servicios), con clasificación por criticidad y sensibilidad, que sirva como base para la evaluación de riesgos de ciberseguridad.",
        "category": "Identificar"
    },
    "SBS-504-6": {
        "title": "Evaluación de Riesgos de Ciberseguridad",
        "description": "Las empresas deben realizar evaluaciones periódicas de riesgos de ciberseguridad que incluyan identificación de amenazas, vulnerabilidades e impactos sobre activos críticos, documentando los resultados y los planes de tratamiento.",
        "category": "Identificar"
    },
    "SBS-504-7": {
        "title": "Gestión de Vulnerabilidades",
        "description": "Las empresas deben implementar un proceso continuo de identificación, clasificación, priorización y remediación de vulnerabilidades técnicas en sistemas, aplicaciones e infraestructura, con plazos de corrección definidos según criticidad.",
        "category": "Identificar"
    },

    # ─── PROTEGER ────────────────────────────────────────────────────────────────
    "SBS-504-8": {
        "title": "Control de Acceso y Gestión de Identidades",
        "description": "Las empresas deben implementar controles de acceso basados en el principio de mínimo privilegio, con autenticación multifactor para accesos privilegiados y remotos, y procesos formales de revisión periódica y revocación de accesos.",
        "category": "Proteger"
    },
    "SBS-504-9": {
        "title": "Seguridad en el Desarrollo de Software",
        "description": "Las empresas deben incorporar controles de seguridad en el ciclo de vida del desarrollo de software (SDLC), incluyendo revisiones de código, pruebas de seguridad y validación de entornos previos a producción.",
        "category": "Proteger"
    },
    "SBS-504-10": {
        "title": "Segmentación de Redes y Protección Perimetral",
        "description": "Las empresas deben implementar segmentación de redes para aislar sistemas críticos, con controles perimetrales (firewalls, IPS/IDS, WAF) que restrinjan el tráfico no autorizado y protejan los servicios expuestos.",
        "category": "Proteger"
    },
    "SBS-504-11": {
        "title": "Cifrado de Datos",
        "description": "Las empresas deben cifrar los datos sensibles en tránsito y en reposo utilizando algoritmos y longitudes de clave robustos, con gestión segura del ciclo de vida de las claves criptográficas.",
        "category": "Proteger"
    },
    "SBS-504-12": {
        "title": "Concientización y Capacitación en Ciberseguridad",
        "description": "Las empresas deben implementar programas periódicos de concientización y capacitación en ciberseguridad para todo el personal, incluyendo simulaciones de phishing y entrenamiento especializado para roles con acceso privilegiado.",
        "category": "Proteger"
    },

    # ─── DETECTAR ────────────────────────────────────────────────────────────────
    "SBS-504-13": {
        "title": "Monitoreo Continuo y SIEM",
        "description": "Las empresas deben implementar capacidades de monitoreo continuo de eventos de seguridad mediante herramientas SIEM u equivalentes, con correlación de logs de sistemas críticos, detección de anomalías y alertas en tiempo real.",
        "category": "Detectar"
    },
    "SBS-504-14": {
        "title": "Centro de Operaciones de Seguridad (SOC)",
        "description": "Las empresas con operaciones de importancia sistémica deben contar con capacidades de SOC (propio o tercerizado) para la detección, análisis y escalamiento de incidentes de ciberseguridad de forma continua.",
        "category": "Detectar"
    },
    "SBS-504-15": {
        "title": "Inteligencia de Amenazas (Threat Intelligence)",
        "description": "Las empresas deben participar en mecanismos de intercambio de información sobre amenazas cibernéticas y consumir fuentes de inteligencia relevantes para el sector financiero, incluyendo las alertas emitidas por la SBS.",
        "category": "Detectar"
    },

    # ─── RESPONDER ───────────────────────────────────────────────────────────────
    "SBS-504-16": {
        "title": "Plan de Respuesta a Incidentes de Ciberseguridad",
        "description": "Las empresas deben contar con un plan documentado y probado de respuesta a incidentes de ciberseguridad que defina roles, procedimientos de contención, erradicación, comunicación interna y coordinación con autoridades.",
        "category": "Responder"
    },
    "SBS-504-17": {
        "title": "Notificación de Incidentes a la SBS",
        "description": "Las empresas deben notificar a la SBS los incidentes de ciberseguridad que afecten la continuidad operativa, la confidencialidad de datos de clientes o la integridad de sistemas críticos, dentro de los plazos establecidos en la circular.",
        "category": "Responder"
    },

    # ─── RECUPERAR ───────────────────────────────────────────────────────────────
    "SBS-504-18": {
        "title": "Plan de Continuidad ante Ciberincidentes",
        "description": "Las empresas deben integrar escenarios de ciberataques en sus planes de continuidad operativa y recuperación de desastres, con RTO/RPO definidos para sistemas críticos y pruebas periódicas de los procedimientos de restauración.",
        "category": "Recuperar"
    },
    "SBS-504-19": {
        "title": "Pruebas de Resiliencia Cibernética",
        "description": "Las empresas deben realizar pruebas periódicas de resiliencia cibernética incluyendo ejercicios de simulación (tabletop), pruebas de penetración y red team, para evaluar la efectividad de los controles y la capacidad de recuperación.",
        "category": "Recuperar"
    },

    # ─── GESTIÓN DE TERCEROS ─────────────────────────────────────────────────────
    "SBS-504-20": {
        "title": "Gestión de Riesgo de Ciberseguridad en Terceros",
        "description": "Las empresas deben evaluar los riesgos de ciberseguridad de proveedores y terceros con acceso a sus sistemas o datos, establecer requisitos contractuales de seguridad, y monitorear el cumplimiento durante toda la relación contractual.",
        "category": "Gestión de Terceros"
    },
}

# Lista de tags para compatibilidad hacia atrás
SBS_TAGS = list(SBS_CONTROLS.keys())


