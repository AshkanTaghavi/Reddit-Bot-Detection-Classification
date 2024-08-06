# AWS - Reddit Bot Detection and Classification

**San Luis Obispo, CA**\
**Cloud Services Analytics Project**\
**January 2024**

## Project Overview

This project involves analyzing user activity on the Reddit community 'r/place' to detect and classify bots. 'r/place' was a public subreddit where users collaboratively placed pixels on a digital canvas to create a communal piece of artwork. The goal of this project is to understand the impact of bot activity on the creation of this artwork.

## Key Features

### Data Processing with AWS

-   **S3 and AWS Glue:** Orchestrated end-to-end data processing workflows for ETL tasks, including data segmentation and Parquet transformation. This optimized efficiency and scalability for a complex dataset of 135 million rows.

-   **AWS SageMaker and Python:** Utilized for detailed analysis and crafting metrics to classify users as bots. This revealed insights into bot impact on artwork, pixel placement, and contribution trends.

## Project Structure

-   **data/**: Contains raw and processed data files.

-   **scripts/**: Python scripts for data processing, analysis, and classification.

-   **notebooks/**: Jupyter notebooks with exploratory data analysis and model training.

-   **output/**: Results and visualizations from the analysis.

-   **README.md**: Project overview and documentation.

## Setup and Usage

### Prerequisites

-   AWS account with S3, Glue, and SageMaker services enabled.

-   Python 3.x environment with required libraries (see `requirements.txt`).

### Data Processing

1.  **Upload Data**: Upload raw data to an S3 bucket.

2.  **AWS Glue**: Set up Glue jobs for data segmentation and Parquet transformation.

3.  **Run ETL Jobs**: Execute the ETL workflows to process the data.

### Analysis and Classification

1.  **Python Scripts**: Use the provided scripts in the `scripts/` directory for data analysis and bot classification.

2.  **SageMaker Notebooks**: Open and run the Jupyter notebooks in the `notebooks/` directory for detailed analysis and visualization.

## Results

The analysis provided insights into how bots interacted with the 'r/place' artwork, including:

-   The extent of bot contributions to pixel placements.

-   Patterns and trends in bot activity compared to human users.

-   The overall impact of bots on the collaborative artwork.
