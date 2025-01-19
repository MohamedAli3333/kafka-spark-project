# kafka-spark-project
# Bank Data Processing with Kafka, Spark, and SQL

This project demonstrates a real-time data processing pipeline for bank transactions. The pipeline leverages Apache Kafka, Apache Spark, and SQL to process data and compute the total number of deposits and withdrawals.

## Project Overview

The main goal of this project is to:

1. **Ingest** bank transaction data using Apache Kafka.
2. **Process** the data using Apache Spark.
3. **Analyze** the data using SQL to calculate:
   - The total number of deposits.
   - The total number of withdrawals.

## Key Components

### 1. Apache Kafka
- **Purpose**: Acts as a message broker to ingest and stream bank transaction data in real time.
- **Setup**:
  - Create a Kafka topic (e.g., `bank-transactions`).
  - Produce sample transaction data to this topic. Each message should contain:
    ```json
    {
      "account_no": "<account_number>",
      "date": "<transaction_date>",
      "transaction_details": "<details>",
      "value_date": "<value_date>",
      "withdraw": <amount_withdrawn>,
      "deposit": <amount_deposited>,
      "balance": <current_balance>
    }
    ```

### 2. Apache Spark
- **Purpose**: Processes streaming data from Kafka.
- **Features**:
  - Consumes messages from the Kafka topic.
  - Parses and transforms the data for analysis.
  - Writes processed data to a storage layer or directly queries it with SQL.

### 3. SQL for Analysis
- **Purpose**: Analyzes the processed data to compute the required metrics.
- **Queries**:
  - Total number of deposits:
    ```sql
    SELECT COUNT(*) AS total_deposits FROM transactions WHERE deposit > 0;
    ```
  - Total number of withdrawals:
    ```sql
    SELECT COUNT(*) AS total_withdrawals FROM transactions WHERE withdraw > 0;
    ```

## Installation and Setup

### Prerequisites
- Apache Kafka
- Apache Spark
- Java 8 or later
- Python 3.x
- A SQL engine (e.g., Spark SQL, PostgreSQL)

### Steps

1. **Kafka Setup**:
   - Install and configure Kafka.
   - Start Zookeeper and Kafka brokers.
   - Create a topic named `bank-transactions`.

2. **Spark Setup**:
   - Install Spark.
   - Configure Spark to connect to Kafka using the Spark-Kafka connector.

3. **Run the Application**:
   - Start the Kafka producer to send transaction data.
   - Execute the Spark job to process and store the data.
   - Use SQL queries to analyze the results.

## Example Dataset

| Account No | Date       | Transaction Details            | Value Date  | Withdraw | Deposit   | Balance   |
|------------|------------|--------------------------------|-------------|----------|-----------|-----------|
| 4090006110 | 29-Jun-17  | TRF FROM Indiaforensic         | 29-Jun-17   |          | 500.00    | ######### |
| 4090006110 | 5-Jul-17   | TRF FROM Indiaforensic         | 5-Jul-17    |          | 500.00    | ######### |
| 4090006110 | 16-Aug-17  | FDRL/INTERNAL FUND T           | 16-Aug-17   | 133,900  |           | ######### |
| 4090006110 | 16-Aug-17  | INDO GIBL Indiaforensic        | 16-Aug-17   |          | 331,650.00| ######### |

## Results

### Sample Output

- Total Deposits: 10
- Total Withdrawals: 5

## Future Enhancements

- Add support for advanced analytics (e.g., transaction trends over time).
- Integrate a dashboard for real-time visualization.
- Enhance fault tolerance and scalability.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
