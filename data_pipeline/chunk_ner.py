import spacy
nlp = spacy.load("en_core_web_sm")

def get_ner_data(text:str):
    doc = nlp(text)

    ent = doc.ents
    ent_dict = {ent.text: [ent.label_, spacy.explain(ent.label_)] for ent in doc.ents}
    print(ent_dict)
    return ent_dict

            
