from flask import Flask, render_template, request, send_file

# Use flask_cache for Flask-Cache
from flask_caching import Cache
import yt_dlp

app = Flask(__name__)

app.config['ENV'] = 'production'
app.config['DEBUG'] = False

# Configure Flask-Cache
cache = Cache(app, config={'CACHE_TYPE': 'simple'})  # You can use other cache types as needed

@app.route('/', methods=['GET', 'POST'])
def download_video():
    if request.method == 'POST':
        url = request.form['url']
        ydl_opts = {}
        try:
            # Define a cache key based on the video URL
            cache_key = f'video_{url}'

            # Check if the result is already cached
            video_file = cache.get(cache_key)

            if video_file is None:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=False)
                    filename = info['title'] + '.mp4'
                    ydl.download([url])

                    # Cache the downloaded video file for a certain period (e.g., 1 hour)
                    cache.set(cache_key, filename, timeout=3600)

                video_file = filename

            return send_file(video_file, as_attachment=True)
        except Exception as e:
            return f"An error occurred: {str(e)}"
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
