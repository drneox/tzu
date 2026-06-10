# TZU 🛡️

[![Version](https://img.shields.io/github/v/release/drneox/tzu?include_prereleases)](https://github.com/drneox/tzu/releases)
[![Build Status](https://img.shields.io/github/actions/workflow/status/drneox/tzu/python-app-test.yml)](https://github.com/drneox/tzu/actions/workflows/python-app-test.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.68+-green.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18+-blue.svg)](https://reactjs.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)
[![OWASP](https://img.shields.io/badge/OWASP-Compliant-red.svg)](https://owasp.org/)

<img src="tzu.png" alt="TZU Logo" width="200">

An AI-powered comprehensive web application designed to help identify threats and manage action plans, following industry cybersecurity standards including OWASP Risk Rating, STRIDE, OWASP ASVS/MASVS.

## 🤔 Why TZU?

**TZU** is inspired by **Sun Tzu**, the Chinese military strategist and philosopher, author of *“The Art of War,”* one of the most influential works on strategy and tactics.


> “Victorious warriors win first and then go to war; defeated warriors go to war first and then seek to win.” — Sun Tzu


Just as Sun Tzu emphasizes knowing the enemy — and knowing yourself — to achieve victory, TZU empowers cybersecurity teams to:

- 🧭 **Know Yourself:** Inventory assets and data; identify crown jewels; map trust boundaries and data flows.
- 🎯 **Profile Adversaries:** Capture skill, motive, opportunity/exposure, and size.  
  _OWASP RR → populates **Threat Agent Factors**, driving **Likelihood**._
- 🔍 **Know Your Threats:** Derive threats from **architecture/DFD diagrams** and **use cases**, supported by AI-assisted analysis.
- 🛡️ **Know Your Defenses:** Assess your current posture and **vulnerabilities**; map **controls** to **OWASP ASVS/MASVS**.
- ⚔️ **Strategic Planning:** Define **mitigation plans prioritized by risk level**; apply a **consistent risk model (Likelihood × Impact)** to **calculate and track** **inherent, current, and residual risk**.










In cybersecurity—as in ancient warfare—**preparation and intelligence make the difference**. TZU delivers the tools and traceability to stay ahead of threats and protect your digital assets by applying Sun Tzu’s strategic wisdom to modern security challenges.




## 🚀 Quick Start

### 🐳 Docker Deployment (Recommended)

> **Prerequisites:** [Docker Desktop](https://www.docker.com/products/docker-desktop) must be installed and running. On Windows, enable the **WSL2 backend** in Docker Desktop settings.

The fastest way to get TZU running is with our automated setup script:

**Linux / macOS / WSL2:**
```bash
# 1. Clone the repository
git clone https://github.com/drneox/tzu
cd tzu

# 2. Configure environment (optional but recommended)
cp .env.example .env
# Edit .env and set:
# - AI_API_KEY=your_api_key_here
# - TZ=your_timezone (e.g., America/New_York, Europe/London, America/Lima)

# 3. Run the automated setup script
./start.sh
```

**Windows (PowerShell):**
```powershell
# 1. Clone the repository
git clone https://github.com/drneox/tzu
cd tzu

# 2. Configure environment
copy .env.example .env
# Edit .env and set AI_API_KEY and TZ

# 3. Run the Windows setup script
.\start.ps1
```

The script will automatically:
- 🔧 Build and start all services (nginx, backend, postgresql)
- 🔐 Generate secure admin credentials
- 📋 Display access information

**⚙️ Configuration Notes:**
- **AI Features**: Choose ONE AI provider - either OpenAI OR Anthropic API key (not both)
- **Timezone**: Set your local timezone for accurate timestamps in reports and logs

**Access the application:**
- **Web App**: http://localhost:3434
- **API Docs**: http://localhost:3434/api/docs
- **Credentials**: Displayed after setup completion


## ✨ Features

### Core Functionality
- **AI-Powered Threat Identification**: Intelligent threat detection and analysis capabilities
- **Action Plan Management**: Comprehensive management of security action plans and remediation strategies
- **OWASP Risk Rating**: Complete implementation for risk level categorization with threat agent factors, vulnerability factors, and impact calculations
- **Industry Standards Compliance**: Built following OWASP Risk Rating, STRIDE, OWASP ASVS, and MASVS cybersecurity standards
- **Threat Modeling**: Interactive diagram upload and threat identification
- **Risk Assessment**: Automated calculation of likelihood and impact scores to determine risk levels
- **PDF Reports**: Professional report generation with detailed analysis and security recommendations
- **Multi-language Support**: English and Spanish localization

## 🔐 Authentication & Security

### Default Credentials
After deployment, generate secure credentials:

```bash
docker exec docker-backend-1 python show_credentials.py
```

This will display:
- **Username**: `admin`
- **Password**: Auto-generated secure password

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

## �🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request


## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- **Carlos Ganoza ** - *Initial work* - [@drneox](https://github.com/drneox)

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

*English Version | [Versión en Español](README.es.md)*

