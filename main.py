from flask import Flask, render_template, request
from flask_cors import CORS
from scraper import download_media, dic_list_all_series_movies, dic_web_name_to_download_name
import os
import glob
from threading import Thread



app = Flask(__name__)

CORS(app)


@app.route("/")
def home():
    # download photos
    # get_photos()
    # get photos from directory

    curr_dir = os.path.dirname(__file__)
    path = os.path.join(curr_dir, 'static/themeImages/*')
    full_files_names = glob.glob(path)
    file_names = []
    for i in full_files_names:
        rel_path = i.split('/')[-2] + '/' + i.split('/')[-1]
        file_names.append(rel_path)
    return render_template('index.html', photos=file_names)


@app.route("/objectpage/<string:name>", methods=['GET'])
def objectpage(name):
    sd = name
    with open('static/texts/' + name + '.txt') as f:
        des_text = f.readline()
        path = 'themeImages/' + name + '.jpeg'
        z=2
        versions_series_to_show = dic_list_all_series_movies[name]
        z=2

        return render_template('objectpage.html', name=name, des_text=des_text, path=path,
                               versions_series_to_show=versions_series_to_show)


@app.route("/showvideo/<string:video_name>", methods=['GET'])
def showvideo(video_name):


    # download video obj using download_media function, pass video_name arg
    # thread_for_download = Thread(target=download_media, args=(video_name,))
    # thread_for_download.start()
    # thread_for_download.join()

    # download_media(video_name)
    # get path by video_name from dic web_name_to_download_name
    # path = 'videos/.If.2021.S01E04.720p.HEVC.x265 @Disney_Plus_il.mp4'
    path = 'videos/' + dic_web_name_to_download_name.get(video_name)
    # render to html
    return render_template('showvideo.html', path=path)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
