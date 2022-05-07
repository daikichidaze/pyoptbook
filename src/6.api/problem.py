import pandas as pd
import pulp

from itertools import product


class CarGroupProblem():
    # Constructor
    def __init__(self, df_students, df_cars, name='ClubCarProblem'):
        self.df_students = df_students
        self.df_cars = df_cars
        self.name = name
        self.prob = self._formulate()

    def _formulate(self):
        set_grade = set(self.df_students.grade)
        set_gender = set(self.df_students.gender)

        df_var = pd.DataFrame(
            [{
                'student_id': s,
                'car_id': c,
                'var': pulp.LpVariable(f'x_{s}_{c}', cat='Binary')
            }
                for s, c in product(self.df_students.student_id, self.df_cars.car_id)]
        )
        df_var = pd.merge(df_var, self.df_students, on='student_id')

        p = pulp.LpProblem(name=self.name, sense=pulp.LpMinimize)

        # constrain
        # 1. 1 student to 1 car
        for s in self.df_students.student_id:
            p += pulp.lpSum(df_var[df_var.student_id == s]['var']) == 1

        for c in self.df_cars.car_id:
            df_tmp_c = df_var[df_var.car_id == c]
            # 2. capacity of the car
            cap = self.df_cars.loc[c, 'capacity']
            p += pulp.lpSum(df_tmp_c['var']) <= cap

            # 3. Driver in each car
            p += pulp.lpSum(df_tmp_c[df_tmp_c.license == 1]['var']) >= 1

            # 4. Each grade in each car
            for g in set_grade:
                p += pulp.lpSum(df_tmp_c[df_tmp_c.grade == g]['var']) >= 1
            # 5. Each gender in each car
            for g in set_gender:
                p += pulp.lpSum(df_tmp_c[df_tmp_c.gender == g]['var']) >= 1

        return {
            'prob': p,
            'variable': df_var,
            'list': {
                'S': self.df_students.student_id.tolist(),
                'C': self.df_cars.car_id.to_list()
            }
        }

    def solve(self):
        status = self.prob['prob'].solve()
        df_x = self.prob['variable']
        S = self.prob['list']['S']
        C = self.prob['list']['C']

        df_x['result'] = df_x['var'].apply(lambda x: x.value())
        return df_x[df_x.result == 1][['student_id', 'car_id']].reset_index(drop=True)


if __name__ == '__main__':
    df_students = pd.read_csv('resource/students.csv')
    df_cars = pd.read_csv('resource/cars.csv')

    prob = CarGroupProblem(df_students, df_cars)
    df_solution = prob.solve()
    print('Solution:\n', df_solution)
