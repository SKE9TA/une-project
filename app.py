from flask import Flask, request, jsonify
from une import extract_text_from_word, parse_translations
from une import find_information as find_info

app = Flask(__name__)

@app.route('/extract-text', methods=['POST'])
def extract_text():
    data = request.json
    doc_path = data.get('docPath')
    try:
        text = extract_text_from_word(doc_path)
        return jsonify({'text': text}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/parse-translations', methods=['GET'])
def parse_translations():
    data = request.json
    text = data.get('text')
    translations = parse_translations(text)
    return jsonify(translations), 200

@app.route('/find-information', methods=['POST'])
def find_information():
    data = request.json
    query = data.get('query')
    text = extract_text_from_word('AI TERMINOLOGIES AND THEIR TRANSLATIONS.docx')
    response = find_info(text, query)
    return jsonify({'response': response}), 200

if __name__ == '__main__':
    app.run(debug=True)
