import re
import pandas as pd
import networkx as nx
import pandas as pd

import re
import csv

def process_text_file(input_file, output_file):
    # Read the input file
    with open(input_file, 'r') as file:
        input_text = file.read()

    output_lines = []

    citing_doi_pattern = re.compile(r'DI (10\.\d+/[^\s]+)')
    cited_doi_pattern = re.compile(r'DOI (10\.\d+/[^\s]+)')

    records = input_text.split('\nER\n')
    
    for record in records:
        print("Record found \n\n", record ,"\n\n")
        citing_match = citing_doi_pattern.search(record)
        if citing_match:
            print("Citing DOI found", citing_match.group(1))
            citing_doi = citing_match.group(1)
            cr_start = record.find('CR ')
            if cr_start != -1:
                print("CR found", cr_start)
                cr_section = record[cr_start + 3:]
                for line in cr_section.split('\n'):
                    cited_match = cited_doi_pattern.search(line)
                    if cited_match:
                        cited_doi = cited_match.group(1)
                        output_lines.append(f'{citing_doi}\t{cited_doi}')
            else:
                print("CR Not found")
        else:
            print("Citing DOI Not found")

    output_text = '\n'.join(output_lines)

    with open(output_file, 'w') as f:
        f.write('Citing Paper\tCited Paper\n') 
        f.write(output_text)


def citation_records():
# Main execution
    input_file = "alltime_1878_PageRank.txt"  # Replace with your input file name
    output_file = "citation_network_all_cr_dois.csv"

    process_text_file(input_file, output_file)


def compute_page_rank_scores():
    # Load the citation network from the CSV file
    df = pd.read_csv('citation_network_all_cr_dois.csv', sep='\t')

    # Create a directed graph from the citation data
    G = nx.from_pandas_edgelist(df, source='Citing Paper', target='Cited Paper', create_using=nx.DiGraph())

    # Compute the PageRank for each paper
    pagerank_scores = nx.pagerank(G, alpha=0.85)

    # Convert the PageRank results into a DataFrame
    pagerank_df = pd.DataFrame(list(pagerank_scores.items()), columns=['paper', 'pagerank_score'])

    # Sort the DataFrame by PageRank score in descending order
    pagerank_df = pagerank_df.sort_values(by='pagerank_score', ascending=False)

    # Save the PageRank scores to a CSV file
    pagerank_df.to_csv('pagerank_scores_all_cr.csv', index=False, quoting=csv.QUOTE_ALL)

    # Display the top 10 papers by PageRank score
    print(pagerank_df.head(10))

if __name__ == '__main__':
    citation_records()
    compute_page_rank_scores()