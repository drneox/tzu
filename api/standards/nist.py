# Controles NIST Cybersecurity Framework

NIST_CONTROLS = {
    # IDENTIFY (ID)
    "ID.AM-1": {
        "title": "Physical devices and systems within the organization are inventoried",
        "description": "Maintain an accurate, complete, and up-to-date inventory of physical devices and systems within the organization.",
        "category": "Asset Management"
    },
    "ID.AM-2": {
        "title": "Software platforms and applications within the organization are inventoried",
        "description": "Maintain an accurate, complete, and up-to-date inventory of software platforms and applications within the organization.",
        "category": "Asset Management"
    },
    "ID.AM-3": {
        "title": "Organizational communication and data flows are mapped",
        "description": "Document and map organizational communication and data flows to understand how information moves through the organization.",
        "category": "Asset Management"
    },
    "ID.AM-4": {
        "title": "External information systems are catalogued",
        "description": "Maintain an inventory of external information systems that the organization depends upon.",
        "category": "Asset Management"
    },
    "ID.AM-5": {
        "title": "Resources (e.g., hardware, devices, data, time, software, and services) are prioritized based on their classification, criticality, and business value",
        "description": "Prioritize organizational resources based on their business importance and criticality.",
        "category": "Asset Management"
    },
    "ID.AM-6": {
        "title": "Cybersecurity roles and responsibilities for the entire workforce and third-party stakeholders are established",
        "description": "Define and document cybersecurity roles and responsibilities for all personnel and third parties.",
        "category": "Governance"
    },
    "ID.BE-1": {
        "title": "The organization's role in the supply chain is identified and communicated",
        "description": "Understand and document the organization's role within its supply chain ecosystem.",
        "category": "Business Environment"
    },
    "ID.BE-2": {
        "title": "The organization's place in critical infrastructure and its industry sector is identified and communicated",
        "description": "Identify the organization's role within critical infrastructure and industry sectors.",
        "category": "Business Environment"
    },
    "ID.BE-3": {
        "title": "Priorities for organizational mission, objectives, and activities are established and communicated",
        "description": "Establish and communicate organizational priorities, mission, and objectives.",
        "category": "Business Environment"
    },
    "ID.BE-4": {
        "title": "Dependencies and critical functions for delivery of critical services are established",
        "description": "Identify dependencies and critical functions required for service delivery.",
        "category": "Business Environment"
    },
    "ID.BE-5": {
        "title": "Resilience requirements to support delivery of critical services are established for all operating states",
        "description": "Define resilience requirements to maintain critical services across all operating conditions.",
        "category": "Business Environment"
    },
    "ID.GV-1": {
        "title": "Organizational cybersecurity policy is established and communicated",
        "description": "Establish, document, and communicate organizational cybersecurity policy.",
        "category": "Governance"
    },
    "ID.GV-2": {
        "title": "Cybersecurity roles and responsibilities are coordinated and aligned with internal roles and external partners",
        "description": "Coordinate cybersecurity roles with internal stakeholders and external partners.",
        "category": "Governance"
    },
    "ID.GV-3": {
        "title": "Legal and regulatory requirements regarding cybersecurity are understood and managed",
        "description": "Understand and manage legal and regulatory cybersecurity requirements.",
        "category": "Governance"
    },
    "ID.GV-4": {
        "title": "Governance and risk management processes address cybersecurity risks",
        "description": "Integrate cybersecurity risks into governance and risk management processes.",
        "category": "Governance"
    },
    "ID.RA-1": {
        "title": "Asset vulnerabilities are identified and documented",
        "description": "Identify and document vulnerabilities in organizational assets.",
        "category": "Risk Assessment"
    },
    "ID.RA-2": {
        "title": "Cyber threat intelligence is received from information sharing forums and sources",
        "description": "Receive and utilize cyber threat intelligence from various sources.",
        "category": "Risk Assessment"
    },
    "ID.RA-3": {
        "title": "Threats, both internal and external, are identified and documented",
        "description": "Identify and document internal and external threats to the organization.",
        "category": "Risk Assessment"
    },
    "ID.RA-4": {
        "title": "Potential business impacts and likelihoods are identified",
        "description": "Identify potential business impacts and their likelihoods.",
        "category": "Risk Assessment"
    },
    "ID.RA-5": {
        "title": "Threats, vulnerabilities, likelihoods, and impacts are used to determine risk",
        "description": "Use threat, vulnerability, likelihood, and impact information to determine risk.",
        "category": "Risk Assessment"
    },
    "ID.RA-6": {
        "title": "Risk responses are identified and prioritized",
        "description": "Identify and prioritize appropriate risk response strategies.",
        "category": "Risk Assessment"
    },
    "ID.RM-1": {
        "title": "Risk management processes are established, managed, and agreed to by organizational stakeholders",
        "description": "Establish and manage risk management processes with stakeholder agreement.",
        "category": "Risk Management Strategy"
    },
    "ID.RM-2": {
        "title": "Organizational risk tolerance is determined and clearly expressed",
        "description": "Determine and clearly express organizational risk tolerance levels.",
        "category": "Risk Management Strategy"
    },
    "ID.RM-3": {
        "title": "The organization's determination of risk tolerance is informed by its role in critical infrastructure and sector specific risk analysis",
        "description": "Inform risk tolerance decisions with critical infrastructure and sector-specific analysis.",
        "category": "Risk Management Strategy"
    },
    "ID.SC-1": {
        "title": "Cyber supply chain risk management processes are identified, established, assessed, managed, and agreed to by organizational stakeholders",
        "description": "Establish and manage cyber supply chain risk management processes.",
        "category": "Supply Chain Risk Management"
    },
    "ID.SC-2": {
        "title": "Suppliers and third party partners of information systems, components, and services are identified, prioritized, and assessed using a cyber supply chain risk assessment process",
        "description": "Identify, prioritize, and assess suppliers and third-party partners for cyber risks.",
        "category": "Supply Chain Risk Management"
    },
    "ID.SC-3": {
        "title": "Contracts with suppliers and third-party partners are used to implement appropriate measures designed to meet the objectives of an organization's cybersecurity program",
        "description": "Use contracts to implement cybersecurity measures with suppliers and partners.",
        "category": "Supply Chain Risk Management"
    },
    "ID.SC-4": {
        "title": "Suppliers and third-party partners are routinely assessed using audits, test results, or other forms of evaluations to confirm they are meeting their contractual obligations",
        "description": "Routinely assess suppliers and partners to confirm contractual compliance.",
        "category": "Supply Chain Risk Management"
    },
    "ID.SC-5": {
        "title": "Response and recovery planning and testing are conducted with suppliers and third-party providers",
        "description": "Conduct response and recovery planning with suppliers and third-party providers.",
        "category": "Supply Chain Risk Management"
    },

    # PROTECT (PR)
    "PR.AC-1": {
        "title": "Identities and credentials are issued, managed, verified, revoked, and audited for authorized devices, users and processes",
        "description": "Manage identities and credentials throughout their lifecycle for all authorized entities.",
        "category": "Identity Management and Access Control"
    },
    "PR.AC-2": {
        "title": "Physical access to assets is managed and protected",
        "description": "Manage and protect physical access to organizational assets.",
        "category": "Identity Management and Access Control"
    },
    "PR.AC-3": {
        "title": "Remote access is managed",
        "description": "Manage remote access to organizational systems and networks.",
        "category": "Identity Management and Access Control"
    },
    "PR.AC-4": {
        "title": "Access permissions and authorizations are managed, incorporating the principles of least privilege and separation of duties",
        "description": "Manage access permissions using least privilege and separation of duties principles.",
        "category": "Identity Management and Access Control"
    },
    "PR.AC-5": {
        "title": "Network integrity is protected (e.g., network segregation, network segmentation)",
        "description": "Protect network integrity through segregation and segmentation.",
        "category": "Identity Management and Access Control"
    },
    "PR.AC-6": {
        "title": "Identities are proofed and bound to credentials and asserted in interactions",
        "description": "Proof identities and bind them to credentials for secure interactions.",
        "category": "Identity Management and Access Control"
    },
    "PR.AC-7": {
        "title": "Users, devices, and other assets are authenticated (e.g., single-factor, multi-factor) commensurate with the risk of the transaction",
        "description": "Authenticate users, devices, and assets based on transaction risk.",
        "category": "Identity Management and Access Control"
    },
    "PR.AT-1": {
        "title": "All users are informed and trained",
        "description": "Inform and train all users on cybersecurity awareness and responsibilities.",
        "category": "Awareness and Training"
    },
    "PR.AT-2": {
        "title": "Privileged users understand their roles and responsibilities",
        "description": "Ensure privileged users understand their specific roles and responsibilities.",
        "category": "Awareness and Training"
    },
    "PR.AT-3": {
        "title": "Third-party stakeholders understand their roles and responsibilities",
        "description": "Ensure third-party stakeholders understand their cybersecurity roles and responsibilities.",
        "category": "Awareness and Training"
    },
    "PR.AT-4": {
        "title": "Senior executives understand their roles and responsibilities",
        "description": "Ensure senior executives understand their cybersecurity roles and responsibilities.",
        "category": "Awareness and Training"
    },
    "PR.AT-5": {
        "title": "Physical and cybersecurity personnel understand their roles and responsibilities",
        "description": "Ensure physical and cybersecurity personnel understand their specific roles.",
        "category": "Awareness and Training"
    },
    "PR.DS-1": {
        "title": "Data-at-rest is protected",
        "description": "Protect data while it is stored (data-at-rest).",
        "category": "Data Security"
    },
    "PR.DS-2": {
        "title": "Data-in-transit is protected",
        "description": "Protect data while it is being transmitted (data-in-transit).",
        "category": "Data Security"
    },
    "PR.DS-3": {
        "title": "Assets are formally managed throughout removal, transfers, and disposition",
        "description": "Formally manage assets through removal, transfer, and disposition processes.",
        "category": "Data Security"
    },
    "PR.DS-4": {
        "title": "Adequate capacity to ensure availability is maintained",
        "description": "Maintain adequate capacity to ensure system and data availability.",
        "category": "Data Security"
    },
    "PR.DS-5": {
        "title": "Protections against data leaks are implemented",
        "description": "Implement protections to prevent unauthorized data disclosure.",
        "category": "Data Security"
    },
    "PR.DS-6": {
        "title": "Integrity checking mechanisms are used to verify software, firmware, and information integrity",
        "description": "Use integrity checking mechanisms to verify software, firmware, and information.",
        "category": "Data Security"
    },
    "PR.DS-7": {
        "title": "The development and testing environment(s) are separate from the production environment",
        "description": "Separate development and testing environments from production environments.",
        "category": "Data Security"
    },
    "PR.DS-8": {
        "title": "Integrity checking mechanisms are used to verify hardware integrity",
        "description": "Use integrity checking mechanisms to verify hardware integrity.",
        "category": "Data Security"
    },
    "PR.IP-1": {
        "title": "A baseline configuration of information technology/industrial control systems is created and maintained incorporating security principles",
        "description": "Create and maintain baseline configurations incorporating security principles.",
        "category": "Information Protection Processes and Procedures"
    },
    "PR.IP-2": {
        "title": "A System Development Life Cycle to manage systems is implemented",
        "description": "Implement a System Development Life Cycle for managing systems.",
        "category": "Information Protection Processes and Procedures"
    },
    "PR.IP-3": {
        "title": "Configuration change control processes are in place",
        "description": "Implement configuration change control processes.",
        "category": "Information Protection Processes and Procedures"
    },
    "PR.IP-4": {
        "title": "Backups of information are conducted, maintained, and tested",
        "description": "Conduct, maintain, and test information backups.",
        "category": "Information Protection Processes and Procedures"
    },
    "PR.IP-5": {
        "title": "Policy and regulations regarding the physical operating environment for organizational assets are met",
        "description": "Meet policy and regulatory requirements for physical operating environments.",
        "category": "Information Protection Processes and Procedures"
    },
    "PR.IP-6": {
        "title": "Data is destroyed according to policy",
        "description": "Destroy data according to organizational policy and procedures.",
        "category": "Information Protection Processes and Procedures"
    },
    "PR.IP-7": {
        "title": "Protection processes are improved",
        "description": "Continuously improve protection processes and procedures.",
        "category": "Information Protection Processes and Procedures"
    },
    "PR.IP-8": {
        "title": "Effectiveness of protection technologies is shared",
        "description": "Share information about the effectiveness of protection technologies.",
        "category": "Information Protection Processes and Procedures"
    },
    "PR.IP-9": {
        "title": "Response plans and recovery plans are in place and managed",
        "description": "Develop, maintain, and manage response and recovery plans.",
        "category": "Information Protection Processes and Procedures"
    },
    "PR.IP-10": {
        "title": "Response and recovery plans are tested",
        "description": "Test response and recovery plans regularly.",
        "category": "Information Protection Processes and Procedures"
    },
    "PR.IP-11": {
        "title": "Cybersecurity is included in human resources practices",
        "description": "Include cybersecurity considerations in human resources practices.",
        "category": "Information Protection Processes and Procedures"
    },
    "PR.IP-12": {
        "title": "A vulnerability management plan is developed and implemented",
        "description": "Develop and implement a comprehensive vulnerability management plan.",
        "category": "Information Protection Processes and Procedures"
    },
    "PR.MA-1": {
        "title": "Maintenance and repair of organizational assets are performed and logged, with approved and controlled tools",
        "description": "Perform and log maintenance and repair activities with approved tools.",
        "category": "Maintenance"
    },
    "PR.MA-2": {
        "title": "Remote maintenance of organizational assets is approved, logged, and performed in a manner that prevents unauthorized access",
        "description": "Approve, log, and securely perform remote maintenance activities.",
        "category": "Maintenance"
    },
    "PR.PT-1": {
        "title": "Audit/log records are determined, documented, implemented, and reviewed in accordance with policy",
        "description": "Determine, document, implement, and review audit/log records according to policy.",
        "category": "Protective Technology"
    },
    "PR.PT-2": {
        "title": "Removable media is protected and its use restricted according to policy",
        "description": "Protect removable media and restrict its use according to organizational policy.",
        "category": "Protective Technology"
    },
    "PR.PT-3": {
        "title": "The principle of least functionality is incorporated by configuring systems to provide only essential capabilities",
        "description": "Configure systems to provide only essential capabilities (least functionality).",
        "category": "Protective Technology"
    },
    "PR.PT-4": {
        "title": "Communications and control networks are protected",
        "description": "Protect communications and control networks from unauthorized access.",
        "category": "Protective Technology"
    },
    "PR.PT-5": {
        "title": "Mechanisms (e.g., failsafe, load balancing, hot swap) are implemented to achieve resilience requirements in normal and adverse situations",
        "description": "Implement mechanisms to achieve resilience in normal and adverse situations.",
        "category": "Protective Technology"
    },

    # DETECT (DE)
    "DE.AE-1": {
        "title": "A baseline of network operations and expected data flows for users and systems is established and managed",
        "description": "Establish and manage baseline network operations and expected data flows.",
        "category": "Anomalies and Events"
    },
    "DE.AE-2": {
        "title": "Detected events are analyzed to understand attack targets and methods",
        "description": "Analyze detected events to understand attack targets and methods.",
        "category": "Anomalies and Events"
    },
    "DE.AE-3": {
        "title": "Event data are collected and correlated from multiple sources and sensors",
        "description": "Collect and correlate event data from multiple sources and sensors.",
        "category": "Anomalies and Events"
    },
    "DE.AE-4": {
        "title": "Impact of events is determined",
        "description": "Determine the impact of detected cybersecurity events.",
        "category": "Anomalies and Events"
    },
    "DE.AE-5": {
        "title": "Incident alert thresholds are established",
        "description": "Establish thresholds for incident alerts and notifications.",
        "category": "Anomalies and Events"
    },
    "DE.CM-1": {
        "title": "The network is monitored to detect potential cybersecurity events",
        "description": "Monitor the network continuously to detect potential cybersecurity events.",
        "category": "Security Continuous Monitoring"
    },
    "DE.CM-2": {
        "title": "The physical environment is monitored to detect potential cybersecurity events",
        "description": "Monitor the physical environment to detect potential cybersecurity events.",
        "category": "Security Continuous Monitoring"
    },
    "DE.CM-3": {
        "title": "Personnel activity is monitored to detect potential cybersecurity events",
        "description": "Monitor personnel activity to detect potential cybersecurity events.",
        "category": "Security Continuous Monitoring"
    },
    "DE.CM-4": {
        "title": "Malicious code is detected",
        "description": "Detect malicious code on systems and networks.",
        "category": "Security Continuous Monitoring"
    },
    "DE.CM-5": {
        "title": "Unauthorized mobile code is detected",
        "description": "Detect unauthorized mobile code execution.",
        "category": "Security Continuous Monitoring"
    },
    "DE.CM-6": {
        "title": "External service provider activity is monitored to detect potential cybersecurity events",
        "description": "Monitor external service provider activity for potential cybersecurity events.",
        "category": "Security Continuous Monitoring"
    },
    "DE.CM-7": {
        "title": "Monitoring for unauthorized personnel, connections, devices, and software is performed",
        "description": "Monitor for unauthorized personnel, connections, devices, and software.",
        "category": "Security Continuous Monitoring"
    },
    "DE.CM-8": {
        "title": "Vulnerability scans are performed",
        "description": "Perform regular vulnerability scans on systems and applications.",
        "category": "Security Continuous Monitoring"
    },
    "DE.DP-1": {
        "title": "Roles and responsibilities for detection are well defined to ensure accountability",
        "description": "Define roles and responsibilities for detection activities to ensure accountability.",
        "category": "Detection Processes"
    },
    "DE.DP-2": {
        "title": "Detection activities comply with all applicable requirements",
        "description": "Ensure detection activities comply with applicable legal and regulatory requirements.",
        "category": "Detection Processes"
    },
    "DE.DP-3": {
        "title": "Detection processes are tested",
        "description": "Test detection processes regularly to ensure effectiveness.",
        "category": "Detection Processes"
    },
    "DE.DP-4": {
        "title": "Event detection information is communicated",
        "description": "Communicate event detection information to appropriate stakeholders.",
        "category": "Detection Processes"
    },
    "DE.DP-5": {
        "title": "Detection processes are continuously improved",
        "description": "Continuously improve detection processes based on lessons learned.",
        "category": "Detection Processes"
    },

    # RESPOND (RS)
    "RS.RP-1": {
        "title": "Response plan is executed during or after an incident",
        "description": "Execute the response plan during or after a cybersecurity incident.",
        "category": "Response Planning"
    },
    "RS.CO-1": {
        "title": "Personnel know their roles and order of operations when a response is needed",
        "description": "Ensure personnel understand their roles and operations order during response.",
        "category": "Communications"
    },
    "RS.CO-2": {
        "title": "Incidents are reported consistent with established criteria",
        "description": "Report incidents according to established criteria and procedures.",
        "category": "Communications"
    },
    "RS.CO-3": {
        "title": "Information is shared consistent with response plans",
        "description": "Share information according to established response plans.",
        "category": "Communications"
    },
    "RS.CO-4": {
        "title": "Coordination with stakeholders occurs consistent with response plans",
        "description": "Coordinate with stakeholders according to response plans.",
        "category": "Communications"
    },
    "RS.CO-5": {
        "title": "Voluntary information sharing occurs with external stakeholders to achieve broader cybersecurity situational awareness",
        "description": "Share information voluntarily with external stakeholders for situational awareness.",
        "category": "Communications"
    },
    "RS.AN-1": {
        "title": "Notifications from detection systems are investigated",
        "description": "Investigate all notifications from detection systems.",
        "category": "Analysis"
    },
    "RS.AN-2": {
        "title": "The impact of the incident is understood",
        "description": "Understand and assess the impact of cybersecurity incidents.",
        "category": "Analysis"
    },
    "RS.AN-3": {
        "title": "Forensics are performed",
        "description": "Perform forensic analysis when appropriate during incident response.",
        "category": "Analysis"
    },
    "RS.AN-4": {
        "title": "Incidents are categorized consistent with response plans",
        "description": "Categorize incidents according to established response plans.",
        "category": "Analysis"
    },
    "RS.AN-5": {
        "title": "Processes are established to receive, analyze and respond to vulnerabilities disclosed to the organization from internal and external sources",
        "description": "Establish processes to receive, analyze, and respond to vulnerability disclosures.",
        "category": "Analysis"
    },
    "RS.MI-1": {
        "title": "Incidents are contained",
        "description": "Contain cybersecurity incidents to prevent further damage.",
        "category": "Mitigation"
    },
    "RS.MI-2": {
        "title": "Incidents are mitigated",
        "description": "Mitigate the effects of cybersecurity incidents.",
        "category": "Mitigation"
    },
    "RS.MI-3": {
        "title": "Newly identified vulnerabilities are mitigated or documented as accepted risks",
        "description": "Mitigate newly identified vulnerabilities or document as accepted risks.",
        "category": "Mitigation"
    },
    "RS.IM-1": {
        "title": "Response plans incorporate lessons learned",
        "description": "Incorporate lessons learned into response plans and procedures.",
        "category": "Improvements"
    },
    "RS.IM-2": {
        "title": "Response strategies are updated",
        "description": "Update response strategies based on lessons learned and evolving threats.",
        "category": "Improvements"
    },

    # RECOVER (RC)
    "RC.RP-1": {
        "title": "Recovery plan is executed during or after a cybersecurity incident",
        "description": "Execute recovery plans during or after cybersecurity incidents.",
        "category": "Recovery Planning"
    },
    "RC.IM-1": {
        "title": "Recovery plans incorporate lessons learned",
        "description": "Incorporate lessons learned into recovery plans and procedures.",
        "category": "Improvements"
    },
    "RC.IM-2": {
        "title": "Recovery strategies are updated",
        "description": "Update recovery strategies based on lessons learned and changing requirements.",
        "category": "Improvements"
    },
    "RC.CO-1": {
        "title": "Public relations are managed",
        "description": "Manage public relations during and after cybersecurity incidents.",
        "category": "Communications"
    },
    "RC.CO-2": {
        "title": "Reputation is repaired after an incident",
        "description": "Take steps to repair organizational reputation after incidents.",
        "category": "Communications"
    },
    "RC.CO-3": {
        "title": "Recovery activities are communicated to internal and external stakeholders as well as executive and management teams",
        "description": "Communicate recovery activities to all relevant stakeholders.",
        "category": "Communications"
    }
}

# Lista de tags para compatibilidad hacia atrás
NIST_TAGS = list(NIST_CONTROLS.keys())
