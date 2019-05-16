from flask import Flask, render_template, request
from flaskext.mysql import MySQL

app = Flask(__name__)

mysql = MySQL(app)

app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'wireda2012'
app.config['MYSQL_DATABASE_DB'] = 'survey_rs'

mysql.init_app(app)

@app.route('/', methods=["POST", "GET"])
def main():
    return render_template('index.html')

@app.route('/Survey', methods=["POST"])
def nextSurvey():
	conn = mysql.connect()
	cursor = conn.cursor()
	
	userData = request.form
	umur = userData['umur']
	jenis_kel = userData['radioJK']

	def setQuestions():
		cursor.execute("""SELECT * FROM soal""")	
		result = cursor.fetchall()
		return result
	def setAnswers():
		cursor.execute("""SELECT * FROM jawaban""")	
		result = cursor.fetchall()
		return result
	def getLastResponden():
		cursor.execute("""SELECT id_responden FROM `responden` ORDER BY id_responden DESC LIMIT 1""")
		result = cursor.fetchall()
		return result

	result_q = setQuestions()
	result_a = setAnswers()
	result_r = getLastResponden()

	return render_template('survey.html', umur=umur, jenis_kel=jenis_kel, result_q=result_q, result_a=result_a, result_r=result_r)

@app.route('/ThankYou', methods=["POST"])
def submitSurvey():
	surveyData = request.form
	umur = surveyData['umur']
	jenis_kel = surveyData['jenis_kel']
	id_res = surveyData['id_res']

	conn = mysql.connect()
	cursor = conn.cursor()
	cursor.execute("""INSERT INTO responden(id_responden, umur, jenis_kel)  VALUES(%s, %s, %s)""", (id_res, umur, jenis_kel))
	conn.commit()
	conn.close()
	
	answer = ['rQ0','rQ1', 'rQ2', 'rQ3', 'rQ4']
	answer_len = len(answer)

	for i in range(1, answer_len):
		ans = surveyData[answer[i]]
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute("""INSERT INTO pilihan(id_responden, id_soal, id_jawaban)  VALUES(%s, %s, %s)""", (id_res, i, ans))
		conn.commit()
		conn.close()
	return render_template('thankyou.html')

@app.route('/Result')
def showResult():
	conn = mysql.connect()
	cursor = conn.cursor()

	def getResponden():
		cursor.execute("""SELECT SUM(IF(age BETWEEN 7 and 17,1,0)) as 'range1', SUM(IF(age BETWEEN 18 and 55,1,0)) as 'range2', 		SUM(IF(age >=55, 1, 0)) as 'range3', COUNT(*) as 'total' FROM (SELECT (umur) AS age FROM responden) as derived""")
		result = cursor.fetchall()
		return result
	def getQuestions():
		cursor.execute("""SELECT * FROM soal""")
		result = cursor.fetchall()
		return result
	#def getAnswers():
	#	cursor.execute("""SELECT id_soal, SUM(IF(id_jawaban=1,1,0)) AS 'Y', SUM(IF(id_jawaban=2,1,0)) AS 'C', SUM(IF(id_jawaban=3,1,0)) AS 'T' FROM pilihan GROUP BY id_soal""")
	#	result = cursor.fetchall()
	#	return result

	def getAnswer1():
		cursor.execute("""SELECT id_soal, SUM(IF(id_jawaban=1,1,0)) AS 'Y', SUM(IF(id_jawaban=2,1,0)) AS 'C', SUM(IF(id_jawaban=3,1,0)) AS 'T' FROM pilihan WHERE id_soal=1""")
		result = cursor.fetchall()
		return result
	def getAnswer2():
		cursor.execute("""SELECT id_soal, SUM(IF(id_jawaban=1,1,0)) AS 'Y', SUM(IF(id_jawaban=2,1,0)) AS 'C', SUM(IF(id_jawaban=3,1,0)) AS 'T' FROM pilihan WHERE id_soal=2""")
		result = cursor.fetchall()
		return result
	def getAnswer3():
		cursor.execute("""SELECT id_soal, SUM(IF(id_jawaban=1,1,0)) AS 'Y', SUM(IF(id_jawaban=2,1,0)) AS 'C', SUM(IF(id_jawaban=3,1,0)) AS 'T' FROM pilihan WHERE id_soal=3""")
		result = cursor.fetchall()
		return result
	def getAnswer4():
		cursor.execute("""SELECT id_soal, SUM(IF(id_jawaban=1,1,0)) AS 'Y', SUM(IF(id_jawaban=2,1,0)) AS 'C', SUM(IF(id_jawaban=3,1,0)) AS 'T' FROM pilihan WHERE id_soal=4""")
		result = cursor.fetchall()
		return result

	result_p = getResponden()
	result_d = getQuestions()
	#result_a = getAnswers()
	result_1 = getAnswer1()
	result_2 = getAnswer2()
	result_3 = getAnswer3()
	result_4 = getAnswer4()
	
	return render_template('result.html', result_p=result_p, result_d=result_d, result_1=result_1, result_2=result_2, result_3=result_3, result_4=result_4)

if __name__ == '__main__':
	# app.run(debug=True)
	app.run(host= '10.10.10.155')
