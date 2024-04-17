import os
import spacy

# Load English tokenizer, tagger, parser, NER and word vectors
nlp = spacy.load("en_core_web_sm")


def get_location(file_path):
    with open(file_path, 'r') as file:
        data = file.read()
        doc = nlp(data)
        locations = [entity.text for entity in doc.ents if entity.label_ == "GPE"]
        return locations


def analyze_files_in_folder(folder_path):
    for subdir, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.txt'):
                file_path = subdir + os.sep + file
                locations = get_location(file_path)
                if locations:
                    print(locations)
                    return locations[0]


# Call the function with the path to your folder
analyze_files_in_folder("scraped_data")
