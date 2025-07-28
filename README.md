<div align="center">
  <img src="https://placehold.co/600x300/1e293b/3b82f6?text=OptionForge&font=raleway" alt="OptionForge Banner">
  <h1 align="center">OptionForge</h1>
  <p align="center">
    A professional-grade platform for designing, backtesting, and analyzing complex options strategies.
  </p>
  <p align="center">
    <a href="#key-features"><strong>Features</strong></a> ·
    <a href="#tech-stack"><strong>Tech Stack</strong></a> ·
    <a href="#getting-started"><strong>Getting Started</strong></a> ·
    <a href="#api-documentation"><strong>API Docs</strong></a> ·
    <a href="#contributing"><strong>Contributing</strong></a>
  </p>
  <p align="center">
    <img src="https://github.com/<your-username>/optionforge/actions/workflows/ci.yml/badge.svg" alt="CI Status">
    <img src="https://img.shields.io/badge/python-3.11-blue.svg" alt="Python Version">
    <img src="https://img.shields.io/badge/react-18-blue.svg" alt="React Version">
    <img src="https://img.shields.io/badge/license-MIT-green.svg" alt="License">
  </p>
</div>

---

**OptionForge** is an open-source web application built for sophisticated options traders. It provides a powerful, data-driven environment to move from a strategy idea to a fully-validated model, ready for paper or live trading. Whether you're exploring a simple covered call or a complex, multi-leg, delta-neutral position, OptionForge gives you the tools to understand its performance and risk profile deeply.

## Key Features

| Feature | Description | Status |
| :--- | :--- | :--- |
| **Visual Strategy Builder** | Construct strategies with an intuitive UI. Add, remove, and configure legs (calls/puts, buy/sell, quantity). | ✅ |
| **Advanced Backtesting Engine** | Vectorized engine using `NumPy`/`Pandas` for speed. Choose between Black-Scholes and Monte Carlo pricing. | ✅ |
| **Interactive Payoff Diagrams** | Instantly visualize a strategy's P/L at expiration. Hover to see break-even points and potential profit/loss. | ✅ |
| **Comprehensive Metrics** | Go beyond P/L. Analyze Sharpe & Sortino ratios, max drawdown, profit factor, Calmar ratio, and win rate. | ✅ |
| **Greek Analysis** | Track and visualize how your position's Delta, Gamma, Theta, and Vega evolve over the life of the backtest. | ✅ |
| **Portfolio Simulation** | Combine multiple strategies into a single portfolio to analyze correlations and the combined equity curve. | ✅ |
| **Data Provider Layer** | Starts with `yfinance` for free, accessible data. Built to be extensible for higher-fidelity providers like Polygon.io. | ✅ |
| **Forward Testing Mode** | Paper trade your validated strategies using a simulated live quote stream via WebSockets. | 🚧 In-Progress |
| **Modern & Secure Auth** | JWT-based API authentication with secure user registration and login flows. | ✅ |
| **Dark/Light Theme** | A comfortable viewing experience in any lighting condition, with a seamless theme toggle. | ✅ |

### Sneak Peek

<div align="center">
  <img src="https://placehold.co/800x450/1e293b/ffffff?text=Dashboard+View" alt="Dashboard Screenshot" style="border-radius: 8px; margin: 10px;">
  <img src="https://placehold.co/800x450/1e293b/ffffff?text=Strategy+Builder+UI" alt="Strategy Builder Screenshot" style="border-radius: 8px; margin: 10px;">
</div>

## Tech Stack

OptionForge is built with a modern, scalable, and containerized architecture.

  +-------------------------+
  |      Browser (User)     |
  |   (React + TypeScript)  |
  +-------------+-----------+
                |
                | (HTTPS)
                |
  +-------------v-----------+
  |   NGINX (Frontend Host)   |
  +-------------+-----------+
                |
                | (API Calls)
                |
