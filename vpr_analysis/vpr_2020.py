import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


class VPR20:
    def __init__(self, file_name):
        self.df = pd.read_excel(file_name)
        self.__data_preprocessing()

    def __data_preprocessing(self):
        self.df.dropna(subset=['sum'], inplace=True)
        self.df = self.df.rename(columns={"user": "логин школы",
                                          "sum": "всего баллов",
                                          "klass": "класс",
                                          "code": "номер обучающегося",
                                          "gender": "пол",
                                          "otc": "отметка за предыдущую четверть/триместр"})
        # self.__add_region()
        index_first_task = self.df.columns.get_loc('a-1-grade')
        index_books = self.df.columns.get_loc('Учебник')
        column_list = self.df.columns[index_first_task: index_books]
        self.df[column_list] = self.df[column_list].apply(pd.to_numeric, errors='coerce')
        self.df[column_list] = self.df[column_list].fillna(0)
        self.df["отметка за предыдущую четверть/триместр"] = self.df[
            "отметка за предыдущую четверть/триместр"].apply(pd.to_numeric, errors='coerce')
        self.df["отметка за предыдущую четверть/триместр"] = self.df[
            "отметка за предыдущую четверть/триместр"].fillna(0)
        self.df[["var-1", "var-2"]] = self.df[["var-1", "var-2"]].apply(pd.to_numeric, errors='coerce')
        self.df[["var-1", "var-2"]] = self.df[["var-1", "var-2"]].fillna(0)

    def get_unic_schools(self) -> list:
        return [school for school in self.df["логин школы"].drop_duplicates()]

    def get_dict_schools_liters(self) -> dict:
        dictionary = {}
        for index, row in self.df[["логин школы", "класс"]].drop_duplicates().iterrows():

            if dictionary.get(row["логин школы"]) is None:
                dictionary[row["логин школы"]] = [row["класс"]]
            else:
                dictionary[row["логин школы"]].append(row["класс"])
        return dictionary

    def get_dict_schools_liters_students(self) -> dict:
        dictionary = {}
        for index, row in self.df[["логин школы", "класс", "номер обучающегося", "пол"]].iterrows():

            if dictionary.get(row["логин школы"]) is None:
                dictionary[row["логин школы"]] = {row["класс"]: {row["номер обучающегося"]: row["пол"]}}
            else:
                if dictionary[row["логин школы"]].get(row["класс"]) is None:
                    dictionary[row["логин школы"]][row["класс"]] = {row["номер обучающегося"]: row["пол"]}
                else:
                    dictionary[row["логин школы"]][row["класс"]][row["номер обучающегося"]] = row["пол"]
        return dictionary

    def df_to_list(self):
        index_books = self.df.columns.get_loc('Учебник')
        return self.df[self.df.columns[:index_books]].values.tolist()

    def get_balls(self, name, parallel):
        subtrahend = 0

        mat4 = [5, 6, 9, 10, 14, 15]
        mat5 = [6, 7, 10, 11, 14, 15]
        mat6 = [5, 6, 9, 10, 13, 14]
        mat7 = [6, 7, 11, 12, 15, 16]
        mat8 = [7, 8, 14, 15, 20, 21]

        rus4 = [13, 14, 23, 24, 32, 33]
        rus5 = [17, 18, 28, 29, 38, 39]
        rus6 = [24, 25, 34, 35, 44, 45]
        rus7 = [21, 22, 31, 32, 41, 42]
        rus8 = [25, 26, 31, 32, 44, 45]

        fra7 = [12, 13, 20, 21, 26, 27]
        fra11 = [10, 11, 17, 18, 24, 25]
        nem7 = [12, 13, 20, 21, 26, 27]
        nem11 = [10, 11, 17, 18, 24, 25]

        fiz7 = [4, 5, 7, 8, 10, 11]
        fiz8 = [4, 5, 7, 8, 10, 11]
        fiz11 = [8, 9, 15, 16, 20, 21]

        obsh6 = [8, 9, 14, 15, 19, 20]
        obsh7 = [9, 10, 15, 16, 20, 21]
        obsh8 = [10, 11, 16, 17, 21, 22]

        bio5 = [11, 12, 17, 18, 23, 24]
        bio6 = [11, 12, 17, 18, 23, 24]
        bio7 = [9, 10, 16, 17, 22, 23]
        bio8 = [12, 13, 20, 21, 28, 29]
        bio11 = [10, 11, 17, 18, 24, 25]

        geo6 = [9, 10, 21, 22, 30, 31]
        geo7 = [10, 11, 25, 26, 32, 33]
        geo8 = [12, 13, 26, 27, 34, 35]
        geo10 = [6, 7, 12, 13, 17, 18]
        geo11 = [6, 7, 12, 13, 17, 18]

        eng7 = [12, 13, 20, 21, 26, 27]
        eng11 = [10, 11, 17, 18, 24, 25]

        him8 = [9, 10, 18, 19, 27, 28]
        him11 = [10, 11, 19, 20, 27, 28]

        ist5 = [3, 4, 7, 8, 11, 12]
        ist6 = [5, 6, 10, 11, 15, 16]
        ist7 = [6, 7, 12, 13, 18, 19]
        ist8 = [6, 7, 11, 12, 17, 18]
        ist11 = [6, 7, 12, 13, 17, 18]

        om4 = [7, 8, 17, 18, 26, 27]

        if 'Математика' in name and parallel == 4:
            translation_scale = mat4
            subtrahend = 1

        elif 'Математика' in name and parallel == 5:
            translation_scale = mat5
            subtrahend = 1

        elif 'Математика' in name and parallel == 6:
            translation_scale = mat6
            subtrahend = 1

        elif 'Математика' in name and parallel == 7:
            translation_scale = mat7
            subtrahend = 1

        elif 'Математика' in name and parallel == 8:
            translation_scale = mat8
            subtrahend = 1

        elif 'Русский язык' in name and parallel == 4:
            translation_scale = rus4
            subtrahend = 2

        elif 'Русский язык' in name and parallel == 5:
            translation_scale = rus5
            subtrahend = 2

        elif 'Русский язык' in name and parallel == 6:
            translation_scale = rus6
            subtrahend = 2

        elif 'Русский язык' in name and parallel == 7:
            translation_scale = rus7
            subtrahend = 2

        elif 'Русский язык' in name and parallel == 8:
            translation_scale = rus8
            subtrahend = 2

        elif 'Французский язык' in name and parallel == 7:
            translation_scale = fra7

        elif 'французскому языку, 11' in name:
            translation_scale = fra11

        elif 'Немецкий язык' in name and parallel == 7:
            translation_scale = nem7

        elif 'немецкому языку, 11' in name:
            translation_scale = nem11

        elif 'Физика' in name and parallel == 7:
            translation_scale = fiz7

        elif 'Физика' in name and parallel == 8:
            translation_scale = fiz8

        elif 'физике, 11' in name:
            translation_scale = fiz11

        elif 'Обществознание' in name and parallel == 6:
            translation_scale = obsh6

        elif 'Обществознание' in name and parallel == 7:
            translation_scale = obsh7

        elif 'Обществознание' in name and parallel == 8:
            translation_scale = obsh8

        elif 'Биология' in name and parallel == 5:
            translation_scale = bio5

        elif 'Биология' in name and parallel == 6:
            translation_scale = bio6

        elif 'Биология' in name and parallel == 7:
            translation_scale = bio7

        elif '(по образцу 8 класса)' in name:
            translation_scale = bio8

        elif 'Биология' in name and parallel == 8:
            translation_scale = bio8

        elif 'биологии, 11' in name:
            translation_scale = bio11

        elif 'География' in name and parallel == 6:
            translation_scale = geo6

        elif 'География' in name and parallel == 7:
            translation_scale = geo7

        elif 'География' in name and parallel == 8:
            translation_scale = geo8

        elif 'географии, 10' in name:
            translation_scale = geo10

        elif 'географии, 11' in name:
            translation_scale = geo11

        elif 'Английский язык' in name and parallel == 7:
            translation_scale = eng7

        elif 'по английскому языку, 11 класс' in name:
            translation_scale = eng11

        elif 'Химия' in name and parallel == 8:
            translation_scale = him8

        elif 'химии, 11' in name:
            translation_scale = him11

        elif 'История' in name and parallel == 5:
            translation_scale = ist5

        elif 'История' in name and parallel == 6:
            translation_scale = ist6

        elif 'История' in name and parallel == 7:
            translation_scale = ist7

        elif 'История' in name and parallel == 8:
            translation_scale = ist8

        elif 'истории, 11' in name:
            translation_scale = ist11

        elif 'Окружающий мир' in name:
            translation_scale = om4

        else:
            print(name)
            translation_scale = [0, 0, 0, 0, 0, 0]

        return translation_scale[1], translation_scale[3], translation_scale[5]
