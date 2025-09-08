"""
ISO 27001:2013 Information Security Management Controls
======================================================
This module contains ISO 27001:2013 Annex A security controls organized by control categories.
ISO 27001 provides requirements for establishing, implementing, maintaining and continually 
improving an information security management system within the context of the organization.

Control Categories (Annex A):
- A.5: Information Security Policies
- A.6: Organization of Information Security  
- A.7: Human Resource Security
- A.8: Asset Management
- A.9: Access Control
- A.10: Cryptography
- A.11: Physical and Environmental Security
- A.12: Operations Security
- A.13: Communications Security
- A.14: System Acquisition, Development and Maintenance
- A.15: Supplier Relationships
- A.16: Information Security Incident Management
- A.17: Information Security Aspects of Business Continuity Management
- A.18: Compliance
"""

# Controles ISO 27001
ISO27001_CONTROLS = {
    # A.5: Information Security Policies
    "A.5.1.1": {
        "title": "Policies for Information Security",
        "description": "Un conjunto de políticas para la seguridad de la información debe ser definido, aprobado por la dirección, publicado y comunicado a empleados y partes externas relevantes.",
        "category": "Information Security Policies"
    },
    "A.5.1.2": {
        "title": "Review of the Policies for Information Security",
        "description": "Las políticas para la seguridad de la información deben ser revisadas a intervalos planificados o si ocurren cambios significativos para asegurar su conveniencia, adecuación y efectividad continuas.",
        "category": "Information Security Policies"
    },

    # A.6: Organization of Information Security
    "A.6.1.1": {
        "title": "Information Security Roles and Responsibilities",
        "description": "Todas las responsabilidades de la seguridad de la información deben ser definidas y asignadas.",
        "category": "Organization of Information Security"
    },
    "A.6.1.2": {
        "title": "Segregation of Duties",
        "description": "Los deberes y áreas de responsabilidad conflictivos deben ser segregados para reducir las oportunidades de modificación no autorizada o no intencional o uso indebido de los activos de la organización.",
        "category": "Organization of Information Security"
    },
    "A.6.1.3": {
        "title": "Contact with Authorities",
        "description": "Se deben mantener contactos apropiados con las autoridades relevantes.",
        "category": "Organization of Information Security"
    },
    "A.6.1.4": {
        "title": "Contact with Special Interest Groups",
        "description": "Se deben mantener contactos apropiados con grupos de interés especial u otros foros de especialistas en seguridad y asociaciones profesionales.",
        "category": "Organization of Information Security"
    },
    "A.6.1.5": {
        "title": "Information Security in Project Management",
        "description": "La seguridad de la información debe ser abordada en la gestión de proyectos, independientemente del tipo de proyecto.",
        "category": "Organization of Information Security"
    },
    "A.6.2.1": {
        "title": "Mobile Device Policy",
        "description": "Se debe adoptar una política y medidas de seguridad de soporte para gestionar los riesgos introducidos por el uso de dispositivos móviles.",
        "category": "Organization of Information Security"
    },
    "A.6.2.2": {
        "title": "Teleworking",
        "description": "Se debe implementar una política y medidas de seguridad de soporte para proteger la información accedida, procesada o almacenada en lugares de teletrabajo.",
        "category": "Organization of Information Security"
    },

    # A.7: Human Resource Security
    "A.7.1.1": {
        "title": "Screening",
        "description": "Las verificaciones de antecedentes de todos los candidatos para el empleo deben ser realizadas de acuerdo con las leyes, regulaciones y ética relevantes, y deben ser proporcionales a los requisitos del negocio.",
        "category": "Human Resource Security"
    },
    "A.7.1.2": {
        "title": "Terms and Conditions of Employment",
        "description": "Los acuerdos contractuales con empleados y contratistas deben declarar sus responsabilidades y las de la organización para la seguridad de la información.",
        "category": "Human Resource Security"
    },
    "A.7.2.1": {
        "title": "Management Responsibilities",
        "description": "La dirección debe requerir que todos los empleados y contratistas apliquen la seguridad de la información de acuerdo con las políticas y procedimientos establecidos de la organización.",
        "category": "Human Resource Security"
    },
    "A.7.2.2": {
        "title": "Information Security Awareness, Education and Training",
        "description": "Todos los empleados de la organización y, donde sea relevante, contratistas deben recibir entrenamiento apropiado de concienciación en seguridad de la información.",
        "category": "Human Resource Security"
    },
    "A.7.2.3": {
        "title": "Disciplinary Process",
        "description": "Debe haber un proceso disciplinario formal y comunicado para tomar acción contra empleados que hayan cometido una brecha de seguridad de la información.",
        "category": "Human Resource Security"
    },
    "A.7.3.1": {
        "title": "Termination or Change of Employment Responsibilities",
        "description": "Las responsabilidades y actividades de seguridad de la información que permanecen válidas después de la terminación o cambio de empleo deben ser definidas, comunicadas al empleado o contratista y aplicadas.",
        "category": "Human Resource Security"
    },

    # A.8: Asset Management
    "A.8.1.1": {
        "title": "Inventory of Assets",
        "description": "Los activos asociados con información e instalaciones de procesamiento de información deben ser identificados y un inventario de estos activos debe ser elaborado y mantenido.",
        "category": "Asset Management"
    },
    "A.8.1.2": {
        "title": "Ownership of Assets",
        "description": "Los activos mantenidos en el inventario deben tener un propietario.",
        "category": "Asset Management"
    },
    "A.8.1.3": {
        "title": "Acceptable Use of Assets",
        "description": "Las reglas para el uso aceptable de información y de activos asociados con información e instalaciones de procesamiento de información deben ser identificadas, documentadas e implementadas.",
        "category": "Asset Management"
    },
    "A.8.1.4": {
        "title": "Return of Assets",
        "description": "Todos los empleados y usuarios de terceras partes deben retornar todos los activos de la organización en su posesión al terminar su empleo, contrato o acuerdo.",
        "category": "Asset Management"
    },
    "A.8.2.1": {
        "title": "Classification of Information",
        "description": "La información debe ser clasificada en términos de requisitos legales, valor, criticidad y sensibilidad para divulgación o modificación no autorizada.",
        "category": "Asset Management"
    },
    "A.8.2.2": {
        "title": "Labelling of Information",
        "description": "Un conjunto apropiado de procedimientos para etiquetado de información debe ser desarrollado e implementado de acuerdo con el esquema de clasificación de información adoptado por la organización.",
        "category": "Asset Management"
    },
    "A.8.2.3": {
        "title": "Handling of Assets",
        "description": "Los procedimientos para el manejo de activos deben ser desarrollados e implementados de acuerdo con el esquema de clasificación de información adoptado por la organización.",
        "category": "Asset Management"
    },
    "A.8.3.1": {
        "title": "Management of Removable Media",
        "description": "Los procedimientos deben ser implementados para la gestión de medios removibles de acuerdo con el esquema de clasificación adoptado por la organización.",
        "category": "Asset Management"
    },
    "A.8.3.2": {
        "title": "Disposal of Media",
        "description": "Los medios deben ser dispuestos de forma segura cuando ya no se requieran, usando procedimientos formales.",
        "category": "Asset Management"
    },
    "A.8.3.3": {
        "title": "Physical Media Transfer",
        "description": "Los medios que contienen información deben ser protegidos contra acceso no autorizado, uso indebido o corrupción durante el transporte.",
        "category": "Asset Management"
    },

    # A.9: Access Control
    "A.9.1.1": {
        "title": "Access Control Policy",
        "description": "Una política de control de acceso debe ser establecida, documentada y revisada basándose en los requisitos del negocio y de seguridad de la información.",
        "category": "Access Control"
    },
    "A.9.1.2": {
        "title": "Access to Networks and Network Services",
        "description": "Los usuarios deben ser provistos únicamente con acceso a la red y servicios de red que hayan sido específicamente autorizados a usar.",
        "category": "Access Control"
    },
    "A.9.2.1": {
        "title": "User Registration and De-registration",
        "description": "Un proceso formal de registro y de-registro de usuarios debe ser implementado para habilitar la asignación de derechos de acceso.",
        "category": "Access Control"
    },
    "A.9.2.2": {
        "title": "User Access Provisioning",
        "description": "Un proceso formal de aprovisionamiento de acceso de usuarios debe ser implementado para asignar o revocar derechos de acceso para todos los tipos de usuarios a todos los sistemas y servicios.",
        "category": "Access Control"
    },
    "A.9.2.3": {
        "title": "Management of Privileged Access Rights",
        "description": "La asignación y uso de derechos de acceso privilegiados debe ser restringido y controlado.",
        "category": "Access Control"
    },
    "A.9.2.4": {
        "title": "Management of Secret Authentication Information of Users",
        "description": "La asignación de información de autenticación secreta debe ser controlada a través de un proceso de gestión formal.",
        "category": "Access Control"
    },
    "A.9.2.5": {
        "title": "Review of User Access Rights",
        "description": "Los propietarios de activos deben revisar los derechos de acceso de los usuarios a intervalos regulares.",
        "category": "Access Control"
    },
    "A.9.2.6": {
        "title": "Removal or Adjustment of Access Rights",
        "description": "Los derechos de acceso de todos los empleados y usuarios de terceras partes a información y facilidades de procesamiento de información deben ser removidos al terminar su empleo, contrato o acuerdo.",
        "category": "Access Control"
    },
    "A.9.3.1": {
        "title": "Use of Secret Authentication Information",
        "description": "Se debe requerir a los usuarios que sigan las prácticas de la organización en el uso de información de autenticación secreta.",
        "category": "Access Control"
    },
    "A.9.4.1": {
        "title": "Information Access Restriction",
        "description": "El acceso a información y funciones del sistema de aplicación debe ser restringido de acuerdo con la política de control de acceso.",
        "category": "Access Control"
    },
    "A.9.4.2": {
        "title": "Secure Log-on Procedures",
        "description": "Donde se requiera por la política de control de acceso, el acceso a sistemas y aplicaciones debe ser controlado por un procedimiento de log-on seguro.",
        "category": "Access Control"
    },
    "A.9.4.3": {
        "title": "Password Management System",
        "description": "Los sistemas de gestión de contraseñas deben ser interactivos y deben asegurar contraseñas de calidad.",
        "category": "Access Control"
    },
    "A.9.4.4": {
        "title": "Use of Privileged Utility Programs",
        "description": "El uso de programas utilitarios que podrían ser capaces de sobrescribir controles del sistema y de aplicación debe ser restringido y estrechamente controlado.",
        "category": "Access Control"
    },
    "A.9.4.5": {
        "title": "Access Control to Program Source Code",
        "description": "El acceso al código fuente del programa debe ser restringido.",
        "category": "Access Control"
    },

    # A.10: Cryptography
    "A.10.1.1": {
        "title": "Policy on the Use of Cryptographic Controls",
        "description": "Una política sobre el uso de controles criptográficos para protección de información debe ser desarrollada e implementada.",
        "category": "Cryptography"
    },
    "A.10.1.2": {
        "title": "Key Management",
        "description": "Una política sobre el uso, protección y tiempo de vida de llaves criptográficas debe ser desarrollada e implementada a través de su ciclo de vida completo.",
        "category": "Cryptography"
    },

    # A.11: Physical and Environmental Security
    "A.11.1.1": {
        "title": "Physical Security Perimeter",
        "description": "Los perímetros de seguridad física deben ser definidos y usados para proteger áreas que contienen información sensible o crítica e instalaciones de procesamiento de información.",
        "category": "Physical and Environmental Security"
    },
    "A.11.1.2": {
        "title": "Physical Entry Controls",
        "description": "Las áreas seguras deben ser protegidas por controles de entrada apropiados para asegurar que solo personal autorizado tenga acceso permitido.",
        "category": "Physical and Environmental Security"
    },
    "A.11.1.3": {
        "title": "Protection Against Environmental Threats",
        "description": "Se debe diseñar e implementar protección física contra daño por fuego, inundación, terremoto, explosión, disturbios civiles y otras formas de desastres naturales o hechos por el hombre.",
        "category": "Physical and Environmental Security"
    },
    "A.11.1.4": {
        "title": "Working in Secure Areas",
        "description": "Los procedimientos para trabajar en áreas seguras deben ser diseñados e implementados.",
        "category": "Physical and Environmental Security"
    },
    "A.11.1.5": {
        "title": "Access Points",
        "description": "Los puntos de acceso como áreas de entrega y carga y otros puntos donde personas no autorizadas podrían entrar a las instalaciones deben ser controlados y, si es posible, aislados de las facilidades de procesamiento de información.",
        "category": "Physical and Environmental Security"
    },
    "A.11.1.6": {
        "title": "Publicly Accessible Areas",
        "description": "Se debe controlar el acceso a las áreas de entrega, carga y otras áreas donde personas no autorizadas pueden entrar a las instalaciones y, si es posible, aislarlas de las facilidades de procesamiento de información.",
        "category": "Physical and Environmental Security"
    },
    "A.11.2.1": {
        "title": "Equipment Siting and Protection",
        "description": "El equipo debe ser ubicado y protegido para reducir los riesgos de amenazas ambientales y peligros, y oportunidades para acceso no autorizado.",
        "category": "Physical and Environmental Security"
    },
    "A.11.2.2": {
        "title": "Supporting Utilities",
        "description": "El equipo debe ser protegido de fallas de energía y otras interrupciones causadas por fallas en las utilidades de soporte.",
        "category": "Physical and Environmental Security"
    },
    "A.11.2.3": {
        "title": "Cabling Security",
        "description": "El cableado de energía y telecomunicaciones que transporta datos o soporta servicios de información debe ser protegido de interceptación, interferencia o daño.",
        "category": "Physical and Environmental Security"
    },
    "A.11.2.4": {
        "title": "Equipment Maintenance",
        "description": "El equipo debe ser mantenido correctamente para asegurar su disponibilidad e integridad continuas.",
        "category": "Physical and Environmental Security"
    },
    "A.11.2.5": {
        "title": "Removal of Assets",
        "description": "El equipo, información o software no debe ser sacado de las instalaciones sin autorización previa.",
        "category": "Physical and Environmental Security"
    },
    "A.11.2.6": {
        "title": "Security of Equipment and Assets Off-premises",
        "description": "Se debe aplicar seguridad a activos fuera de las instalaciones teniendo en cuenta los diferentes riesgos de trabajar fuera de las instalaciones de la organización.",
        "category": "Physical and Environmental Security"
    },
    "A.11.2.7": {
        "title": "Secure Disposal or Reuse of Equipment",
        "description": "Todos los elementos de equipo que contienen medios de almacenamiento deben ser verificados para asegurar que cualquier dato sensible e software licenciado haya sido removido o sobrescrito de forma segura antes de la disposición o reutilización.",
        "category": "Physical and Environmental Security"
    },
    "A.11.2.8": {
        "title": "Unattended User Equipment",
        "description": "Los usuarios deben asegurar que el equipo desatendido tenga protección apropiada.",
        "category": "Physical and Environmental Security"
    },
    "A.11.2.9": {
        "title": "Clear Desk and Clear Screen Policy",
        "description": "Una política de escritorio limpio para papeles y medios de almacenamiento removibles y una política de pantalla limpia para las facilidades de procesamiento de información deben ser adoptadas.",
        "category": "Physical and Environmental Security"
    },

    # Formatos alternativos con prefijo ISO27001 (para compatibilidad)
    "ISO27001-A.5.1.1": {
        "title": "Policies for Information Security",
        "description": "Un conjunto de políticas para la seguridad de la información debe ser definido, aprobado por la dirección, publicado y comunicado a empleados y partes externas relevantes.",
        "category": "Information Security Policies"
    },
    "ISO27001-A.9.1.1": {
        "title": "Access Control Policy",
        "description": "Una política de control de acceso debe ser establecida, documentada y revisada basándose en los requisitos del negocio y de seguridad de la información.",
        "category": "Access Control"
    },
    "ISO27001-A.11.1.1": {
        "title": "Physical Security Perimeter",
        "description": "Los perímetros de seguridad física deben ser definidos y usados para proteger áreas que contienen información sensible o crítica e instalaciones de procesamiento de información.",
        "category": "Physical and Environmental Security"
    }
}
