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
    src_code = request.args.get('source-code', 'Not Specified')
    sys_content = "As a cybersecurity expert, your task is to assess user input for potential malware presence and determine the likelihood of it being malicious."
    usr_content = 'Comment on the following source code: '+src_code+'.'
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
    return render_template('feedback.html', 
                           fb = session['feedback']
                           )


if __name__ == "__main__":
    app.run()