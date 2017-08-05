from flask import Flask
from flask_ask import Ask, statement, question
import wolframalpha

app = Flask(__name__)
ask = Ask(app, '/')

client = wolframalpha.Client("7R59HP-PXXLXE8RJE")
		
@app.route('/') 
def homepage():
	return "Hello, let's math" 

@ask.launch
def start_skill():
	msg = "What would you like me to solve?"
	return question(msg)

@ask.intent("mathIntent") 
def solveMath(equation):
	"""
	Parameter: Math problem user wants to solve
	
	Using the API of Wolfram Alpha, we take in a LITERAL slot with the parameter name as "equation".  This "equation" is a math
	problem the user inputs for Alexa to solve.  This parameter gets formatted into a string and then put passed to Wolfram Alpha 
	as a query.  We then get the output and then pass it through some formatting conditions to ensure the output is easily said by 
	Alexa.  

	Return: Answer to the math problem
	"""
	stringEquation = "{}".format(equation)	
	stringEquation = stringEquation.replace(".", "")
	print(stringEquation, flush = True)
	testy = "derivative"
	yay = "integral"
	yaye = "integrate"
	if testy in stringEquation:
		result = client.query(stringEquation)
		message = next(result.results).text
		indexer = message.index("=")	 		
		message = message[indexer + 2 : ]
		return statement(message)	
	if yay in stringEquation or yaye in stringEquation:
		result = client.query(stringEquation)
		message = next(result.results).text
		indexer = message.index("=")	 		
		message = message[indexer + 2 : ]
		message = message.replace("/", " divided by ")
		return statement(message)
	result = client.query(stringEquation)
	message = next(result.results).text
	message = message.replace("/", " divided by ")
	print(message, flush = True)
	return statement(message)

@ask.intent("NoIntent")
def no_intent():
	"""
	Intent that is intialized if the user wants to cancel action  
	"""
	msg = "Ok, thanks. Have a nice day."
	return statement(msg)
 
if __name__ == '__main__':
	app.run(debug=True)



