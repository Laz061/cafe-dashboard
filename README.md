# Cafe Sales Dashboard

This project is a web-based dashboard built with Streamlit to visualize and analyze customer feedback and sales data for a cafe chain. The application reads data from `data/CafeData.csv` and presents it in an interactive web interface.

## Features

*   Displays the raw sales and feedback data in a table.

## Getting Started

Follow these instructions to get a copy of the project up and running on your local machine.

### Prerequisites

Ensure you have Python 3.7+ installed on your system.

### Installation

1.  Clone the repository to your local machine.
2.  Navigate to the project directory:
    ```sh
    cd cafe-dashboard
    ```
3.  Create and activate a virtual environment (recommended):
    ```sh
    # Create a virtual environment
    python -m venv venv

    # Activate on Windows
    .\venv\Scripts\activate

    # Activate on macOS/Linux
    source venv/bin/activate
    ```
4.  Install the required packages from `requirements.txt`:
    ```sh
    pip install -r requirements.txt
    ```

### Running the Application

To run the Streamlit application, execute the following command in your terminal from the root directory of the project:

```sh
streamlit run app.py
```

The application will then be accessible in your web browser, typically at `http://localhost:8501`.