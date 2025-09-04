import json
import os
import glob


class data_loader():
    def __init__(self, num_labels=0, unique_classes=None):
        self.num_labels = num_labels
        self.unique_classes = unique_classes
    
    def load_sentiment_data(self, file_path):
        """
        Loads and extracts sentiment data from a specific JSON format.
        Args:
            file_path (str): The full path to the JSON file.

        Returns:
            list: A list of tuples, where each tuple contains (text, emotion_label).
                Returns an empty list if the file is not found or is invalid.
        """
        # Check if the file exists before trying to open it
        if not os.path.exists(file_path):
            print(f"Error: The file '{file_path}' was not found.")
            return []

        try:
            # Open and load the JSON data from the file
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Initialize a list to store our processed data
            sentiment_pairs = []

            # The core data is inside the 'Conversation' list
            conversation_log = data.get("Conversation", [])
            if not conversation_log:
                print("Warning: 'Conversation' key not found or is empty in the JSON file.")
                return []

            # Loop through each entry in the conversation
            for entry in conversation_log:
                # Extract the text and the target emotion
                text = entry["text"]
                emotion_label = entry["SpeakerEmotionTarget"]

                # Ensure both fields exist before adding them
                if text and emotion_label:
                    sentiment_pairs.append((text, emotion_label))

            return sentiment_pairs

        except json.JSONDecodeError:
            print(f"Error: The file '{file_path}' is not a valid JSON file.")
            return []
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return []
        
    def load_all_files_in_folder(self, folder_path='VL_01.실내'):
        """
        Finds all JSON files in a folder and extracts sentiment data from them.

        Args:
            folder_path (str): The path to the folder containing the JSON files.

        Returns:
            list: A list containing all (text, emotion_label) tuples from all files.
        """
        # Check if the folder exists
        if not os.path.isdir(folder_path):
            print(f"Error: The folder '{folder_path}' does not exist.")
            return []

        # Use glob to find all files ending with .json in the specified folder
        # The pattern folder_path + '/*.json' means "all files ending in .json inside folder_path"
        json_files = glob.glob(os.path.join(folder_path, '*.json'))

        if not json_files:
            print(f"No .json files were found in the folder '{folder_path}'.")
            return []
        
        print(f"Found {len(json_files)} JSON files. Starting to process...\n")
        
        # This list will hold all the data from all the files
        all_data = []

        # Loop through each file found
        for file_path in json_files:
            print(f"Processing: {os.path.basename(file_path)}")
            # Load the data from the current file
            data_from_file = self.load_sentiment_data(file_path)
            # Add the loaded data to our master list
            if data_from_file:
                all_data.extend(data_from_file)
                
        all_labels = [label for text, label in all_data]

        self.unique_classes = list(set(all_labels))
        self.num_labels = len(self.unique_classes)
        return all_data

    # --- Example Usage ---
    def verification(self):
        # 1. Specify the path to your folder.
        #    Using '.' means "the current folder where the script is running".
        folder_to_load = 'VL_01.실내'

        # 2. Load the data from all files in that folder
        total_loaded_data = self.load_all_files_in_folder(folder_to_load)

        all_labels = [label for text, label in total_loaded_data]

        # 3. Verify the loaded data
        if total_loaded_data:
            print(f"\n✅ Success! Finished processing all files.")
            print(f"Total data pairs extracted: {len(total_loaded_data)}\n")

            # Print the first 5 entries as a sample
            print("--- Sample of Extracted Data ---")
            for i, (text, label) in enumerate(total_loaded_data[:5]):
                print(f"Entry {i+1}: Text='{text}', Emotion='{label}'")
        else:
            print("\nNo data was loaded from the specified folder.")