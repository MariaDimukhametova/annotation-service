import re
import nltk
import pymorphy2
import PyPDF2

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

nltk.download('punkt')
nltk.download('stopwords')


def process_pdf_text(file_path):
    with open(file_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)

        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            page_text = re.sub(r'(\w+)-(\n)(\w+)', r'\1\3', page_text)
            text += page_text

    return text


def clean_token(token):
    return re.sub('[^а-яА-ЯёЁ]', '', token)


def extract_tokens(data, language='russian'):
    tokens = word_tokenize(data, language=language)
    filtered_tokens = set()
    lemmatized_text = {}

    stop_words = set(stopwords.words(language))
    analyzer = pymorphy2.MorphAnalyzer()

    for token in tokens:
        cleaned = clean_token(token)
        if cleaned and cleaned not in stop_words and len(cleaned) > 1:

            normal_form = analyzer.parse(cleaned)[0].normal_form
            filtered_tokens.add(normal_form)

            if normal_form not in lemmatized_text:
                lemmatized_text[normal_form] = []
            lemmatized_text[normal_form].append(token)

    return filtered_tokens, lemmatized_text


def process(tokens, lemmatized_text, output_file='tokens.txt', lemma_output_file='lemmas.txt'):
    with open(output_file, 'w', encoding='utf-8') as tokens_file, \
            open(lemma_output_file, 'w', encoding='utf-8') as lemmas_file:
        for token in tokens:
            tokens_file.write(token + '\n')  # Запись исходного токена в файл с токенами

        for lemma, tokens_list in lemmatized_text.items():
            # Запись нормализованного слова и его исходных форм в файл с леммами
            lemmas_file.write(f"{lemma}: {' '.join(tokens_list)}\n")


def replace_tokens_with_lemmas(input_text, lemmas_file):
    lemmas = {}
    with open(lemmas_file, 'r', encoding='utf-8') as f:
        for line in f:
            lemma, tokens_list = line.strip().split(':')
            tokens = tokens_list.split()
            lemmas.update({token: lemma for token in tokens})

    replaced_text = input_text
    for word, lemma in lemmas.items():
        replaced_text = re.sub(r'\b' + re.escape(word) + r'\b', lemma, replaced_text)

    return replaced_text


if __name__ == "__main__":
    pdf_text = process_pdf_text("testdoc.pdf")
    filtered_tokens, lemmatized_text = extract_tokens(pdf_text)
    process(filtered_tokens, lemmatized_text, lemma_output_file='lemmas.txt')

    replaced_text = replace_tokens_with_lemmas(pdf_text, "lemmas.txt")

    with open("replaced_text.txt", "w", encoding="utf-8") as f:
        f.write(replaced_text)