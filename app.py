import os
from flask import Flask, jsonify, redirect, render_template, request, session
from openai import OpenAI

secret_key = os.urandom(16)

app = Flask(__name__)
app.secret_key = secret_key 
client = OpenAI()


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/generate_feedback', methods=['POST'])
def generate_feedback():
  try:
    src_code = request.form.get('source-code', 'Not Specified')
    print("Source Code:", src_code)
    sys_content = "As a cybersecurity expert, your task is to assess user input for potential malware presence and determine the likelihood of it being malicious."
    usr_content = (
      'Evaluate the provided source code for malware presence, identify any specific malware type, and present the findings in bullet format: '
      'the first line indicating whether it is malware, change the line, the second line specifying the type of malware of the function of the source code in one sentence if applicable, no other explanation is needed.\n'
      + src_code
  )
    completion = client.chat.completions.create(
      model="gpt-4",
      messages=[
        {"role": "system", "content": sys_content},
        {"role": "user", "content": usr_content}
      ]
    )
    feedback = completion.choices[0].message.content
    session['feedback'] = feedback
    return redirect('/feedback/')

  except Exception as e:
    return jsonify({'feedback': str(e)})

@app.route('/feedback/')
def practice():
    feedback = session.get('feedback', 'No feedback available')
    formatted_feedback = feedback.replace('\n', '<br>')
    return render_template('feedback.html', fb=formatted_feedback)



if __name__ == "__main__":
    app.run()