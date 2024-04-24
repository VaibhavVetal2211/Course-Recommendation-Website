from flask import Flask, render_template, request
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle

app = Flask(__name__)

# Load the necessary data for recommendation
newc = pd.read_pickle(r"venv_name\model.pkl")
similarity =pd.read_pickle(r"venv_name\similarity.pkl")



@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about', endpoint='about')
def about_page():
    return render_template('about.html')


@app.route('/login', endpoint='login')
def about_page():
    return render_template('login.html')

@app.route('/contactus')
def about_page():
    return render_template('contactus.html')

@app.route('/form', endpoint='form')
def about_page():
    return render_template('form.html')
@app.route('/blog', endpoint='blog')
def about_page():
    return render_template('blog.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    domain = request.form['domain']
    min_duration = float(request.form['min_duration'])
    max_duration = float(request.form['max_duration'])
    level = request.form['level']

    recommended_courses = get_recommendations(domain, min_duration, max_duration, level)

    return render_template('result.html', recommended_courses=recommended_courses)

def get_recommendations(domain, min_duration, max_duration, level):
    index = newc[newc['domain'] == domain].index

    if len(index) == 0:
        print("Course not found.")
        return []

    index = index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])

    recommended_courses = []

    for i in distances[1:]:  
        course_index = i[0]
        course_duration = newc.iloc[course_index]['durations']
        course_level = newc.iloc[course_index]['level'][0]

        if (min_duration is None or course_duration >= min_duration) and \
           (max_duration is None or course_duration <= max_duration) and \
           (level in course_level):
            recommended_courses.append({
                'course_title': newc.iloc[course_index]['course_title'],
                'duration': course_duration,
                'level': course_level,
                'url': newc.iloc[course_index]['url'],
                'is_paid': newc.iloc[course_index]['is_paid'],
                'price': newc.iloc[course_index]['price']
            })

        if len(recommended_courses) >= 5:
            break

    # if recommended_courses:
    #     print("Recommended courses:")
    #     for count, course in enumerate(recommended_courses, start=1):
    #         print(f"{count}. Course Name: {course['course_title']}")
    #         print(f"   Duration: {course['duration']}")
    #         print(f"   Course Level: {course['level']}")
    #         print(f"   URL: {course['url']}")
    # else:
    #     print("No courses found within the specified duration range.")

    return recommended_courses


if __name__ == '__main__':
    app.run(debug=True)