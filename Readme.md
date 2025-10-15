# ☕ Café Sales ETL Pipeline


An end-to-end ETL (Extract, Transform, Load) data pipeline designed for café sales analytics. This project demonstrates production-grade data engineering practices using Apache Airflow, Python, and PostgreSQL to automate data processing, quality validation, and business intelligence reporting.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Pipeline Workflow](#pipeline-workflow)
- [Sample Outputs](#sample-outputs)
- [Future Enhancements](#future-enhancements)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## 🎯 Overview

This project implements a comprehensive ETL pipeline that processes raw café sales data through a series of automated stages: data extraction from CSV files, data cleansing and validation, loading into a PostgreSQL data warehouse, executing analytical SQL queries, and generating visual reports. The entire workflow is orchestrated using Apache Airflow, ensuring reliability, monitoring, and scalability.

**Key Capabilities:**
- Automated daily processing of sales transactions
- Data quality validation and error handling
- SQL-based business intelligence reporting
- Automated visualization generation
- Scalable architecture supporting multiple data sources

## ✨ Features

- **Automated ETL Orchestration**: Fully automated pipeline scheduling and monitoring via Apache Airflow DAGs
- **Data Quality Validation**: Built-in checks for data integrity, completeness, and consistency
- **Flexible Data Processing**: Modular design supporting easy integration of new data sources
- **Business Intelligence Reports**: Pre-configured SQL queries for common business metrics
- **Visual Analytics**: Automatic generation of charts and graphs from analytical results
- **Error Handling**: Robust exception handling and logging throughout the pipeline
- **Database Management**: Efficient data loading with SQLAlchemy ORM

## 🏗️ Architecture

The pipeline follows a layered ETL architecture:

```
Raw Data (CSV) → Extract → Transform → Load → PostgreSQL → Analyze → Visualize
                    ↓         ↓          ↓         ↓           ↓         ↓
                 Airflow   Pandas   SQLAlchemy  Warehouse    SQL    Matplotlib
```

**Pipeline Stages:**

1. **Extract**: Load raw CSV data from the `/data` directory
2. **Transform**: Clean and standardize data using Pandas (handle missing values, format dates, validate numeric fields)
3. **Load**: Insert processed data into PostgreSQL using SQLAlchemy with transaction management
4. **Validate**: Execute data quality checks (row counts, null checks, schema validation)
5. **Analyze**: Run SQL queries for business metrics and save results as CSV reports
6. **Visualize**: Generate charts (bar, line, pie) from analytical results

## 🛠️ Tech Stack

| Technology | Purpose | Version |
|-----------|---------|---------|
| **Apache Airflow** | Workflow orchestration and scheduling | 2.0+ |
| **Python** | Core ETL logic and data processing | 3.12 |
| **Pandas** | Data manipulation and transformation | Latest |
| **SQLAlchemy** | Database ORM and connection management | Latest |
| **PostgreSQL** | Relational data warehouse | 13+ |
| **Matplotlib** | Data visualization and chart generation | Latest |
| **Linux** | Development and deployment environment | Arch Linux |

## 📁 Project Structure

```
cafe_sales_etl/
├── airflow/
│   └── dags/
│       └── cafe_sales_etl_dag.py      # Main Airflow DAG definition
├── data/
│   └── dirty_cafe_sales.csv           # Raw input dataset
├── reports/                            # Generated CSV reports (gitignored)
├── plots/                              # Generated visualizations (gitignored)
├── sql_queries/
│   ├── top_items.sql                  # Top-selling products query
│   ├── revenue_by_location.sql        # Location-based revenue analysis
│   └── daily_revenue.sql              # Daily revenue trends
├── utils/
│   └── pipeline_utils.py              # Reusable ETL helper functions
├── requirements.txt                    # Python dependencies
├── .gitignore                         
└── README.md
```

## 🚀 Installation

### Prerequisites

- Python 3.12 or higher
- PostgreSQL 13 or higher
- pip (Python package manager)
- Git

### Setup Steps

**1. Clone the Repository**
```bash
git clone https://github.com/<your-username>/cafe_sales_etl.git
cd cafe_sales_etl
```

**2. Create Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

**3. Install Dependencies**
```bash
pip install -r requirements.txt
```

**4. Configure PostgreSQL**

Create the database and user:
```sql
CREATE DATABASE cafe_sales;
CREATE USER cafe_user WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE cafe_sales TO cafe_user;
```

Update connection settings in `utils/pipeline_utils.py` or use environment variables:
```bash
export DB_HOST=localhost
export DB_PORT=5432
export DB_NAME=cafe_sales
export DB_USER=cafe_user
export DB_PASSWORD=your_secure_password
```

**5. Initialize Airflow**
```bash
export AIRFLOW_HOME=$(pwd)/airflow
airflow db init
airflow users create \
    --username admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com
```

## 💻 Usage

### Starting the Pipeline

**1. Start Airflow Services**

In separate terminal windows:

```bash
# Terminal 1: Web Server
airflow webserver --port 8080

# Terminal 2: Scheduler
airflow scheduler
```

**2. Access Airflow UI**

Navigate to `http://localhost:8080` and log in with your admin credentials.

**3. Trigger the DAG**

- Locate the `cafe_sales_etl` DAG in the UI
- Toggle the DAG to "ON"
- Click "Trigger DAG" to start execution

**4. Monitor Execution**

View real-time logs, task status, and execution history in the Airflow UI.

### Running Standalone Components

You can also execute individual pipeline components:

```bash
# Run ETL without Airflow
python utils/pipeline_utils.py

# Execute specific SQL query
psql -d cafe_sales -f sql_queries/top_items.sql
```

## 🔄 Pipeline Workflow

The Airflow DAG orchestrates the following task sequence:

```
start → extract_data → clean_data → load_to_db → validate_data → 
generate_reports → create_visualizations → end
```

**Task Details:**

- **extract_data**: Reads raw CSV file into Pandas DataFrame
- **clean_data**: Applies data cleansing rules (null handling, type conversion, validation)
- **load_to_db**: Inserts cleaned data into PostgreSQL with upsert logic
- **validate_data**: Runs data quality checks and logs results
- **generate_reports**: Executes SQL queries and exports results to CSV
- **create_visualizations**: Generates PNG charts from report data

## 📊 Sample Outputs

### Generated Reports

The pipeline produces the following analytical reports in `/reports`:

- **top_items.csv**: Best-selling products by quantity and revenue
- **revenue_by_location.csv**: Sales performance by café location
- **daily_revenue.csv**: Daily transaction counts and revenue trends

### Visualizations

Automatically generated charts in `/plots`:

- **top_items.png**: Horizontal bar chart of top products
- **revenue_by_location.png**: Bar chart comparing location performance
- **daily_revenue.png**: Line chart showing revenue trends over time

*Example visualization:*

```
Revenue by Location
┌─────────────────────────────┐
│ Downtown  ████████████ $45K │
│ Uptown    ████████ $32K     │
│ Suburbs   █████ $21K        │
└─────────────────────────────┘
```

## 🔮 Future Enhancements

- [ ] Implement data quality framework using **Great Expectations**
- [ ] Containerize with **Docker** and **Docker Compose** for portability
- [ ] Add **dbt** for advanced SQL transformations
- [ ] Integrate **Apache Spark** for large-scale data processing
- [ ] Implement **CI/CD pipeline** with GitHub Actions
- [ ] Add **alerting system** (email/Slack) for pipeline failures
- [ ] Create **interactive dashboards** using Tableau or Power BI
- [ ] Implement **incremental loading** for improved performance
- [ ] Add **unit tests** and **integration tests**
- [ ] Set up **monitoring** with Prometheus and Grafana

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

Please ensure your code follows PEP 8 style guidelines and includes appropriate tests.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Contact

**Alhussain Baalawi**

Data Engineer | Python & SQL Developer

- GitHub: [@Hsooni491](https://github.com/Hsooni491)
- LinkedIn: [Alhussain-Baalawi](https://linkedin.com/in/Alhussain-Baalawi)
- Email: h.baalawi@outlook.com

---

⭐ If you found this project helpful, please consider giving it a star!

**Project Link**: [https://github.com/Hsooni491/cafe_sales_etl](https://github.com/Hsooni491/cafe_sales_etl)
