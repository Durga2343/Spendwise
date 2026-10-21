# SpendWise — Smart Expense Analyzer

## Project Description
SpendWise is a privacy-first, machine learning-powered personal expense analysis web application. It helps users track their spending habits, visualize expenses across categories, and detect unusual spending patterns using an Isolation Forest anomaly detection model. The application operates entirely locally, ensuring that no financial data is ever shared or uploaded to the cloud.

## Features
- **Interactive Dashboards**: Built with Streamlit and Plotly for deep insights.
- **Machine Learning Integration**: Uses Scikit-learn's Isolation Forest to flag unusual expenses.
- **High-Performance Caching**: Uses `@st.cache_data` for instant sub-millisecond page transitions and data parsing.
- **Premium UI Design**: High-contrast, tailored fintech design system with emerald, sage, cream, and forest accents.
- **File Upload & Parsing**: Allows users to upload their own CSV expenses or manually enter them.
- **Privacy First**: No APIs, no banking integrations, 100% local processing.
- **Complete Viva Voce PDF Guide**: 10-page master technical defense guide with 30+ Q&As (`SpendWise_Complete_Viva_Guide.pdf`).

## Technologies Used
- Python 3.10+
- Streamlit (Web UI Framework)
- Pandas & NumPy (Data Processing)
- Plotly (Data Visualization)
- Scikit-learn (Machine Learning Anomaly Detection)
- ReportLab (PDF Documentation Generation)


---

## Installation Instructions (Windows)

1. **Open PowerShell or Command Prompt** and navigate to the project directory:
   ```cmd
   cd SpendWise
   ```

2. **Create a Virtual Environment**:
   ```cmd
   python -m venv venv
   ```

3. **Activate the Environment**:
   ```cmd
   .\venv\Scripts\activate
   ```

4. **Install Dependencies**:
   ```cmd
   pip install -r requirements.txt
   ```

5. **Run the Application**:
   ```cmd
   streamlit run app.py
   ```

---

## Viva Preparation Document

### 1. What is Expense Analysis?
Expense analysis is the process of reviewing and tracking spending to understand where money is going. By categorizing expenses, a user can visualize trends and identify opportunities to save.

### 2. What does Data Visualization mean?
Data visualization represents data points graphically (charts, graphs). In SpendWise, Plotly translates raw expense rows into understandable trends, like the "Expense by Category" donut chart or "Monthly Spend" area chart.

### 3. What is an Anomaly?
An anomaly (or outlier) is an observation that deviates significantly from the normal pattern of the dataset.

### 4. What is Machine Learning Anomaly Detection?
It's the use of algorithms to automatically learn normal patterns in data without explicit rules. When new data arrives, the algorithm can calculate how different it is from the norm.

### 5. How does Isolation Forest work?
Isolation Forest is an unsupervised machine learning algorithm. It 'isolates' observations by randomly selecting a feature and then randomly selecting a split value. Since anomalies are sparse and different, they are isolated quicker (require fewer splits) than normal observations.

### 6. What does "Contamination" mean?
In Isolation Forest, 'contamination' is a hyperparameter indicating the expected proportion of outliers in the dataset. We set it low (e.g., 0.05 or 5%) to avoid flagging too many ordinary transactions.

### 7. Why is an unusual expense not necessarily fraud?
An unusual expense simply breaks the historical mathematical pattern (e.g., buying a laptop when you normally just buy groceries). It doesn't mean someone stole your card; it just means it's mathematically anomalous.

### 8. How is CSV data loaded and cleaned?
We use Python's `pandas` library. `pd.read_csv()` loads the data. We standardize column names using `.str.lower()`, rename common aliases (like 'merchant' to 'description'), and convert text dates and string amounts to proper Python datetime objects and numeric floats using `pd.to_datetime()` and `pd.to_numeric()`.

### 9. How is each graph calculated?
We group the data using Pandas `.groupby()`. For example, `df.groupby('category')['amount'].sum()` calculates the total spent per category, which is then fed into `px.pie()` (Plotly Express pie chart).

### 10. How does the UI connect to the Python backend?
Streamlit is the bridge. It lets us write pure Python scripts where UI elements (`st.plotly_chart`, `st.metric`) automatically reflect the Python variables and DataFrames. When a user changes a filter, the script re-runs from top to bottom with the new filter values.

## Limitations
- Small datasets (< 20 rows) disable the ML model to prevent overfitting or wildly inaccurate predictions.
- The Isolation Forest model relies primarily on the amount; future enhancements could include complex time-series pattern recognition.
