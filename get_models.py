import os
import json
import requests
import argparse

def download_file(url, output_path):
	try:
		# Check if the file already exists
		if os.path.exists(output_path):
			print(f"File already exists, skipping: {output_path}")
			return
		
		response = requests.get(url, stream=True)
		response.raise_for_status()

		with open(output_path, 'wb') as f:
			for chunk in response.iter_content(chunk_size=8192):
				if chunk:
					f.write(chunk)
		print(f"Downloaded: {url} -> {output_path}")
	except Exception as e:
		print(f"Failed to download {url}: {e}")

def main(json_file, output_dir):
	# Ensure output directory exists
	if not os.path.exists(output_dir):
		os.makedirs(output_dir)

	# Read the JSON file
	with open(json_file, 'r') as f:
		data = json.load(f)

	# Iterate over the entries in the JSON file
	for entry in data:
		folder = entry.get("folder")
		files = entry.get("files", [])

		# Ensure subfolder exists
		folder_path = os.path.join(output_dir, folder)
		if not os.path.exists(folder_path):
			os.makedirs(folder_path)

		# Process each file entry
		for file_entry in files:
			if isinstance(file_entry, str):
				# If it's a URL string, use the basename of the URL as the filename
				url = file_entry
				filename = os.path.basename(url)
			elif isinstance(file_entry, dict):
				# If it's a dict, use the 'url' and 'path' from the JSON
				url = file_entry.get("url")
				filename = file_entry.get("path")
			else:
				print(f"Skipping invalid file entry: {file_entry}")
				continue

			output_path = os.path.join(folder_path, filename)
			download_file(url, output_path)

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Download files from a JSON file.")
	parser.add_argument("json_file", help="Path to the JSON file containing URLs and filenames.")
	parser.add_argument("output_dir", help="Directory to save the downloaded files.")
	
	args = parser.parse_args()
	
	main(args.json_file, args.output_dir)