+-------------------v-------------------+       +-----------------+|      Gunicorn (Flask Backend)         |------>|      Redis      || (Python + SQLAlchemy + Celery Client) |<------| (Celery Broker) |+-------------------+-------------------+       +-----------------+|| (DB Queries)|+-------------v-----------+|  PostgreSQL / SQLite    |+-------------------------+
* **Frontend:** React 18 (with Vite), TypeScript, Tailwind CSS, Plotly.js
* **Backend:** Python 3.11, Flask, SQLAlchemy
* **Database:** PostgreSQL (production), SQLite (development)
* **Async Tasks:** Celery for running intensive backtests in the background.
* **Caching/Message Broker:** Redis
* **Containerization:** Docker & Docker Compose

## Getting Started

Follow these instructions to set up your local development environment.

### Prerequisites

* [Docker](https://www.docker.com/get-started)
* [Docker Compose](https://docs.docker.com/compose/install/)
* `git` for cloning the repository.
* A code editor like [VS Code](https://code.visualstudio.com/).

### Installation & Launch

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/](https://github.com/)<your-username>/optionforge.git
    cd optionforge
    ```

2.  **Configure Your Environment:**
    Create a `.env` file for the backend and a separate one for the frontend.
    
    *Backend:*
    ```bash
    # In the project root directory
    cp .env.example .env
    ```
    The defaults are fine for local development.

    *Frontend:*
    ```bash
    # In the frontend directory
    cd frontend
    echo "VITE_API_BASE_URL=http://localhost:5000/api" > .env
    cd .. 
    ```

3.  **Build and Run with Docker Compose:**
    From the project's root directory, run:
    ```bash
    docker-compose up --build
    ```
    This command will build the images, start the containers, and link them together.

4.  **Access the Application:**
    * **💻 Frontend App:** [http://localhost:5173](http://localhost:5173)
    * **⚙️ Backend API:** [http://localhost:5000](http://localhost:5000)
    * **📚 API Docs (Swagger UI):** [http://localhost:5000/docs](http://localhost:5000/docs)

5.  **Seed the Database (Highly Recommended):**
    To make the app useful, populate it with sample strategies and historical options data. Open a **new terminal window** and run:
    ```bash
    docker-compose exec web python scripts/seed_data.py
    ```
    > **Warning:** This will download several gigabytes of data and may take a very long time (30+ minutes) depending on your internet connection.

## Project Structure

A brief overview of the repository layout.

optionforge/├── .github/                # GitHub Actions CI/CD workflows├── backend/│   ├── optionforge/        # Main Flask application package│   │   ├── api/            # API blueprints (auth, strategies, etc.)│   │   ├── backtester/     # Core backtesting engine and logic│   │   ├── main/           # Core application routes│   │   ├── models.py       # SQLAlchemy DB models│   │   └── init.py     # Application factory│   ├── scripts/            # Helper scripts (e.g., seed_data.py)│   ├── tests/              # Backend tests│   └── requirements.txt    # Python dependencies├── docker/│   ├── Dockerfile          # Backend Dockerfile│   └── docker-compose.yml  # Docker Compose configuration├── frontend/│   ├── public/             # Static assets│   ├── src/                # React source code│   │   ├── api/            # API client setup│   │   ├── components/     # Reusable UI components│   │   ├── context/        # React context providers (Auth, Theme)│   │   ├── hooks/          # Custom React hooks│   │   ├── layouts/        # Main application layout│   │   ├── pages/          # Page components│   │   └── ...│   ├── Dockerfile          # Frontend Dockerfile (for NGINX)│   └── package.json        # Node.js dependencies└── README.md               # You are here!
## API Documentation

The backend provides a ReST/JSON API that is documented using the OpenAPI 3.0 standard. When the application is running, you can access an interactive Swagger UI to explore and test the API endpoints.

➡️ **[http://localhost:5000/docs](http://localhost:5000/docs)**

## Contributing

We welcome contributions from the community! Whether it's a bug fix, a new feature, or documentation improvements, your help is appreciated. Please see our [Contributing Guide](CONTRIBUTING.md) (placeholder) for more details on how to get started.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
