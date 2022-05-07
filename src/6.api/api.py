import pandas as pd
from flask import Flask, make_response, request
from problem import CarGroupProblem

app = Flask(__name__)


@app.route('/api', methods=['POST'])
def solve():
    df_students, df_cars = preprocess(request)
    df_solution = CarGroupProblem(df_students, df_cars).solve()
    response = postprocess(df_solution)
    return response


def preprocess(request):
    students = request.files['students']
    cars = request.files['cars']

    df_students = pd.read_csv(students)
    df_cars = pd.read_csv(cars)

    return df_students, df_cars


def postprocess(df_solution):
    solution_csv = df_solution.to_csv(index=False)
    response = make_response()
    response.data = solution_csv
    response.headers['Content-Type'] = 'text/csv'
    return response
