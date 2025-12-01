

*This visualization demonstrates the engine's genetic algorithm iterating through generations of strategies, with fitness (Sharpe Ratio) and complexity plotted in real-time.*

## Quick Start

This repository contains the core engine framework. Deployment requires configuration for specific data sources and execution venues.

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/psiquis-x/psiquis-quant-engine.git
    cd psiquis-quant-engine
    ```

2.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure the Environment:**
    *   Modify `config/environment.yml` to specify data paths, API keys, and risk parameters.

4.  **Initiate an Optimization Run:**
    ```bash
    python main.py --mode=optimize --strategy-universe=equities_sp500
    ```

---

## Deploy This Architecture

This repository represents the core framework of the Psiquis-X Quant Engine. It is a production-ready system designed for institutional deployment.

For enterprise licensing, custom integrations, and managed deployment, please contact our solutions architecture team.

**[Contact Psiquis-X](mailto:orquestadrop6@gmail.com?subject=Inquiry:%20Psiquis-X%20Quant%20Engine%20Deployment)**