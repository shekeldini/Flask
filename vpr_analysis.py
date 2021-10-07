import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


class VPR:
    def __init__(self, file_name):
        self.translation_scale, self.subj_name, self.subtrahend = self.__get_balls(file_name)

        try:
            self.df = pd.read_excel(file_name)
        except Exception:
            self.df = pd.read_csv(file_name, sep=";")

        self.__data_preprocessing()
        self.logins_df = pd.read_excel("excel/logins.xlsx")

    def __data_preprocessing(self):
        try:
            index_books = self.df.columns.get_loc('Учебник')
            index_first_task = self.df.columns.get_loc('балл за 1')
            column_list = self.df.columns[index_first_task: index_books]

            self.df = self.df[self.df['вариант'] != 'отсутствовал']

            self.df = self.df[self.df.columns[: index_books + 1]]
            self.df['Учебник'] = self.df['Учебник'].replace(np.nan, "Нет данных")

            self.df[column_list] = self.df[column_list].apply(pd.to_numeric, errors='coerce')
            self.df[column_list] = self.df[column_list].fillna(0)

            self.df["отметка за предыдущую четверть/триместр"] = self.df[
                "отметка за предыдущую четверть/триместр"].apply(pd.to_numeric, errors='coerce')
            self.df["отметка за предыдущую четверть/триместр"] = self.df[
                "отметка за предыдущую четверть/триместр"].fillna(0)

            self.df["вариант"] = self.df["вариант"].apply(pd.to_numeric, errors='coerce')
            self.df["вариант"] = self.df["вариант"].fillna(0)

            for char in ["0", "1", "2", "3", "4", "X"]:
                self.df = self.df[self.df['Учебник'] != char]
        except Exception:
            self.df = self.df[self.df['var-1'] != 'отсутствовал']
            self.df = self.df.rename(columns={"user": "логин школы", "sum": "всего баллов"})
            self.__add_region()
            self.df = self.df[["всего баллов", "логин школы", "регион"]]

    def get_translation_scale(self) -> tuple:
        # 3 [1] 4 [3] 5 [5]
        return self.translation_scale[1], self.translation_scale[3], self.translation_scale[5]

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

    def get_subj_name(self):
        return self.subj_name

    def get_unic_schools(self) -> list:
        return [school for school in self.df["логин школы"].drop_duplicates()]

    def get_dict_schools_liters_books(self) -> dict:
        dictionary = {}
        for index, row in self.df[["логин школы", "класс", "Учебник"]].drop_duplicates().iterrows():

            if dictionary.get(row["логин школы"]) is None:
                dictionary[row["логин школы"]] = {row["класс"]: row["Учебник"]}
            else:
                dictionary[row["логин школы"]][row["класс"]] = row["Учебник"]
        return dictionary

    def get_dict_schools_liters(self) -> dict:
        dictionary = {}
        for index, row in self.df[["логин школы", "класс"]].drop_duplicates().iterrows():

            if dictionary.get(row["логин школы"]) is None:
                dictionary[row["логин школы"]] = [row["класс"]]
            else:
                dictionary[row["логин школы"]].append(row["класс"])
        return dictionary

    def __add_region(self) -> None:
        self.df["регион"] = self.df.apply(lambda x: self.__find_region(x['логин школы']), axis=1)

    def __get_basemark(self, value) -> int:
        if value - self.subtrahend <= self.translation_scale[0]:
            return 2
        elif (value - self.subtrahend >= self.translation_scale[1]) and (
                value - self.subtrahend <= self.translation_scale[4]):
            return 4
        elif value - self.subtrahend >= self.translation_scale[5]:
            return 5

    def __get_realmark(self, value) -> int:
        if value <= self.translation_scale[0]:
            return 2
        elif value >= self.translation_scale[1] and value <= self.translation_scale[2]:
            return 3
        elif value >= self.translation_scale[3] and value <= self.translation_scale[4]:
            return 4
        elif value >= self.translation_scale[5]:
            return 5

    def __get_school_count_for_region(self, region_name) -> int:
        df = self.df[self.df["регион"] == region_name]
        return len(df["логин школы"].drop_duplicates())

    def __convert_all_score_to_baseMarks(self) -> None:
        self.df["Оценка"] = self.df.apply(lambda x: self.__get_basemark(x['всего баллов']), axis=1)

    def __convert_all_score_to_realMarks(self) -> None:
        self.df["Оценка"] = self.df.apply(lambda x: self.__get_realmark(x['всего баллов']), axis=1)

    def __get_df_with_mark(self, mark):
        return self.df[self.df['Оценка'] == mark]

    def __convert_column(self, df, by, base):
        df = df.groupby([by]).count()
        df = df["Оценка"].reset_index()
        df = df.rename(columns={"Оценка": base})
        return df

    def __merge_data_frames(self, *args):
        df = args[0]
        for df_ in args[1:-1]:
            df = df.merge(df_, on=args[-1], how='outer')
        return df.fillna(0)

    def __find_school_name(self, school):
        return self.logins_df.loc[self.logins_df["логин"] == school].iloc[0]['имя']

    def __find_region(self, school):
        return self.logins_df.loc[self.logins_df["логин"] == school].iloc[0]['регион']

    def __rename_schools(self, df):
        df["логин школы"] = df.apply(lambda x: self.__find_school_name(x['логин школы']), axis=1)
        return df

    def __get_counts_for_regions(self):
        counts = self.df['регион'].value_counts()
        counts = counts.reset_index()
        counts = counts.rename(columns={"index": "регион", "регион": "Кол-во участников"})
        counts["Кол-во ОО"] = counts.apply(lambda x: self.__get_school_count_for_region(x['регион']), axis=1)
        return counts

    def __get_counts_for_schools(self):
        counts = self.df['логин школы'].value_counts()
        counts = counts.reset_index()
        counts = counts.rename(columns={"index": "логин школы", "логин школы": "Кол-во участников"})
        return counts

    def get_base_information_for_schools(self):
        self.__convert_all_score_to_baseMarks()
        counts_for_schools = self.__get_counts_for_schools()
        below_baseline = self.__convert_column(self.__get_df_with_mark(2), "логин школы", "Ниже базового")
        baseline = self.__convert_column(self.__get_df_with_mark(4), "логин школы", "Базовый")
        above_baseline = self.__convert_column(self.__get_df_with_mark(5), "логин школы", "Выше базового")
        school_logins_with_region = self.df[["логин школы", "регион"]].drop_duplicates()
        base_information_for_schools = self.__merge_data_frames(counts_for_schools,
                                                                below_baseline,
                                                                baseline,
                                                                above_baseline,
                                                                school_logins_with_region, "логин школы")
        cols = ["Ниже базового", "Базовый", "Выше базового"]
        base_information_for_schools[cols] = round(
            base_information_for_schools[cols].div(base_information_for_schools[cols].sum(axis=1), axis=0).multiply(
                100), 2)
        return base_information_for_schools

    def get_real_information_for_schools(self):
        self.__convert_all_score_to_realMarks()
        counts_for_schools = self.__get_counts_for_schools()
        result_with_2 = self.__convert_column(self.__get_df_with_mark(2), "логин школы", "2")
        result_with_3 = self.__convert_column(self.__get_df_with_mark(3), "логин школы", "3")
        result_with_4 = self.__convert_column(self.__get_df_with_mark(4), "логин школы", "4")
        result_with_5 = self.__convert_column(self.__get_df_with_mark(5), "логин школы", "5")
        school_logins_with_region = self.df[["логин школы", "регион"]].drop_duplicates()
        real_information_for_schools = self.__merge_data_frames(counts_for_schools,
                                                                result_with_2,
                                                                result_with_3,
                                                                result_with_4,
                                                                result_with_5,
                                                                school_logins_with_region, "логин школы")
        cols = ["2", "3", "4", "5"]
        real_information_for_schools[cols] = round(
            real_information_for_schools[cols].div(real_information_for_schools[cols].sum(axis=1), axis=0).multiply(
                100), 2)
        return real_information_for_schools

    def get_base_information_for_regions(self):
        self.__convert_all_score_to_baseMarks()
        counts_for_regions = self.__get_counts_for_regions()
        below_baseline = self.__convert_column(self.__get_df_with_mark(2), "регион", "Ниже базового")
        baseline = self.__convert_column(self.__get_df_with_mark(4), "регион", "Базовый")
        above_baseline = self.__convert_column(self.__get_df_with_mark(5), "регион", "Выше базового")
        base_information_for_regions = self.__merge_data_frames(counts_for_regions,
                                                                below_baseline,
                                                                baseline,
                                                                above_baseline, "регион")
        cols = ["Ниже базового", "Базовый", "Выше базового"]
        base_information_for_regions[cols] = round(
            base_information_for_regions[cols].div(base_information_for_regions[cols].sum(axis=1), axis=0).multiply(
                100), 2)
        return base_information_for_regions

    def get_real_information_for_regions(self):
        self.__convert_all_score_to_realMarks()
        counts_for_regions = self.__get_counts_for_regions()
        result_with_2 = self.__convert_column(self.__get_df_with_mark(2), "регион", "2")
        result_with_3 = self.__convert_column(self.__get_df_with_mark(3), "регион", "3")
        result_with_4 = self.__convert_column(self.__get_df_with_mark(4), "регион", "4")
        result_with_5 = self.__convert_column(self.__get_df_with_mark(5), "регион", "5")
        real_information_for_regions = self.__merge_data_frames(counts_for_regions,
                                                                result_with_2,
                                                                result_with_3,
                                                                result_with_4,
                                                                result_with_5, "регион")
        cols = ["2", "3", "4", "5"]
        real_information_for_regions[cols] = round(
            real_information_for_regions[cols].div(real_information_for_regions[cols].sum(axis=1), axis=0).multiply(
                100), 2)
        return real_information_for_regions

    def plot_NB(self, df):
        altai_krai_VB = df.iloc[0]['Выше базового']
        df = df.loc[1:]
        plt.figure(figsize=(25, 7))
        plt.bar(df["Группы участников"], df["Выше базового"], color='#7eb8e9')
        plt.xticks(rotation=90)
        plt.ylabel("Уровень знаний в процентах (%)")
        plt.title("Уровень знаний выше базового")

        plt.hlines(altai_krai_VB, xmin=-1, xmax=len(df), linestyles='dashed',
                   color='r', linewidth=3, label='Алтайский край')
        plt.xlim([-0.5, len(df)])
        plt.legend(loc='upper right')

    def save(self, df, name):
        df.to_excel("excel/vpr_analysis/" + name + ".xlsx", index=False)

    def __find_subject_name(self, file_name):

        if "математике" in file_name:
            return "Математика"

        elif "окружающему миру" in file_name:
            return "Окружающий_мир"

        elif "русскому языку" in file_name:
            return "Русский_язык"

        elif "биологии" in file_name:
            return "Биология"

        elif "истории" in file_name:
            return "История"

        elif "географии" in file_name:
            return "География"

        elif "обществознанию" in file_name:
            return "Обществознание"

        elif "немецкому языку" in file_name:
            return "Немецкий_язык"

        elif "физике" in file_name:
            return "Физика"

        elif "французскому языку" in file_name:
            return "Французский_язык"

        elif "английскому языку" in file_name:
            return "Английский_язык"

        elif "химии" in file_name:
            return "Химия"

    def __get_balls(self, name):
        subj_name = self.__find_subject_name(name)
        subtrahend = 0
        translation_scale = [1, 1, 1, 1, 1, 1]

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

        if 'Mat5' in name or 'математике, 4' in name:
            translation_scale = mat4
            subtrahend = 1

        elif 'Mat6' in name or 'математике, 5' in name:
            translation_scale = mat5
            subtrahend = 1

        elif 'Mat7' in name or 'математике, 6' in name:
            translation_scale = mat6
            subtrahend = 1

        elif 'Mat8' in name or 'математике, 7' in name:
            translation_scale = mat7
            subtrahend = 1

        elif 'Mat9' in name or 'математике, 8' in name:
            translation_scale = mat8
            subtrahend = 1

        elif 'Rus5' in name or 'русскому языку, 4' in name:
            translation_scale = rus4
            subtrahend = 2

        elif 'Rus6' in name or 'русскому языку, 5' in name:
            translation_scale = rus5
            subtrahend = 2

        elif 'Rus7' in name or 'русскому языку, 6' in name:
            translation_scale = rus6
            subtrahend = 2

        elif 'Rus8' in name or 'русскому языку, 7' in name:
            translation_scale = rus7
            subtrahend = 2

        elif 'Rus9' in name or 'русскому языку, 8' in name:
            translation_scale = rus8
            subtrahend = 2

        elif 'Fra8' in name or 'французскому языку, 7' in name:
            translation_scale = fra7

        elif 'французскому языку, 11' in name:
            translation_scale = fra11

        elif 'Nem8' in name or 'немецкому языку, 7' in name:
            translation_scale = nem7

        elif 'немецкому языку, 11' in name:
            translation_scale = nem11

        elif 'Fiz8' in name or 'физике, 7' in name:
            translation_scale = fiz7

        elif 'Fiz9' in name or 'физике, 8' in name:
            translation_scale = fiz8

        elif 'физике, 11' in name:
            translation_scale = fiz11

        elif 'Obsh7' in name or 'обществознанию, 6' in name:
            translation_scale = obsh6

        elif 'Obsh8' in name or 'обществознанию, 7' in name:
            translation_scale = obsh7

        elif 'Obsh9' in name or 'обществознанию, 8' in name:
            translation_scale = obsh8

        elif 'Bio6' in name or 'биологии, 5' in name:
            translation_scale = bio5

        elif 'Bio7' in name or 'биологии, 6' in name:
            translation_scale = bio6

        elif 'Bio8' in name or '(по образцу 7 класса)' in name:
            translation_scale = bio7

        elif '(по образцу 8 класса)' in name:
            translation_scale = bio8

        elif 'Bio9' in name or 'биологии, 8' in name:
            translation_scale = bio8

        elif 'биологии, 11' in name:
            translation_scale = bio11

        elif 'Geo7' in name or 'географии, 6' in name:
            translation_scale = geo6

        elif 'Geo8' in name or 'географии, 7' in name:
            translation_scale = geo7

        elif 'Geo9' in name or 'географии, 8' in name:
            translation_scale = geo8

        elif 'географии, 10' in name:
            translation_scale = geo10

        elif 'географии, 11' in name:
            translation_scale = geo11

        elif 'Eng8' in name or "английскому языку, 7 класс" in name:
            translation_scale = eng7

        elif 'английскому языку, 11' in name:
            translation_scale = eng11

        elif 'Him9' in name or 'химии, 8' in name:
            translation_scale = him8

        elif 'химии, 11' in name:
            translation_scale = him11

        elif 'Ist6' in name or 'истории, 5' in name:
            translation_scale = ist5

        elif 'Ist7' in name or 'истории, 6' in name:
            translation_scale = ist6

        elif 'Ist8' in name or 'истории, 7' in name:
            translation_scale = ist7

        elif 'Ist9' in name or 'истории, 8' in name:
            translation_scale = ist8

        elif 'истории, 11' in name:
            translation_scale = ist11

        elif 'окру' in name:
            translation_scale = om4

        return translation_scale, subj_name, subtrahend
