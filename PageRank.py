import re
import pandas as pd

# Step 1: Load the Web of Science data (replace with the path to your file)
with open('alltime_1878_PageRank.txt', 'r') as file:
    data = file.read()

# Step 2: Split the data into individual records (each record ends with 'ER')
records = data.split('ER\n')

# Step 3: Initialize lists to store citing and cited paper information
citing_papers = []
cited_papers = []

# Step 4: Loop through each record and extract the citing paper DOI and all cited paper DOIs
for record in records:
    # Extract the citing paper's DOI (DI field)
    paper_id_match = re.search(r'DI\s(.*)\n', record)
    if paper_id_match:
        citing_paper = paper_id_match.group(1).strip()

        # Extract all the cited references (CR field) and look for all DOIs
        references = re.findall(r'CR\s(.*)\n', record)
        
        # For each reference, find all DOI matches
        for ref in references:
            # Find all DOI patterns in the reference string
            doi_matches = re.findall(r'(10\.\d{4,9}/[-._;()/:A-Z0-9]+)', ref, re.IGNORECASE)
            
            # Add each DOI match as a cited paper
            for doi in doi_matches:
                cited_paper = doi.strip()
                citing_papers.append(citing_paper)
                cited_papers.append(cited_paper)

# Step 5: Create a DataFrame to store the citing-cited pairs
df = pd.DataFrame({
    'citing_paper': citing_papers,
    'cited_paper': cited_papers
})

# Step 6: Save the DataFrame to a CSV file for further analysis
df.to_csv('citation_network_all_cr_dois.csv', index=False)

# Display the first few rows of the DataFrame to verify
print(df.head())

import networkx as nx
import pandas as pd

# Step 1: Load the citation network from the CSV file
df = pd.read_csv('citation_network_all_cr_dois.csv')

# Step 2: Create a directed graph from the citation data
G = nx.from_pandas_edgelist(df, source='citing_paper', target='cited_paper', create_using=nx.DiGraph())

# Step 3: Compute the PageRank for each paper
pagerank_scores = nx.pagerank(G, alpha=0.85)

# Step 4: Convert the PageRank results into a DataFrame
pagerank_df = pd.DataFrame(list(pagerank_scores.items()), columns=['paper', 'pagerank_score'])

# Step 5: Sort the DataFrame by PageRank score in descending order
pagerank_df = pagerank_df.sort_values(by='pagerank_score', ascending=False)

# Step 6: Save the PageRank scores to a CSV file
pagerank_df.to_csv('pagerank_scores_all_cr.csv', index=False)

# Display the top 10 papers by PageRank score
print(pagerank_df.head(10))