# SpendWise – Smart Expense Analyzer

**An interactive expense analysis application powered by Python, data visualization, and machine learning.**

[Live Demo](https://durga2343-spendwise-app-sofwov.streamlit.app/) · [GitHub Repository](https://github.com/Durga2343/Spendwise)

## Overview

SpendWise is a web-based expense analysis application designed to help users understand their spending habits through interactive dashboards, data visualization, and machine learning-based anomaly detection.

Users can upload expense records in CSV format, explore spending patterns, analyze category-wise expenses, and identify potentially unusual transactions. The application provides meaningful financial insights through a clean, interactive interface.

## Features

- **Interactive Dashboard:** View expense summaries and key spending metrics.
- **Expense Analytics:** Analyze daily, monthly, and category-wise spending patterns.
- **Transaction Management:** Explore transaction records and apply filters.
- **CSV Upload:** Import expense data for analysis.
- **Data Visualization:** Understand spending trends through interactive charts and graphs.
- **Machine Learning Insights:** Use the Isolation Forest algorithm to identify potentially unusual transactions.
- **Expense Export:** Download analyzed transaction data where supported by the application.
- **User Authentication:** Access the application through its login and registration interface.
- **Responsive Interface:** Navigate the application through a modern, user-friendly design.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core application logic |
| Streamlit | Web application framework |
| Pandas | Data processing and analysis |
| NumPy | Numerical operations |
| Scikit-learn | Machine learning and anomaly detection |
| Isolation Forest | Identification of potentially unusual transactions |
| Plotly | Interactive charts and visualizations |
| CSV | Expense data import and export |

## Machine Learning Approach

SpendWise uses the **Isolation Forest** algorithm, an unsupervised machine learning technique for anomaly detection.

The algorithm identifies transactions that differ from typical patterns in the analyzed dataset. These transactions are flagged for further review.

The results represent potentially unusual spending activity and should not be interpreted as confirmed fraud.

## Application Workflow

1. Open the SpendWise application.
2. Sign in or create an account, depending on the configured authentication functionality.
3. Upload an expense CSV file or use sample data if available.
4. Explore expense summaries and transaction records.
5. Review category-wise and time-based visualizations.
6. Examine potentially unusual transactions identified by the machine learning model.
7. Apply available filters and export data where supported.

## Installation and Local Setup

### Prerequisites

- Python 3.10 or another version compatible with the project's dependencies
- Git
- pip

### 1. Clone the Repository

```bash
git clone https://github.com/Durga2343/Spendwise.git
```

### 2. Navigate to the Project Directory

```bash
cd Spendwise
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Application

If your main application file is `app.py`, execute:

```bash
streamlit run app.py
```

Streamlit will display a local URL in the terminal. Open that URL in your browser to access the application.

## Input Data

The application is designed to analyze expense records provided in CSV format.

Depending on the application's expected schema, records may include fields such as:

- Transaction date
- Transaction description
- Expense category
- Transaction amount

Use the column names and formats expected by the application. Invalid or incomplete input data may require correction before analysis.

## Deployment

SpendWise is deployed using Streamlit Community Cloud.

**Live Application:**  
https://durga2343-spendwise-app-sofwov.streamlit.app/

The deployment is connected to the GitHub repository. Updates pushed to the configured deployment branch can be reflected in the hosted application.

## Project Structure

```text
Spendwise/
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
```

The structure above illustrates the core files. Additional modules, assets, configuration files, or data files may exist in the actual repository.

## Security and Privacy

- Do not commit passwords, API keys, access tokens, or private configuration files.
- Keep sensitive configuration in environment variables or the deployment platform's secrets manager.
- Avoid committing real financial records or personal information.
- Ensure authentication and user-data access controls are properly configured before allowing multiple users.
- Use synthetic datasets for demonstrations and testing.

## Limitations

- Analysis depends on the quality and completeness of the uploaded data.
- Anomaly detection identifies unusual patterns; it does not establish fraud.
- Results depend on the dataset and the model configuration.
- The application analyzes provided expense records and does not imply direct bank or payment-app integration.

## Future Enhancements

- Advanced budgeting and savings recommendations
- Improved anomaly detection and explainability
- Custom spending limits and alerts
- Enhanced data export and reporting
- Secure multi-user data storage
- Additional financial trend analysis

## Author

**Durga Velumani**

Computer Science and Engineering Student

- GitHub: [Durga2343](https://github.com/Durga2343)
- LinkedIn: [Connect on LinkedIn](https://linkedin.com/in/durga-vb-616679340/)

## License

No license has been specified for this repository yet. Add a suitable open-source license if you intend to permit others to reuse, modify, or distribute the project.
