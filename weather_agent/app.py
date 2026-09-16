from flask import (Flask, render_template, request, redirect, url_for,
                   session)
from ai_agent import agent
import uuid

app = Flask(__name__)
app.secret_key = 'gs8dgyshdgw43nnt439-gdgfnf'

@app.route('/')
def index():
    session['thread_id'] = str(uuid.uuid4())
    if 'messages' not in session:
        session['messages'] = []
    return render_template("chat.html",
                           messages=session['messages'])


@app.route('/send', methods=['POST'])
def another():
    user_message = request.form['message']
    user_lat = request.form.get('latitude')
    user_lon = request.form.get('longitude')

    if user_lon and user_lat:
        session['user_location'] = {'lat': user_lat, 'lon': user_lon}

    response = agent.invoke(
        {"messages": [{"role": "user", "content": user_message}]},
        {"configurable": {"thread_id": session['thread_id']}}
    )
    session['messages'].append({'type': 'human',
                                'content': user_message})
    session['messages'].append({'type': 'ai',
                                'content': response["messages"][-1].text})
    session.modified = True

    return redirect(url_for('index'))

app.run(debug=True)