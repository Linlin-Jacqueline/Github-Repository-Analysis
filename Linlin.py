import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy.optimize import curve_fit


# Function to load data
def load_data():
    github_dataset = pd.read_csv('github_dataset.csv')
    # Remove '_count' suffix from columns
    github_dataset.columns = github_dataset.columns.str.replace('_count', '')
    github_dataset.drop_duplicates(inplace=True)  # Drop duplicate rows
    return github_dataset

def select_top_chart(github_dataset):

    # Dropdown to select repository attribute
    selected_option = st.selectbox('Select a category:', ['stars', 'forks', 'issues', 'pull_requests', 'contributors', 'language'])

    st.subheader(f'Top 10 Repositories by {selected_option.capitalize()} Count')

    if selected_option == 'language':
        plot_language_rank(github_dataset)  
    else:
        top_repo = github_dataset.nlargest(10, columns=selected_option)[['repositories', selected_option]]
        top_repo = top_repo.sort_values(by=selected_option, ascending=True)

        # Assigning different colors to bars based on repositories using 'tab20c' colormap
        colors = plt.cm.tab20c(np.linspace(0, 1, len(top_repo)))

        fig, ax = plt.subplots(figsize=(12, 6))
        for idx, (repo, count) in enumerate(zip(top_repo['repositories'], top_repo[selected_option])):
            ax.barh(repo, count, color=colors[idx])

        ax.set_xlabel('Count')
        ax.set_ylabel('Repository')
        plt.tight_layout()
        st.pyplot(fig)

    st.write("""
    This horizontal bar chart displays the top 10 repositories based on their stars, forks, issues, pull requests, contributors, and language count.
             
    The number of stars attributed to a repository is a measure of its popularity or perceived significance within the GitHub community.
    
    Forks in GitHub repositories are indicative of community involvement, interest, and the level of usage a project receives.
    
    Issues count indicates the number of reported problems, bugs, or suggested enhancements within the repository.
    
    Pull requests count reflects the number of times someone has proposed changes to a repository. It showcases how open the repository is to collaboration and contributions.
    
    A higher contributors count typically suggests a more diverse range of contributions, potentially representing a healthy and engaged community. 
    
    The language count identifies the technology stack and helps understand the tools and languages utilized.
    """)

# Function to plot Repository Activity Analysis
def plot_repository_activity(github_dataset):
    st.subheader('Repository Activity Analysis')

    activity_data = github_dataset[['stars', 'forks', 'issues', 'pull_requests']]
    activity_counts = activity_data.sum()

    plt.figure(figsize=(10, 6))
    activity_counts.plot(kind='bar', color='skyblue')
    plt.title('Count of Stars, Forks, Issues, and Pull Requests')
    plt.xlabel('Activity')
    plt.ylabel('Count')
    plt.xticks(rotation=45)
    plt.grid(True)
    st.pyplot()

    # Description
    st.write("""
    This bar chart shows the total count of stars, forks, issues, and pull requests across all repositories.
    It provides an overview of the activity level of the repositories.
    """)

def plot_language_rank(github_dataset):
    language_counts = github_dataset['language'].value_counts().nlargest(10)  
    language_counts = language_counts.sort_values(ascending=True)  

    # Assigning different colors to bars based on language counts using 'tab20c' colormap
    colors = plt.cm.tab20c(np.linspace(0, 1, len(language_counts)))

    fig, ax = plt.subplots(figsize=(10, 6))
    for idx, (language, count) in enumerate(language_counts.items()):
        ax.barh(language, count, color=colors[idx])
    ax.set_xlabel('Count')
    ax.set_ylabel('Language')
    plt.title('Top 10 Languages Used in Repositories')
    plt.tight_layout()
    st.pyplot(fig)



