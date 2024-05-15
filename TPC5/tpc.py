import spacy

nlp = spacy.load("pt_core_news_lg")
text = """O Daniel e o André foram a Ponte de Lima a pé."""
doc = nlp(text)

print("{:<15} | {:<15} | {:<15}".format("Word", "POS_", "Lemma"))

for token in doc:
    print("{:<15} | {:<15} | {:<15}".format(token.text, token.pos_, token.lemma_))

for entity in doc.ents:
    print("{:<15} | {:<15} | {:<15}".format(entity.text, entity.label_, entity.lemma_))
