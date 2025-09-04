import transformers
from transformers import pipeline
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import os
import argparse
from transformers import logging

logging.set_verbosity_error()

pwd_path = "/home/sangbaek-lee/uploads"
model_path = "/home/sangbaek-lee/uploads/retrained_models/checkpoint-90"

if __name__ == "__main__":
    
    # Load the fine-tuned model and tokenizer
    file_path = os.path.join("models", "best_model")
    from transformers import pipeline

    # Step 1: Specify the path to your saved model checkpoint
    # Replace this with the actual path to your best checkpoint.
    # model_path = "./retrained_models/checkpoint-12902" # Example path

    # Step 2: Create a text-classification pipeline with your model
    # The pipeline will load everything it needs from this one directory.
    classifier = pipeline("text-classification", model=model_path, device=-1)

    file_path = f"{pwd_path}/transcript.txt"
    # Step 3: Use the pipeline to make predictions on new text
    with open(file_path, 'r') as file:
        text = file.readlines()

    # You can process a single sentence or a list of sentences
    results = classifier(text)
    # Step 4: Print the results
    print(results[0]['label'])
    
    # for text, result in zip([text1, text2], results):
    #     print(f"Text: '{text}'")
    #     print(f" -> Predicted Label: {result['label']}, Score: {result['score']:.4f}\n")