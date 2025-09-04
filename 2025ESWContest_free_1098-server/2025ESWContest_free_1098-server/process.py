import json
import re

def process_and_combine_files(text_filename: str, idx_filename: str, output_filename: str):
    """
    Reads a text file of dialogues and a corresponding text file of indices,
    matches them, and saves the combined data to a structured JSON file.

    Args:
        text_filename: The path to the file with dialogue text.
        idx_filename: The path to the file with indices.
        output_filename: The name of the final JSON file to create.
    """
    # 1. Process the TEXT file into a flat list of utterances
    print(f"Reading and processing '{text_filename}'...")
    with open(text_filename, 'r', encoding='utf-8') as f:
        full_text_content = f.read()

    # Clean the text: remove [source] tags and newlines
    text_no_source = re.sub(r'\'', '', full_text_content)
    cleaned_text_block = text_no_source.replace('\n', ' ')

    # Split into utterances and filter out empty strings
    all_utterances = [
        utterance.strip() for utterance in cleaned_text_block.split('__eou__') if utterance.strip()
    ]

    # 2. Process the INDEX file into a flat list of integers
    print(f"Reading and processing '{idx_filename}'...")
    with open(idx_filename, 'r', encoding='utf-8') as f:
        full_idx_content = f.read()

    all_indices = []
    for line in full_idx_content.strip().split('\n'):
        all_indices.extend([int(num) for num in line.split()])

    # 3. Sanity Check: Ensure the number of texts matches the number of indices
    num_utterances = len(all_utterances)
    num_indices = len(all_indices)
    print(f"Found {num_utterances} utterances and {num_indices} indices.")

    if num_utterances != num_indices:
        print("⚠️ Error: The number of texts does not match the number of indices!")
        print("Please check your input files. Aborting.")
        return

    # 4. Combine the data into a new list of dictionaries
    print("Matching text to idx...")
    combined_data = {"conversation": [] }
    for i in range(num_utterances):
        combined_data['conversation'].append({
            "text": all_utterances[i],
            "SpeakerEmotionTarget": all_indices[i]
        })

    # 5. Save the final combined data to a JSON file
    print(f"Saving combined data to '{output_filename}'...")
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(combined_data, f, ensure_ascii=False, indent=4)

    print(f"Successfully created '{output_filename}'! ✅")


# --- Main execution ---
if __name__ == "__main__":
    process_and_combine_files(
        text_filename='ijcnlp_dailydialog/test/dialogues_test.txt',
        idx_filename='ijcnlp_dailydialog/test/dialogues_emotion_test.txt',
        output_filename='dialogues_dataset.json'
    )