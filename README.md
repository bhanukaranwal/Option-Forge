# OptionForge

**OptionForge** is a modern, professional-grade web platform for designing, back-testing, and analyzing multi-leg options strategies. It provides a powerful, intuitive interface for traders to validate their ideas against historical data before risking capital.

![OptionForge Screenshot (Conceptual)](https://placehold.co/1200x600/1a202c/ffffff?text=OptionForge%20Dashboard)

## Key Features

* **Visual Strategy Builder:** Drag-and-drop interface to construct complex multi-leg options strategies.
* **Powerful Backtest Engine:** Vectorized engine using NumPy/Pandas for high-speed analysis. Supports Black-Scholes and Monte Carlo pricing models.
* **In-Depth Analytics:** Comprehensive performance metrics including P/L curves, Sharpe/Sortino ratios, max drawdown, and Greek exposures over time.
* **Interactive Payoff Diagrams:** Instantly visualize the risk/reward profile of any strategy at expiration.
* **Portfolio-Level Testing:** Combine multiple strategies and analyze their correlated performance.
* **Forward Testing:** Paper-trade your strategies with simulated live market data.
* **Secure & Scalable:** Built with a modern tech stack, featuring JWT-based authentication, background task processing, and a containerized architecture for easy deployment.

## Tech Stack

* **Backend:** Python 3.11, Flask, SQLAlchemy, Celery, Redis
* **Frontend:** React 18, TypeScript, Vite, Tailwind CSS, Plotly.js
* **Database:** SQLite (dev), PostgreSQL (prod)
* **Containerization:** Docker & Docker Compose
* **Testing:** Pytest, Vitest
* **CI/CD:** GitHub Actions

## Quick Start & Setup

Follow these steps to get the OptionForge platform running locally for development.

1.  **Clone the Repository:**
    ```bash
    git clone <repository-url>
    cd optionforge
    ```

2.  **Configure Environment:**
    Copy the example environment file and customize it as needed.
    ```bash
    cp .env.example .env
    ```
    *Note: The default `.env` is configured for local development with Docker and SQLite.*

3.  **Build and Run with Docker:**
    Make sure you have Docker and Docker Compose installed. Then, run:
    ```bash
    docker-compose up --build
    ```
    This command will build the images for the backend and frontend, and start the `web`, `worker`, and `redis` services.

4.  **Access the Application:**
    * **Frontend:** Open your browser to [http://localhost:5173](http://localhost:5173)
    * **Backend API:** The API will be available at [http://localhost:5000](http://localhost:5000)
    * **API Docs (Swagger UI):** [http://localhost:5000/docs](http://localhost:5000/docs)

5.  **Seed the Database (Optional):**
    To populate the database with sample data (SPY/QQQ option chains and example strategies), run the seed script:
    ```bash
    docker-compose exec web python -m scripts.seed_data
    ```
    *This may take a significant amount of time as it downloads several years of options data.*

## Environment Variables

The following environment variables are used for configuration. They should be placed in a `.env` file in the project root.

backend/config.pyFLASK_ENV=developmentSECRET_KEY=a_very_secret_key_that_should_be_changedDATABASE_URL=sqlite:///../instance/optionforge.dbCELERY_BROKER_URL=redis://redis:6379/0CELERY_RESULT_BACKEND=redis://redis:6379/0YFINANCE_TICKERS="SPY QQQ"frontend/.envVITE_API_BASE_URL=http://localhost:5000
## API Documentation

The ReST/JSON API is documented using the OpenAPI 3 standard. An interactive Swagger UI is available at the `/docs` endpoint when the application is running.

A Postman collection can be generated from the `openapi.json` file available at `/openapi.json`.