# Function to plot the distribution of stars
def plot_stars_distribution(github_dataset):
    st.subheader('Stars Distribution in GitHub Repositories')
    
    # 设置 pandas 默认选项
    with pd.option_context('mode.use_inf_as_null', True):
        plt.figure(figsize=(10, 6))
        sns.histplot(github_dataset['stars'], bins=30, kde=True)
        plt.title('Distribution of Stars Count in GitHub Repositories')
        plt.xlabel('Stars Count')
        plt.ylabel('Frequency')
        plt.grid(True)
        st.pyplot()
    
    # Description
    st.write("""
    This histogram illustrates the distribution of stars count across GitHub repositories. 
    
    Upon examining the distribution, it's evident that the majority of repositories fall within the range of 0 to 50 stars, 
    indicating a prevalence of repositories with comparatively lower star counts. However, as the star count increases, the frequency of repositories sharply decreases, 
    suggesting a rarity of repositories with higher star counts.
    
    Notably, there is a noticeable scarcity of repositories that have accumulated more than 400 stars, signifying a significant threshold where repositories garnering such high levels of recognition become less common.
    
    This distribution pattern indicates that while a considerable number of repositories exist with relatively lower star counts, repositories achieving a higher number of stars are more infrequent, 
    showcasing the selectivity and competitive nature of gaining substantial attention within the GitHub ecosystem.
    """)

# Function to plot the distribution of forks
def plot_forks_distribution(github_dataset):
    st.subheader('Forks Distribution in GitHub Repositories')
    plt.figure(figsize=(10, 6))
    sns.histplot(github_dataset['forks'], bins=30, kde=True)
    plt.title('Distribution of Forks Count in GitHub Repositories')
    plt.xlabel('Forks Count')
    plt.ylabel('Frequency')
    plt.grid(True)
    st.pyplot()

    # Description
    st.write("""
   This histogram showcases the distribution of fork counts among GitHub repositories. 
    
   The distribution pattern of fork counts mirrors that of the stars chart. A majority of GitHub repositories, over 700 in number, exhibit a range of stars between 0 to 50, suggesting a prevalent trend in the platform. Notably, there is a scarcity of repositories with fork counts exceeding 200.

   The similarity in distribution patterns between stars and forks signifies a common trend in repository engagement. This overlap in distributions might indicate a correlation between the level of interest in a repository, as depicted by stars, and the level of community engagement, often represented by forks.

   It's crucial to note that while high stars imply popularity or interest, high forks may signify active contribution and collaboration within the repository's community.

   This histogram offers valuable insights into the engagement levels and distribution patterns of forks across GitHub repositories, shedding light on the dynamics of community involvement within the platform.
    """)

# Function to plot Scatter Plot of Forks vs Stars
def func(x, a, b):
    return a * np.sqrt(x) + b  

def plot_forks_vs_stars(github_dataset):
    st.subheader('Scatter Plot of Forks vs Stars')
    scatter_fig = plt.figure(figsize=(10, 6))
    sns.scatterplot(x='forks', y='stars', data=github_dataset, label='Data Points')
    
    x_data = github_dataset['forks']
    y_data = github_dataset['stars']
    popt, _ = curve_fit(func, x_data, y_data)
    x_line = np.linspace(min(x_data), max(x_data), 100)
    y_line = func(x_line, *popt)
    plt.plot(x_line, y_line, 'r--', label='Curve Fit')  

    plt.title('Forks vs Stars in GitHub Repositories')
    plt.xlabel('Forks Count')
    plt.ylabel('Stars Count')
    plt.legend()
    plt.grid(True)
    st.pyplot(scatter_fig)

    # Description
    st.write("""
    This scatter plot presents the correlation between the counts of forks and stars across individual repositories. Additionally, it features a fitted curve, offering a visual representation of the relationship between these two variables.
             
    The majority of the data points are concentrated within the range of 0 to 200 for both stars and forks counts. Notably, these points predominantly overlap with the curve within this range. However, upon considering the overall distribution, most data points do not precisely align with the curve. This divergence suggests a potential lack of direct correlation between the number of stars and forks.
             
    Certain instances stand out, such as repositories with nearly 1000 stars yet exhibiting a minimal count of forks, or conversely, repositories with high fork counts but a significantly lower number of stars. These instances highlight the absence of a strict relationship between these attributes. This observation implies that a repository's popularity isn't solely contingent on its collaboration level. A repository completed by a single contributor might achieve substantial popularity, while a highly collaborative repository might not necessarily garner the same level of attention.
    
    In summary, this analysis suggests that while some repositories showcase aligned stars and forks counts, the broader trend among repositories indicates that the relationship between stars and forks is not consistently linear. Popularity and collaboration, as depicted by stars and forks counts, do not universally correlate, indicating that other factors significantly influence a repository's prominence and community engagement.
    """)

