from flask import Markup
from flask import Flask, render_template, request, url_for
import os
from snippet_Instance import SnippetInstance

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
looker = SnippetInstance()


# It represents the default page
@app.route("/")
def template():
    return render_template("template.html")

@app.route("/result", methods=['POST', 'GET'])
def result():
    if request.method == 'POST':
        user_Input = request.form
        out_txt = looker.snippets(user_Input['username'], user_Input['date'],
                                  user_Input['quantity'])
        topic = looker.generate_topic(out_txt)
        tf_Idf_topic = looker.generate_tfidf_topic(out_txt)

        # generate wordcloud
        looker.create_wordcloud()
        PEOPLE_FOLDER = os.path.join('static', 'img')
        app.config['UPLOAD_FOLDER'] = PEOPLE_FOLDER
        full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'h.jpg')

        # generate bar chart
        sortdict_term_frequency = looker.create_tf_idf_dic(out_txt)
        bar_labels = []
        bar_values = []
        for s in sortdict_term_frequency[:9]:
            bar_labels.append(s[1])
            bar_values.append(s[0])

        return render_template("template.html", result=out_txt, lda_topics=topic, tf_Idf_topics = tf_Idf_topic, a=user_Input['username'], b=user_Input['date']
                                  ,c=user_Input['quantity'], user_image = full_filename,  max=17000, labels=bar_labels, values=bar_values)


# No caching at all for API endpoints.
@app.after_request
def add_header(response):
    # response.cache_control.no_store = True
    if 'Cache-Control' not in response.headers:
        response.headers['Cache-Control'] = 'no-store'
    return response

# __name__ means this current file. In this case, it will be main.py.
# This current file will represent my web application.
if __name__ == "__main__":
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
