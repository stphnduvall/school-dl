from os import listdir

import youtube_dl
from flask import Flask, redirect, render_template, request, send_file, url_for

app = Flask(__name__, template_folder="./")

ytdl_options = {'format': 'm4a', 'restrictfilenames': 'True', 'outtmpl': 'media/%(title)s-%(id)s.%(ext)s'}


@app.route('/')
@app.route('/form')
def form():
    return render_template('form.html')


@app.route('/download', methods=['POST', 'GET'])  # type: ignore
def download():
    if request.method == 'GET':
        return f"The URL /download is accessed directly. Try going to '/form' to submit form"
    if request.method == 'POST':
        form_data = request.form['urls'].split('\n')
        video_ids = []
        for url in form_data:
            if url == '':
                continue
            id_loc = int(url.find('v='))+2
            video_ids.append(url[id_loc:id_loc+11])

        with youtube_dl.YoutubeDL(ytdl_options) as ydl:
            ydl.download(video_ids)

        
        return downloads(video_ids)


@app.route('/downloads')
def downloads(video_ids):
    print(video_ids)
    downloaded_files = listdir('./media/')
    videos = {}
    for id in video_ids:
        for file in downloaded_files:
            if id in file:
                videos[id] = file
                downloaded_files.remove(file)
                break
    print(videos)
    return render_template('downloads.html', links=videos)


@app.route('/files/<video>')
def files(video):
    return send_file('media/' + video, as_attachment=True)


if __name__ == "__main__":
    app.run(host='localhost', port=5000)