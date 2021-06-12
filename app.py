from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dbsparta


## HTML을 주는 부분
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/participate')
def home_participate():
    return render_template('index_participate.html')


@app.route('/result')
def home_result():
    return render_template('index_result.html')


@app.route('/register', methods=['GET'])
def data_loading():
    questions = list(db.surveytest.find({}, {'_id': False}).sort("number"))
    return jsonify({'all_questions': questions})


## API 역할을 하는 부분
@app.route('/register', methods=['POST'])
def data_saving():
    number_receive = request.form['number_give']
    question_receive = request.form['question_give']
    type_receive = request.form['type_give']
    list_receive = request.form['list_give'].split(",")

    if number_receive == 0:
        return jsonify({'msg': "문항 번호를 입력해주세요."})
    if question_receive == "":
        return jsonify({'msg': "질문을 입력해주세요."})
    if type_receive == "":
        return jsonify({'msg': "유형을 선택해주세요."})
    if type_receive != "word" and list_receive == ['']:
        return jsonify({'msg': "보기를 1개 이상 입력해주세요."})

    doc = {
        'number': number_receive,
        'question': question_receive,
        'type': type_receive,
        'list': list_receive
    }

    db.surveytest.insert_one(doc)

    return jsonify({'msg': "문항이 저장되었습니다."})


@app.route('/participate/load', methods=['GET'])
def question_loading():
    questions = list(db.surveytest.find({}, {'_id': False}).sort("number"))
    return jsonify({'all_questions': questions})


@app.route('/result/load', methods=['GET'])
def answer_loading():
    answers = list(db.surveyanswertest.find({}, {'_id': False}).sort("number"))
    return jsonify({'all_answers': answers})


## API 역할을 하는 부분
@app.route('/participate/save', methods=['POST'])
def answer_saving():
    number_receive = request.form['number_give']
    question_receive = request.form['question_give']
    answer_receive = request.form['answer_give']

    doc = {
        'number': number_receive,
        'question': question_receive,
        'answer': answer_receive
    }

    db.surveyanswertest.insert_one(doc)

    return jsonify({'msg': "답변이 저장되었습니다."})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