# Function to plot Bar Chart of Top 10 Repositories by Number of Stars & Forks
def plot_top_repo(github_dataset):
    st.subheader('The Forks Count For the Top 10 popular Repositories')

    top_repo = github_dataset.nlargest(10, columns=['stars', 'forks'])

    fig, ax1 = plt.subplots(figsize=(12, 6))

    ax1.bar(top_repo['repositories'], top_repo['stars'], color='b', alpha=0.7, label='Stars')
    ax1.set_xlabel('Repository')
    ax1.set_ylabel('Stars', color='b')
    ax1.tick_params('y', colors='b')
    ax1.set_xticklabels(top_repo['repositories'], rotation=45, ha='right')

    ax2 = ax1.twinx()
    ax2.plot(top_repo['repositories'], top_repo['forks'], color='r', marker='o', label='Forks')
    ax2.set_ylabel('Forks', color='r')
    ax2.tick_params('y', colors='r')

    fig.tight_layout()
    st.pyplot(fig)

    # Description
    st.write("""
    This chart represents the distribution of fork counts for the top 10 popular repositories. It's notable that the majority of these repositories exhibit lower fork counts. This observation suggests a potential area for enhancement in the community's overall activity level. To amplify community engagement, it becomes imperative for community managers to strategize and implement methods that encourage increased user contributions to repositories.

    The prevalence of repositories with lower fork counts among the top 10 suggests a certain limitation in community involvement or contributions. This scenario could be improved by fostering an environment that encourages collaboration, active participation, and contribution from users. Community managers could explore various initiatives such as organizing hackathons, conducting developer engagement programs, or creating documentation and guidelines that encourage contributions. Increasing user engagement is pivotal in nurturing a vibrant and thriving community ecosystem.

    A diversified and engaged community actively contributing to repositories can foster innovation, facilitate problem-solving, and enhance the overall growth and health of the GitHub community. Hence, focusing on strategies to enhance user contributions can significantly impact the activity and robustness of the entire community.
    """)



# Function to plot Contributor Analysis
def plot_contributor_analysis(github_dataset):

    contributors_data = github_dataset[['contributors', 'pull_requests', 'issues']]
    contributors_counts = contributors_data.sum()

    st.subheader('Number of Contributors:')
    st.text(contributors_counts['contributors'])

    st.subheader('Distribution of Contribution Types:')
    contribution_types = ['Pull Requests', 'Issues']
    contribution_counts = [contributors_counts['pull_requests'], contributors_counts['issues']]
    plt.figure(figsize=(8, 6))
    plt.pie(contribution_counts, labels=contribution_types, autopct='%1.1f%%', startangle=140)
    st.pyplot()

    # Description
    st.write("""
    This pie chart illustrates the distribution of contribution types, specifically pull requests and issues.
    It gives an overview of the contribution dynamics within the repositories. It can be seen from the chart that 66.9% of the contributions are from issues and 33.1% from pull requests.
    
    1. Project Activity and Issue Management: More contributions from issues might indicate that there are many users engaging with the project by reporting problems or suggesting improvements. It showcases project activity and community involvement. Developers need to address these issues, answer user queries, and fix bugs, which is crucial for the project's growth and health.

    2. Pull Request Contributions: Pull requests represent concrete contributions from users, including adding features, fixing bugs, etc. Even though the number of pull requests might be relatively less, it signifies some users' willingness to contribute technically to the project.

    3. Project Direction and Needs: An increase in issues might reflect users' expectations, needs, or identified problems with the project, requiring the project team to allocate more time and effort to handle and resolve these issues. Fewer pull requests might indicate that the project is still in a development phase, requiring more features or improvements to attract more developers.
    """)

