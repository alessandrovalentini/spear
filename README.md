![logo](doc/imgs/logo.png)

# What is SPEAR

**SPEAR** is a project designed to provide a low-cost, smart Power Distribution Unit (PDU) based on Arduino and Raspberry Pi Zero, primarily intended for homelab environments.

The goal is to **measure power consumption** and **control power to individual plugs**, both via physical switches and a web API.

Power metrics are exposed via a **Prometheus-compatible endpoint**, allowing for easy collection and visualization using **Prometheus** and **Grafana**.

The project is designed to be **stateless**. Prometheus and Grafana are expected to be hosted externally to enable centralized monitoring environments.

---

# ⚠️ Disclaimer

This project involves working with **high-voltage electricity (110/240V)**, which can cause serious damage to equipment, electrical systems, or even result in personal injury or death.

**Use this project at your own risk.** You assume full responsibility for any damage or injury.  
The author assumes no liability for any harm resulting from the use of this project.

---

# 🛠 Roadmap

### 🔌 Power Measurement via Arduino
- [x] Measure current
- [x] Measure voltage
- [ ] Calculate power
- [ ] Calibrate specific sensors

### 🌐 Web Service
- [x] Read power data from Arduino
- [x] Expose Prometheus-compatible endpoint
- [ ] Implement basic authentication for all services
- [x] Load configuration from file

### ⚙️ Plug Control
- [ ] Control plugs via physical switch
- [ ] Control plugs via API
- [ ] Read actual plug state
- [ ] Control status LED for switches

### 🧪 Testing Environment
- [x] Launch Prometheus and Grafana via Docker Compose (for local testing)
- [x] Automatically configure Prometheus to scrape local instance
- [ ] Automatically configure Grafana to connect to local Prometheus
- [ ] Generate random values to simulate data without Arduino

### 📊 Other
- [ ] Provide ready-to-use Grafana dashboards
