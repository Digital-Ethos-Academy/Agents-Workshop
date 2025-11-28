# VM Setup Requirements for Agents Workshop

**Document Purpose:** Technical specifications for provisioning student VMs  
**Target Audience:** IT/DevOps team setting up workshop environments  
**Workshop:** Crafting Custom Agents (6 hours)  
**Students per session:** _[Fill in expected count]_

---

## 1. VM Specifications

### Minimum Requirements
| Resource | Specification |
|----------|---------------|
| **OS** | Ubuntu 22.04 LTS or Ubuntu 24.04 LTS |
| **CPU** | 2 vCPUs |
| **RAM** | 8 GB |
| **Storage** | 30 GB SSD |
| **Network** | Outbound HTTPS (port 443) to OpenAI, Anthropic, Tavily APIs |

### Recommended (for smoother experience)
| Resource | Specification |
|----------|---------------|
| **CPU** | 4 vCPUs |
| **RAM** | 16 GB |
| **Storage** | 50 GB SSD |

---

## 2. Software Installation

### 2.1 System Packages
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y \
    python3.11 \
    python3.11-venv \
    python3-pip \
    git \
    curl \
    wget \
    build-essential \
    libffi-dev \
    libssl-dev
```

### 2.2 Clone Repository
```bash
cd /home/student
git clone https://github.com/Digital-Ethos-Academy/Agents-Workshop.git
cd Agents-Workshop
```

### 2.3 Python Environment
```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### 2.4 Jupyter Setup
```bash
# Install Jupyter kernel for the virtual environment
source .venv/bin/activate
python -m ipykernel install --user --name=agents-workshop --display-name="Agents Workshop"
```

---

## 3. API Keys Configuration

### Required Keys
Create `/home/student/Agents-Workshop/.env` with the following:

```env
# REQUIRED - Workshop will not function without this
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxx

# OPTIONAL - For web search functionality in labs
TAVILY_API_KEY=tvly-xxxxxxxxxxxxxxxxxxxx

# OPTIONAL - For Anthropic examples
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxxxxxx
```

### Key Provisioning Options

**Option A: Pre-configured Keys (Recommended)**
- Provision shared API keys with spending limits
- Set per-key limits: ~$5-10 per student for safety
- Pre-populate `.env` file on each VM

**Option B: Student-provided Keys**
- Students bring their own OpenAI API keys
- Provide `.env.example` template (already in repo)
- Estimated cost per student: $1-3

### API Key Sources
| Provider | URL | Free Tier |
|----------|-----|-----------|
| OpenAI | https://platform.openai.com/api-keys | No (pay-as-you-go) |
| Tavily | https://tavily.com | Yes (1000 calls/month) |
| Anthropic | https://console.anthropic.com | No |

---

## 4. IDE/Editor Setup

### Option A: VS Code (Recommended)
```bash
# Install VS Code
sudo snap install code --classic

# Install extensions
code --install-extension ms-python.python
code --install-extension ms-toolsai.jupyter
code --install-extension ms-python.vscode-pylance
```

### Option B: JupyterLab (Browser-based)
```bash
source /home/student/Agents-Workshop/.venv/bin/activate
pip install jupyterlab
jupyter lab --ip=0.0.0.0 --port=8888 --no-browser
```

If using JupyterLab, configure firewall to allow port 8888.

---

## 5. Verification Script

Run this to verify the environment is correctly configured:

```bash
cd /home/student/Agents-Workshop
source .venv/bin/activate
python check_environment.py
```

**Expected Output:**
```
✓ Python 3.11.x
✓ All required packages installed
✓ OPENAI_API_KEY configured
✓ OpenAI API connection successful
✓ utils package importable
All checks passed! You're ready for the workshop.
```

---

## 6. Network Requirements

### Outbound Access Required
| Destination | Port | Purpose |
|-------------|------|---------|
| api.openai.com | 443 | LLM API calls |
| api.anthropic.com | 443 | Anthropic API (optional) |
| api.tavily.com | 443 | Web search tool |
| pypi.org | 443 | Package installation |
| github.com | 443 | Repository clone |
| cdn.tailwindcss.com | 443 | Slide styling |

### No Inbound Access Required
(Unless using JupyterLab remotely)

---

## 7. User Account Setup

```bash
# Create student user (if not using default)
sudo useradd -m -s /bin/bash student
sudo passwd student

# Set ownership
sudo chown -R student:student /home/student/Agents-Workshop

# Add to sudoers (optional, for troubleshooting)
sudo usermod -aG sudo student
```

---

## 8. Pre-Workshop Checklist

| Task | Verified |
|------|----------|
| VM provisioned with specs above | ☐ |
| Python 3.11 installed | ☐ |
| Repository cloned | ☐ |
| Virtual environment created | ☐ |
| All pip packages installed | ☐ |
| `.env` file configured with API keys | ☐ |
| VS Code or JupyterLab installed | ☐ |
| `check_environment.py` passes | ☐ |
| Student can open Lab 1 notebook | ☐ |
| Network connectivity to OpenAI verified | ☐ |

---

## 9. Troubleshooting

### Package Installation Fails
```bash
# Ensure pip is updated
pip install --upgrade pip setuptools wheel

# If specific package fails, try:
pip install --no-cache-dir -r requirements.txt
```

### API Key Not Working
```bash
# Verify .env is loaded
python -c "from dotenv import load_dotenv; load_dotenv(); import os; print(os.getenv('OPENAI_API_KEY')[:10])"
```

### Jupyter Kernel Not Found
```bash
source .venv/bin/activate
python -m ipykernel install --user --name=agents-workshop
jupyter kernelspec list
```

---

## 10. Support Contact

For issues during VM setup, contact:  
**[Workshop Coordinator Email]**  
**[IT Support Contact]**

---

## Appendix: Quick Setup Script

Save as `setup_vm.sh` and run with sudo:

```bash
#!/bin/bash
set -e

# Update system
apt update && apt upgrade -y
apt install -y python3.11 python3.11-venv python3-pip git curl

# Setup student environment
cd /home/student
git clone https://github.com/Digital-Ethos-Academy/Agents-Workshop.git
cd Agents-Workshop

# Python environment
python3.11 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
python -m ipykernel install --user --name=agents-workshop

# Create .env template (API keys need to be added)
cp .env.example .env

# Set permissions
chown -R student:student /home/student/Agents-Workshop

echo "Setup complete! Add API keys to .env and run: python check_environment.py"
```
