import pandas as pd

# Load all uploaded CSVs into dataframes
ansira_df = pd.read_csv('./Ansira.net.csv')
dealer_com_df = pd.read_csv('./Dealer.Com.csv')
auto_corner_df = pd.read_csv('./Auto_Corner.csv')
dealer_inspire_df = pd.read_csv('./Dealer_Inspire.csv')

# Combine website and provider information from all files into one DataFrame
website_data = []

# Extracting relevant columns: Dealer_Website and Website Provider
if 'Dealer_Website' in ansira_df.columns and 'Website Provider' in ansira_df.columns:
    website_data.extend(
        ansira_df[['Dealer_Website', 'Website Provider']].dropna().values.tolist())

if 'Dealer_Website' in dealer_com_df.columns and 'Website Provider' in dealer_com_df.columns:
    website_data.extend(
        dealer_com_df[['Dealer_Website', 'Website Provider']].dropna().values.tolist())

if 'Dealer_Website' in auto_corner_df.columns and 'Website Provider' in auto_corner_df.columns:
    website_data.extend(
        auto_corner_df[['Dealer_Website', 'Website Provider']].dropna().values.tolist())

if 'Dealer_Website' in dealer_inspire_df.columns and 'Website Provider' in dealer_inspire_df.columns:
    website_data.extend(
        dealer_inspire_df[['Dealer_Website', 'Website Provider']].dropna().values.tolist())

# Combine into one DataFrame for processing
website_df = pd.DataFrame(website_data, columns=[
                          'Dealer_Website', 'Website Provider'])

# Save the combined DataFrame to a CSV file
website_df.to_csv('combined_dealer_websites.csv', index=False)
