# TZU - Threat Zero Utility 

An AI-powered comprehensive web application designed to help identify threats and manage action plans, following industry cybersecurity standards including OWASP Risk Rating, STRIDE, OWASP ASVS/ MASVS.

![TZU Logo](static/tzu.png)

## 🚀 Features

### Core Functionality
- **AI-Powered Threat Identification**: Intelligent threat detection and analysis capabilities
- **Action Plan Management**: Comprehensive management of security action plans and remediation strategies
- **OWASP Risk Rating**: Complete implementation for risk level categorization with threat agent factors, vulnerability factors, and impact calculations
- **Industry Standards Compliance**: Built following OWASP Risk Rating, STRIDE, OWASP ASVS, and MASVS cybersecurity standards
- **Threat Modeling**: Interactive diagram upload and threat identification
- **Risk Assessment**: Automated calculation of likelihood and impact scores to determine risk levels
- **PDF Reports**: Professional report generation with detailed analysis and security recommendations based on MASVS/ASVS standards
- **Multi-language Support**: English and Spanish localization

### Technical Features
- **Modern React Frontend**: Built with Chakra UI for responsive design
- **FastAPI Backend**: High-performance Python API with SQLAlchemy ORM
- **Authentication System**: Secure user management with protected routes

## 🛠️ Technology Stack

### Backend
- **FastAPI** - Modern, fast web framework for building APIs
- **SQLAlchemy** - SQL toolkit and ORM
- **Alembic** - Database migration tool
- **Python 3.11+** - Core programming language

### Frontend
- **React 18** - Modern UI library
- **Chakra UI** - Simple, modular, and accessible component library
- **React Router** - Declarative routing for React
- **jsPDF** - PDF generation in JavaScript
- **Axios** - HTTP client for API requests

### Development & Testing
- **Jest** - JavaScript testing framework
- **React Testing Library** - Testing utilities for React components
- **ESLint** - Code linting and formatting
- **Git** - Version control system


**Test Coverage:**
- 8 test suites
- 79+ individual tests
- Components, services, hooks, and integration testing
- Comprehensive mocking for external dependencies

## 📊 Cybersecurity Standards & Methodologies

This AI-powered application helps identify threats and manage action plans by implementing industry-leading cybersecurity standards and methodologies.

### Threat Identification & Action Plan Management

The system combines artificial intelligence with established cybersecurity frameworks to:
- **Identify Threats**: AI-powered analysis for comprehensive threat detection
- **Manage Action Plans**: Structured approach to security remediation and risk mitigation
- **Follow Industry Standards**: Implementation based on market-leading cybersecurity standards

### Supported Cybersecurity Standards

- **OWASP Risk Rating**: Complete methodology for risk level categorization and assessment
- **STRIDE**: Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, and Elevation of Privilege threat categorization
- **OWASP ASVS**: Application Security Verification Standard for comprehensive security requirements coverage
- **OWASP MASVS**: Mobile Application Security Verification Standard for mobile security assessment and security recommendations generation

### Risk Assessment Process

The OWASP Risk Rating methodology categorizes risk levels by evaluating factors across four dimensions:

### Threat Agent Factors
- **Skill Level**: How technically skilled is this group of threat agents?
- **Motive**: How motivated is this group of threat agents to find and exploit this vulnerability?
- **Opportunity**: What resources and opportunities are required for this group of threat agents to find and exploit this vulnerability?
- **Size**: How large is this group of threat agents?

### Vulnerability Factors
- **Ease of Discovery**: How easy is it for this group of threat agents to discover this vulnerability?
- **Ease of Exploit**: How easy is it for this group of threat agents to actually exploit this vulnerability?
- **Awareness**: How well known is this vulnerability to this group of threat agents?
- **Intrusion Detection**: How likely is an exploit to be detected?

### Technical Impact
- **Loss of Confidentiality**: How much data could be disclosed and how sensitive is it?
- **Loss of Integrity**: How much data could be corrupted and how damaged is it?
- **Loss of Availability**: How much service could be lost and how vital is it?
- **Loss of Accountability**: Are the threat agents' actions traceable to an individual?

### Business Impact
- **Financial Damage**: How much financial damage will result from an exploit?
- **Reputation Damage**: Would an exploit result in reputation damage that would harm the business?
- **Non-Compliance**: How much exposure does this create for non-compliance with regulations?
- **Privacy Violation**: How much personally identifiable information could be disclosed?

## 🏗️ Architecture

### Project Structure
```
tzu/
├── alembic/              # Database migrations
├── frontend/             # React application
│   ├── src/
│   │   ├── components/   # React components
│   │   ├── services/     # API services
│   │   ├── hooks/        # Custom React hooks
│   │   ├── locales/      # Internationalization
│   │   └── __tests__/    # Test files
├── static/               # Static assets
├── templates/            # HTML templates
├── api.py               # FastAPI application
├── models.py            # SQLAlchemy models
├── schemas.py           # Pydantic schemas
├── crud.py              # Database operations
└── requirements.txt     # Python dependencies
```



## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow conventional commit messages
- Maintain test coverage above 80%
- Use ESLint for code formatting
- Write comprehensive documentation

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- **Carlos Ganoza (drneox)** - *Initial work* - [@drneox](https://github.com/drneox)

## 🙏 Acknowledgments

- [OWASP Foundation](https://owasp.org/) for the cybersecurity frameworks and methodologies
- [OWASP Lima Chapter](https://owasp.org/www-chapter-lima/) for the cybersecurity community support and guidance
- Contributors and the open-source community

## 📧 Support

If you have questions or need support, please:

1. Check the [documentation](README.md)
2. Search existing [issues](https://github.com/drneox/tzu/issues)
3. Create a new issue if needed

---