# Function to plot Repository Feature Analysis
def plot_repository_feature_analysis(github_dataset):
    language_counts = github_dataset['language'].value_counts()
    plt.figure(figsize=(14, 8))  # Increase figure size
    language_counts.plot(kind='bar', color='lightgreen')
    plt.title('Distribution of Programming Languages')
    plt.xlabel('Programming Languages')
    plt.ylabel('Count')
    plt.xticks(rotation=90)  # Rotate x-axis labels to 90 degrees
    plt.grid(True)
    st.pyplot()
    
    # Description
    st.write("""
    This bar chart shows the distribution of programming languages used in the repositories.
    We can see that:
    
    JavaScript has the highest count, significantly more than any other language shown on the chart, suggesting that it is the most common or popular language among the data represented.

    Python comes next, with a count that is less than half of JavaScript's, but still considerably higher than the rest of the languages on the chart.

    HTML and CSS follow, indicating a good number of projects or usages. This makes sense given that these languages are foundational to web development, often used along with JavaScript.

    After the top four languages, there is a sharp drop-off in counts. Languages like C++, C, Java, TypeScript, and Ruby show moderate counts.

    Many languages on the chart have very low counts compared to the top languages, which could suggest they are less commonly used in the dataset being analyzed or they are specialized languages for specific domains.
    """)


# Function to plot Heatmap of Correlation Matrix
def plot_correlation_matrix(github_dataset):
    st.subheader('Correlation Matrix of GitHub Dataset')
    numeric_data = github_dataset[['stars', 'forks', 'issues', 'pull_requests', 'contributors']]
    correlation_matrix = numeric_data.corr()
    heatmap_fig = plt.figure(figsize=(8, 6))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
    plt.title('Correlation Matrix of GitHub Dataset')
    st.pyplot(heatmap_fig)

    # Description
    st.write("""
    This heatmap is created to gain a deeper insight into the correlation between different numerical variables in the GitHub dataset.
    It suggests that there are some positive relationships between the various metrics of GitHub repositories, with the number of contributors showing the most consistent positive correlation with other metrics. However, none of the correlations are very strong, which suggests that while there are tendencies, they are not necessarily indicative of a strong predictive relationship.
             
    Stars and forks have a positive correlation of 0.26, which means that repositories with more stars tend to have more forks, although the relationship is not very strong.

    Issues have a very low positive correlation with stars (0.06) and forks (0.13), indicating that the number of issues is not strongly related to the number of stars or forks.

    Pull requests show a moderate positive correlation with issues (0.31), suggesting that repositories with more issues tend to have more pull requests.

    Contributors have a positive correlation with forks (0.28) and a moderate positive correlation with issues (0.36) and pull requests (0.14), indicating that repositories with more contributors tend to have more forks, more issues, and slightly more pull requests.

    There are some very small negative correlations present (e.g., stars with pull requests at -0.0037), but these are so close to zero that they indicate no meaningful relationship.
    """)

# Streamlit app
def main():
    github_dataset = load_data()

    st.title('GitHub Repositories Analysis')
    st.markdown("""
    ###### Written by: Linlin Li
    ###### Contact: jacquelinlin7@outlook.com
    ---
    """)

    st.markdown("""
    <span style="color: red;">*You can navigate to different sections of this report by using the sidebar.*</span>
    """, unsafe_allow_html=True)
    st.write("""
    This report comprises three distinct sections. The initial segment delineates the activity levels exhibited by the GitHub repositories. The subsequent section provides insights into contributor distribution, while the final part delves into exploring correlations among the various features.
    """)

    navigation = st.sidebar.radio('Navigation', ['Repository Activity Analysis', 'Contributor Analysis', 'Repository Feature Analysis'])

    if navigation == 'Repository Activity Analysis':
        st.header('1. Repository Activity Analysis')
        select_top_chart(github_dataset)
        plot_repository_activity(github_dataset)
        plot_stars_distribution(github_dataset)
        plot_forks_distribution(github_dataset)
        
        plot_top_repo(github_dataset)
    elif navigation == 'Contributor Analysis':
        st.header('2. Contributor Analysis')
        plot_contributor_analysis(github_dataset)
    elif navigation == 'Repository Feature Analysis':
        st.header('3. Repository Feature Analysis')
        plot_repository_feature_analysis(github_dataset)
        plot_forks_vs_stars(github_dataset)
        plot_correlation_matrix(github_dataset)

st.set_option('deprecation.showPyplotGlobalUse', False)

# Call main function to run the app
if __name__ == '__main__':
    main()
