from flask import Flask, render_template, jsonify, Response, request
import markdown
import os
from api.islami import get_asmaul_husna, get_quran_audio, get_ayat_quran, get_list_quran, get_jadwal  # Importing the function from islami.py
from api.downloader import get_apk
import requests

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/docs')
def render_markdown():
    # Read the README.md file
    with open('README.md', 'r', encoding='utf-8') as markdown_file:
        content = markdown_file.read()

    # Convert Markdown to HTML
    html_content = markdown.markdown(content)
    print("/docs")
    return render_template('markdown_viewer.html', content=html_content)

# Endpoint for getting Asmaul Husna data
@app.route('/api/asmaulhusna', methods=['GET'])
def get_asmaul_husna_endpoint():
    response = get_asmaul_husna()
    print("/api/asmaulhusna")
    return Response(response, status=200, content_type='application/json')

@app.route("/api/quran/audio/<int:surah>/<int:ayat>", methods=["GET"])
def get_quran_audio_route(surah, ayat=None):
    if surah is None:
        return jsonify({"error": "Surah parameter is missing"}), 400
    if ayat is None:
        audio_url = get_quran_audio(surah)
    else:
        audio_url = get_quran_audio(surah, ayat)

    try:
        audio_response = requests.get(audio_url)
        if audio_response.status_code == 200:
            # Returning audio content with proper content type
            print("/api/quran/audio/:int/:int")
            return Response(audio_response.content, mimetype="audio/ogg")
        else:
            return jsonify({"error": "Failed to fetch audio"}), audio_response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route("/api/quran/audio/<int:surah>", methods=["GET"])
def get_quran_audio_route_full(surah):
    if surah is None:
        return jsonify({"error": "Surah parameter is missing"}), 400
    else:
        audio_url = get_quran_audio(surah)

    try:
        audio_response = requests.get(audio_url)
        if audio_response.status_code == 200:
            # Returning audio content with proper content type
            print("/api/quran/audio/:int")
            return Response(audio_response.content, mimetype="audio/ogg")
        else:
            return jsonify({"status": 500}), audio_response.status_code
    except Exception as e:
        return jsonify({"status": str(e)}), 500
    
@app.route("/api/quran/<int:surah>/<int:ayat>", methods=["GET"])
def get_quran_text_route(surah, ayat=None):
    try:
        response = get_ayat_quran(surah,ayat)
        print("/api/quran/:int/:int")
        return Response(response, status=200, content_type='application/json')
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route("/api/quran/<int:surah>", methods=["GET"])
def get_quran_text_route_full(surah):
    try:
        response = get_ayat_quran(surah)
        print("/api/quran/:int")
        return Response(response, status=200, content_type='application/json')
    except Exception as e:
        return jsonify({"status": str(e)}), 500

@app.route("/api/quran", methods=["GET"])
def get_quran_list():
    try:
        response = get_list_quran()
        print("/api/quran")
        return Response(response, status=200, content_type='application/json')
    except Exception as e:
        return jsonify({"status": str(e)}), 500
    
@app.route("/api/sholat/<string:kota>", methods=["GET"])
def get_jadwal_sholat(kota):
    try:
        response = get_jadwal(kota)
        print("/api/sholat/:str")
        return Response(response, status=200, content_type='application/json')
    except Exception as e:
        return jsonify({"status": str(e)}), 500
    
@app.route('/api/apkdownloader')
def apk_downloader():
    print("/api/apkdownloader")
    package_name = request.args.get('package')
    if package_name is None:
        return jsonify({"status": 500}), 500
    apk_data = get_apk(package_name)
    
    # Assuming get_apk returns the APK data as a response
    return Response(apk_data, status=200, content_type='application/json')

    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
