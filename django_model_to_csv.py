from stackoverflow.models import StackoverflowAnswersToUserQuestions

answers = StackoverflowAnswersToUserQuestions.objects.all()[0:5000]

a_body = []

from bs4 import BeautifulSoup


for ans in answers:
	clean_answer_body= BeautifulSoup(ans.body,"lxml").text
	a_body.append(clean_answer_body)


import pandas as pd

df = pd.DataFrame({'body':a_body})

df.to_csv('stack_answer.csv', sep='\t')