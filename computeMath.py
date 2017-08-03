from flask import Flask
from flask_ask import Ask, statement, question
import wolframalpha

client = wolframalpha.Client("7R59HP-PXXLXE8RJE")

app = Flask(__name__)
ask = Ask(app, '/')

@app.route('/')
def homepage():
    return "Hello, this is an application where we compute mathematical equations"

@ask.launch
def start_skill():
    msg = "Hello, what would you like me to solve?"
    return question(msg)

@ask.intent("mathIntent")
def solveMath(equation):
	stringEquation = "{}".format(equation)
	print(stringEquation)
	testy = "derivative"
	if testy in stringEquation:
		result = client.query(stringEquation)
		message = next(result.results).text
		indexer = message.index("=")	
		message = message[indexer + 2 : ]
		return statement(message)
	result = client.query(stringEquation)
	message = next(result.results).text
	return statement(message)

@ask.intent("NoIntent")
def no_intent():
    msg = "Ok, thanks. Have a nice day."
    return statement(msg)

if __name__ == '__main__':
    app.run(debug=True)


