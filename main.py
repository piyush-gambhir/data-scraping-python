# import pandas as pd
# from multiprocessing import Pool

# # Load your provider identification helper function
# from scrapers.dealership_website_providers.dealership_website_provider_identification import identify_dealer_provider
# from urllib.parse import urlparse

# # Load the CSV file
# file_path = './dealer_list.csv'
# data = pd.read_csv(file_path)

# # Print column names to verify
# print("Column names in CSV:", data.columns)

# # Check if 'Dealer_Website' is the actual column name
# if 'Dealer_Website' not in data.columns:
#     raise ValueError(
#         "The 'Dealer_Website' column does not exist. Please check the column names in your CSV file."
#     )

# # Function to validate and clean URLs


# def clean_url(url):
#     parsed_url = urlparse(url)
#     if not parsed_url.scheme:
#         # If no scheme (http/https), add https
#         url = 'https://' + url
#     return url

# # Function to process a single row in the dataframe


# def process_row(row):
#     website = row['Dealer_Website']
#     website = clean_url(website)  # Clean and validate the URL

#     provider = None
#     try:
#         print(f"Processing {website}")
#         provider = identify_dealer_provider(website)
#     except Exception as e:
#         print(f"Error processing {website}: {e}")
#     return provider

# # Function to save chunks incrementally


# def save_chunk(data_chunk, file_path, mode='a'):
#     # Save the chunk to the file; append mode ('a') except for the first chunk, which overwrites
#     header = mode == 'w'
#     data_chunk.to_csv(file_path, mode=mode, index=False, header=header)


# # Use multiprocessing for parallel execution
# if __name__ == '__main__':
#     chunk_size = 100  # Save after processing every 100 rows
#     num_rows = len(data)
#     processed_data = []

#     with Pool() as pool:
#         for start in range(0, num_rows, chunk_size):
#             chunk = data.iloc[start:start + chunk_size]  # Get the chunk
#             chunk['scrapped_provider'] = pool.map(
#                 # Process chunk
#                 process_row, [row for _, row in chunk.iterrows()])

#             # Save the chunk incrementally
#             # 'w' for the first chunk, 'a' for the rest
#             save_mode = 'w' if start == 0 else 'a'
#             save_chunk(chunk, file_path, mode=save_mode)

#     print(f"Updated CSV saved to {file_path}")


from scrapers.vehicle_maketplaces.cars_dot_com.cars_dot_com_istings import main as cars_com_main


if __name__ == "__main__":
    cars_com_main()
