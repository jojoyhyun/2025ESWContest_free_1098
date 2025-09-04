import torch
import evaluate
import numpy as np
import data_loader
from datasets import load_dataset, Dataset
from transformers import pipeline



from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    TrainingArguments,
    Trainer
)

# -----------------------------------------------------------------------------
# Step 1: Load a Multi-Class Dataset 📰
# -----------------------------------------------------------------------------
# We'll use the KLUE benchmark's Topic Classification (TC) task.
# This dataset classifies news headlines into 7 topics.
print("➡️ Step 1: Loading dataset...")

# 0: no emotion, 1: anger, 2: disgust, 3: fear, 4: happiness, 5: sadness, 6: surprise
# dataset for dailydialog
data_load = data_loader.data_loader(num_labels=7, unique_classes={0:'no_emotion', 1:'anger',2: 'disgust',\
                                                                  3:'fear',4: 'happiness',5: 'sadness',6: 'surprise'})
file_path = 'translated_dataset.json'

# dataset = data_load.load_all_files_in_folder(file_path)
dataset = data_load.load_sentiment_data(file_path)

text = [item[0] for item in dataset]
labels = [item[1] for item in dataset]

# Let's see what the data looks like
print("\nSample from training data:")
print(dataset[0][0])

# -----------------------------------------------------------------------------
# Step 2: Prepare Labels and Mappings 🏷️
# -----------------------------------------------------------------------------
# The most crucial step for multi-class classification!
# We need to tell the model how many labels there are and what they mean.
print("\n➡️ Step 2: Preparing labels...")
num_labels = data_load.num_labels
class_names = data_load.unique_classes

# Create mappings from integer ID to label name and vice versa
id2label = {i: name for i, name in enumerate(class_names)}
label2id = {name: i for i, name in enumerate(class_names)}

print(f"\nNumber of labels: {num_labels}")
print(f"Label names: {class_names}")
print(f"ID to Label mapping: {id2label}")

# -----------------------------------------------------------------------------
# Step 3: Preprocessing and Tokenization ⚙️
# -----------------------------------------------------------------------------
# We'll use a pre-trained model suitable for the KLUE benchmark.
print("\n➡️ Step 3: Tokenizing dataset...")

sentiment_model = pipeline(task = "sentiment-analysis",
                           model="WhitePeak/bert-base-cased-Korean-sentiment")

model_name = "WhitePeak/bert-base-cased-Korean-sentiment"
tokenizer = AutoTokenizer.from_pretrained(model_name)

tokenized_dataset = tokenizer(
    text,
    padding=True,
    truncation=True,
    max_length=128,
)

numeric_labels = [label2id[label] for label in labels]

# Step 3: Create a Hugging Face Dataset object
# The keys "text" and "label" will become the column names.
raw_dataset = Dataset.from_dict({
    "text": text,
    "label": numeric_labels # Use the numeric labels
})

print("--- Initial Dataset ---")
print(raw_dataset)
print(raw_dataset[0])

def tokenize_function(examples):
    # The tokenizer will operate on the "text" column of the dataset.
    return tokenizer(examples["text"], padding="max_length", truncation=True, max_length=128)

# Step 5: Apply the tokenizer to the entire dataset using .map()
# This is highly efficient as it processes multiple examples at once (batched=True).
tokenized_dataset = raw_dataset.map(tokenize_function, batched=True)

# Step 6: Remove the original "text" column as it's no longer needed
tokenized_dataset = tokenized_dataset.remove_columns(["text"])

# Step 7: Rename the "label" column to "labels"
# The Trainer API specifically looks for a column named "labels".
tokenized_dataset = tokenized_dataset.rename_column("label", "labels")

# Step 8: Set the format to PyTorch tensors
# This prepares the dataset to output torch.Tensor objects, ready for the model.
tokenized_dataset.set_format("torch")

print("\n--- Final Trainable Dataset ---")
print(tokenized_dataset)
print(tokenized_dataset[0])

print("Tokenization complete.")

# -----------------------------------------------------------------------------
# Step 4: Load the Pre-trained Model 🤖
# -----------------------------------------------------------------------------
# Load the base model, but configure it for our specific multi-class task.
print("\n➡️ Step 4: Loading pre-trained model for fine-tuning...")

model = AutoModelForSequenceClassification.from_pretrained(
    model_name,
    num_labels=num_labels,
    id2label=id2label,
    label2id=label2id,
    ignore_mismatched_sizes=True
)

model.to(device="cuda")
# -----------------------------------------------------------------------------
# Step 5: Define Training Arguments and Metrics 📊
# -----------------------------------------------------------------------------
print("\n➡️ Step 5: Defining training arguments...")
# We'll use accuracy to measure performance.
accuracy_metric = evaluate.load("accuracy")

def compute_metrics(eval_pred):
    predictions, labels = eval_pred
    predictions = np.argmax(predictions, axis=1) # Get the class with the highest score
    return accuracy_metric.compute(predictions=predictions, references=labels)

# Set up the training parameters
training_args = TrainingArguments(
    output_dir="./retrained_models",
    learning_rate=3e-5,
    per_device_train_batch_size=32,
    per_device_eval_batch_size=32,
    num_train_epochs=50, # Use 1-2 epochs for a quick demonstration
    weight_decay=0.01,
    eval_strategy="epoch",
    save_strategy="epoch",
    load_best_model_at_end=True,
)

# -----------------------------------------------------------------------------
# Step 6: Create the Trainer and Start Training 🚀
# -----------------------------------------------------------------------------
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset,
    eval_dataset=tokenized_dataset, # Use the validation set for evaluation
    tokenizer=tokenizer,
    compute_metrics=compute_metrics,
)

print("\n➡️ Step 6: Starting model training...")
trainer.train()
print("🎉 Training complete!")

# -----------------------------------------------------------------------------
# Step 7: Test Your New Model! ✨
# -----------------------------------------------------------------------------
print("\n➡️ Step 7: Testing the fine-tuned model...")
