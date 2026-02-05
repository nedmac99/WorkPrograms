<div align="center">

# 🛠️ WorkPrograms

### Workplace Automation & Efficiency Tools

[![Python](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/)
[![Chrome Extension](https://img.shields.io/badge/Chrome-Extension-yellow.svg)](https://developer.chrome.com/docs/extensions/)
[![License](https://img.shields.io/badge/License-Personal%20Use-green.svg)](#license)

*A curated collection of automation tools designed to streamline workflows and boost productivity in technical repair and maintenance operations.*

[Getting Started](#getting-started) • [Programs](#programs) • [Documentation](#documentation)

---

</div>

## 📋 Overview

This repository houses production-ready automation tools developed to eliminate repetitive manual tasks and improve operational efficiency in a professional repair environment. Each tool is designed with reliability, ease of use, and real-world applicability in mind.

## 🚀 Programs

### 🌐 Stratus Manufacture Warranty Form Automation
> **Chrome Extension** • *Manifest V3* • `stratus_mw_form_automation/`

Intelligent browser automation for internal repair documentation. Reduces form completion time by 80%+ through smart auto-fill capabilities.

**Key Features:**
- ✨ **Smart Auto-Fill** - System Hours, Oxygen Purity, and diagnostic fields
- 📊 **Test Results Automation** - Flow rates, PSI, O2 purity measurements
- 🔧 **Parts Table Management** - Automatic part matching and confirmation
- 🔍 **Dry Run Mode** - Preview all actions before execution
- 💾 **Persistent Storage** - Chrome sync for cross-device value retention
- 🎯 **Intelligent Keyword Matching** - Resilient to form wording variations

**Tech Stack:** JavaScript, Chrome Extension API (MV3), Chrome Storage API

📖 [View Full Documentation →](stratus_mw_form_automation/README.md)

---

### 📦 Parts List Tracker
> **Python Script** • *Command Line Tool* • `Parts List/`

Streamlined serial number and parts inventory management system with persistent storage.

**Key Features:**
- 🔢 Serial number logging and tracking
- 📝 Multi-part entry support per serial
- 💾 Persistent data storage (text file)
- 🖥️ Simple command-line interface

**Tech Stack:** Python 3.x

**Use Cases:**
- Equipment repair tracking
- Parts inventory auditing
- Serial number history logging

---

### ⚖️ Weighted Output Tracker
> **Analytics Tool** • *Performance Metrics* • `weighted_output_tracker/`

Comprehensive tracking and analysis system for weighted output data, enabling data-driven efficiency insights.

**Key Features:**
- 📈 Performance metrics calculation
- 📊 Work efficiency analysis
- 📉 Historical data tracking

**Tech Stack:** Python 3.x, TeX (documentation)

---

## 🏁 Getting Started

### Prerequisites

Ensure you have the following installed:

| Tool | Version | Purpose |
|------|---------|---------|
| **Python** | 3.x+ | Python scripts |
| **Google Chrome** | Latest | Form automation extension |

### Installation

Each tool has specific setup requirements. Navigate to the respective directory for detailed instructions:

```bash
# Clone the repository
git clone https://github.com/nedmac99/WorkPrograms.git
cd WorkPrograms

# Navigate to desired tool
cd stratus_mw_form_automation/  # For Chrome extension
# or
cd "Parts List/"                # For parts tracker
# or
cd weighted_output_tracker/     # For output tracker
```

## 📖 Documentation

- **[Form Automation Setup Guide](stratus_mw_form_automation/README.md)** - Complete Chrome extension installation and usage
- Each program directory contains specific documentation and setup instructions

## 🎯 Use Cases

These tools are optimized for:
- ✅ Technical repair operations
- ✅ Equipment maintenance documentation
- ✅ Parts inventory management
- ✅ Performance metrics tracking
- ✅ Quality assurance processes

## 🤝 Contributing

These tools are currently maintained for internal workplace use. For questions or collaboration opportunities, please open an issue.

## 📊 Repository Stats

![Top Languages](https://img.shields.io/badge/TeX-51.9%25-blue)
![HTML](https://img.shields.io/badge/HTML-27.9%25-orange)
![Python](https://img.shields.io/badge/Python-12.6%25-yellow)
![JavaScript](https://img.shields.io/badge/JavaScript-7.0%25-green)

## 📄 License

This project is developed for personal and workplace use. All rights reserved.

---

<div align="center">

*Last Updated: February 2026*

</div>
