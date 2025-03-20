# GitHub Repositories Analysis

## Overview
This Streamlit application provides an interactive analysis of GitHub repositories, offering insights into repository activity, contributor distribution, and feature correlations. The app visualizes key metrics such as stars, forks, issues, pull requests, contributors, and programming languages used in GitHub repositories.

## Features
### 1. Repository Activity Analysis
- **Top 10 Repositories by Stars, Forks, Issues, Pull Requests, Contributors, or Language**
- **Repository Activity Overview**: Displays total counts of stars, forks, issues, and pull requests.
- **Stars and Forks Distribution**: Histograms illustrating the distribution of stars and forks across repositories.
- **Top 10 Popular Repositories**: Shows a bar chart of the most starred repositories and their fork counts.

### 2. Contributor Analysis
- **Contributor Count**: Displays the total number of contributors across repositories.
- **Distribution of Contribution Types**: Pie chart showing the proportion of pull requests and issues as contribution types.

### 3. Repository Feature Analysis
- **Language Distribution**: Bar chart showing the most used programming languages across repositories.
- **Forks vs. Stars Correlation**: Scatter plot with a fitted curve showing the relationship between forks and stars.
- **Correlation Matrix**: Heatmap visualizing the correlation between different GitHub metrics.

## Installation
To run the app locally, follow these steps:

### Prerequisites
Ensure you have Python installed (preferably 3.7 or later). Install required dependencies using:

```bash
pip install streamlit pandas matplotlib seaborn numpy scipy
```

### Running the App
1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/github-analysis.git
   cd github-analysis
   ```
2. Ensure you have the dataset `github_dataset.csv` in the project directory.
3. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

## How to Use
1. **Start the App**: Launch the application using the command above.
2. **Navigate through Sections**: Use the sidebar to explore different analysis sections.
3. **Interact with the Visualizations**: Select categories and filters to dynamically update charts.

## Dataset
The dataset `github_dataset.csv` should contain columns such as:
- `repositories`: Repository name
- `stars`: Star count
- `forks`: Fork count
- `issues`: Issue count
- `pull_requests`: Pull request count
- `contributors`: Number of contributors
- `language`: Programming language

Ensure the dataset is properly formatted to avoid issues while loading.

## Contact
- **Author**: Linlin Li
- **Email**: jacquelinlin7@outlook.com

## License
This project is open-source and available under the MIT License.

