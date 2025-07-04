from transformers import pipeline

# Load the NER pipeline with aggregation for grouped entities
ner_pipeline = pipeline(
    "ner",
    model="dbmdz/bert-large-cased-finetuned-conll03-english",
    aggregation_strategy="average"  # or "simple", "first", "max"
)

def extract_entities(text: str):
    """
    Extract named entities from the given text.
    Returns a list of dicts: [{entity_group, word, start, end, score}, ...]
    """
    return ner_pipeline(text)
