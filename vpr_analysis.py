import pandas as pd
import matplotlib.pyplot as plt


class VPR:
    def __init__(self, file_name):
        self.translation_scale, self.subj_name, self.subtrahend = self.get_balls(file_name)

        try:
            self.df = pd.read_excel(file_name)
        except Exception:
            self.df = pd.read_csv(file_name, sep=";")

        self.data_preprocessing()
        self.logins_df = pd.read_excel("excel/logins.xlsx")

    def data_preprocessing(self):
        try:
            self.df = self.df[self.df['вариант'] != 'отсутствовал']
            for char in ["0", "1", "2", "X"]:
                self.df = self.df[self.df['Учебник'] != char]
        except Exception:
            self.df = self.df[self.df['var-1'] != 'отсутствовал']
            self.df = self.df.rename(columns={"user": "логин школы", "sum": "всего баллов"})
            self.add_region()
            self.df = self.df[["всего баллов", "логин школы", "регион"]]

    def get_unic_schools(self):
        return [school for school in self.df["логин школы"].drop_duplicates()]

    def get_schools_and_liters(self):
        dictionary = {}
        for index, row in self.df[["логин школы", "класс"]].drop_duplicates().iterrows():

            if dictionary.get(row["логин школы"]) is None:
                dictionary[row["логин школы"]] = [row["класс"]]
            else:
                dictionary[row["логин школы"]].append(row["класс"])
        return dictionary
    def get_book_for_class(self, school_login, liter):
        pass
    def add_region(self):
        self.df["регион"] = self.df.apply(lambda x: self.find_region(x['логин школы']), axis=1)

    def get_basemark(self, value):
        if value - self.subtrahend <= self.translation_scale[0]:
            return 2
        elif (value - self.subtrahend >= self.translation_scale[1]) and (
                value - self.subtrahend <= self.translation_scale[4]):
            return 4
        elif value - self.subtrahend >= self.translation_scale[5]:
            return 5

    def get_realmark(self, value):
        if value <= self.translation_scale[0]:
            return 2
        elif value >= self.translation_scale[1] and value <= self.translation_scale[2]:
            return 3
        elif value >= self.translation_scale[3] and value <= self.translation_scale[4]:
            return 4
        elif value >= self.translation_scale[5]:
            return 5

    def get_school_count_for_region(self, region_name):
        df = self.df[self.df["регион"] == region_name]
        return len(df["логин школы"].drop_duplicates())

    def convert_all_score_to_baseMarks(self):
        self.df["Оценка"] = self.df.apply(lambda x: self.get_basemark(x['всего баллов']), axis=1)

    def convert_all_score_to_realMarks(self):
        self.df["Оценка"] = self.df.apply(lambda x: self.get_realmark(x['всего баллов']), axis=1)

    def get_df_with_mark(self, mark):
        return self.df[self.df['Оценка'] == mark]

    def convert_column(self, df, by, base):
        df = df.groupby([by]).count()
        df = df["Оценка"].reset_index()
        df = df.rename(columns={"Оценка": base})
        return df

    def merge_data_frames(self, *args):
        df = args[0]
        for df_ in args[1:-1]:
            df = df.merge(df_, on=args[-1], how='outer')
        return df.fillna(0)

    def find_school_name(self, school):
        return self.logins_df.loc[self.logins_df["логин"] == school].iloc[0]['имя']

    def find_region(self, school):
        return self.logins_df.loc[self.logins_df["логин"] == school].iloc[0]['регион']

    def rename_schools(self, df):
        df["логин школы"] = df.apply(lambda x: self.find_school_name(x['логин школы']), axis=1)
        return df

    def get_counts_for_regions(self):
        counts = self.df['регион'].value_counts()
        counts = counts.reset_index()
        counts = counts.rename(columns={"index": "регион", "регион": "Кол-во участников"})
        counts["Кол-во ОО"] = counts.apply(lambda x: self.get_school_count_for_region(x['регион']), axis=1)
        return counts

    def get_counts_for_schools(self):
        counts = self.df['логин школы'].value_counts()
        counts = counts.reset_index()
        counts = counts.rename(columns={"index": "логин школы", "логин школы": "Кол-во участников"})
        return counts

    def get_base_information_for_schools(self):
        self.convert_all_score_to_baseMarks()
        counts_for_schools = self.get_counts_for_schools()
        below_baseline = self.convert_column(self.get_df_with_mark(2), "логин школы", "Ниже базового")
        baseline = self.convert_column(self.get_df_with_mark(4), "логин школы", "Базовый")
        above_baseline = self.convert_column(self.get_df_with_mark(5), "логин школы", "Выше базового")
        school_logins_with_region = self.df[["логин школы", "регион"]].drop_duplicates()
        base_information_for_schools = self.merge_data_frames(counts_for_schools,
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
        self.convert_all_score_to_realMarks()
        counts_for_schools = self.get_counts_for_schools()
        result_with_2 = self.convert_column(self.get_df_with_mark(2), "логин школы", "2")
        result_with_3 = self.convert_column(self.get_df_with_mark(3), "логин школы", "3")
        result_with_4 = self.convert_column(self.get_df_with_mark(4), "логин школы", "4")
        result_with_5 = self.convert_column(self.get_df_with_mark(5), "логин школы", "5")
        school_logins_with_region = self.df[["логин школы", "регион"]].drop_duplicates()
        real_information_for_schools = self.merge_data_frames(counts_for_schools,
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
        self.convert_all_score_to_baseMarks()
        counts_for_regions = self.get_counts_for_regions()
        below_baseline = self.convert_column(self.get_df_with_mark(2), "регион", "Ниже базового")
        baseline = self.convert_column(self.get_df_with_mark(4), "регион", "Базовый")
        above_baseline = self.convert_column(self.get_df_with_mark(5), "регион", "Выше базового")
        base_information_for_regions = self.merge_data_frames(counts_for_regions,
                                                              below_baseline,
                                                              baseline,
                                                              above_baseline, "регион")
        cols = ["Ниже базового", "Базовый", "Выше базового"]
        base_information_for_regions[cols] = round(
            base_information_for_regions[cols].div(base_information_for_regions[cols].sum(axis=1), axis=0).multiply(
                100), 2)
        return base_information_for_regions

    def get_real_information_for_regions(self):
        self.convert_all_score_to_realMarks()
        counts_for_regions = self.get_counts_for_regions()
        result_with_2 = self.convert_column(self.get_df_with_mark(2), "регион", "2")
        result_with_3 = self.convert_column(self.get_df_with_mark(3), "регион", "3")
        result_with_4 = self.convert_column(self.get_df_with_mark(4), "регион", "4")
        result_with_5 = self.convert_column(self.get_df_with_mark(5), "регион", "5")
        real_information_for_regions = self.merge_data_frames(counts_for_regions,
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

    def get_balls(self, name):
        fullname = ""
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
            fullname = "Математика 4 класс"
            subtrahend = 1
        elif 'Mat6' in name or 'математике, 5' in name:
            translation_scale = mat5
            fullname = "Математика 5 класс"
            subtrahend = 1
        elif 'Mat7' in name or 'математике, 6' in name:
            translation_scale = mat6
            fullname = "Математика 6 класс"
            subtrahend = 1
        elif 'Mat8' in name or 'математике, 7' in name:
            translation_scale = mat7
            fullname = "Математика 7 класс"
            subtrahend = 1
        elif 'Mat9' in name or 'математике, 8' in name:
            translation_scale = mat8
            fullname = "Математика 8 класс"
            subtrahend = 1


        elif 'Rus5' in name or 'русскому языку, 4' in name:
            translation_scale = rus4
            fullname = "Русский язык 4 класс"
            subtrahend = 2
        elif 'Rus6' in name or 'русскому языку, 5' in name:
            translation_scale = rus5
            fullname = "Русский язык 5 класс"
            subtrahend = 2
        elif 'Rus7' in name or 'русскому языку, 6' in name:
            translation_scale = rus6
            fullname = "Русский язык 6 класс"
            subtrahend = 2
        elif 'Rus8' in name or 'русскому языку, 7' in name:
            translation_scale = rus7
            fullname = "Русский язык 7 класс"
            subtrahend = 2
        elif 'Rus9' in name or 'русскому языку, 8' in name:
            translation_scale = rus8
            fullname = "Русский язык 8 класс"
            subtrahend = 2


        elif 'Fra8' in name or 'французскому языку, 7' in name:
            translation_scale = fra7
            fullname = "Французский язык 7 класс"
        elif 'французскому языку, 11' in name:
            translation_scale = fra11
            fullname = "Французский язык 11 класс"


        elif 'Nem8' in name or 'немецкому языку, 7' in name:
            translation_scale = nem7
            fullname = "Немецкий язык 7 класс"
        elif 'немецкому языку, 11' in name:
            translation_scale = nem11
            fullname = "Немецкий язык 11 класс"


        elif 'Fiz8' in name or 'физике, 7' in name:
            translation_scale = fiz7
            fullname = "Физика 7 класс"
        elif 'Fiz9' in name or 'физике, 8' in name:
            translation_scale = fiz8
            fullname = "Физика 8 класс"
        elif 'физике, 11' in name:
            translation_scale = fiz11
            fullname = "Физика 11 класс"


        elif 'Obsh7' in name or 'обществознанию, 6' in name:
            translation_scale = obsh6
            fullname = "Обществознание 6 класс"
        elif 'Obsh8' in name or 'обществознанию, 7' in name:
            translation_scale = obsh7
            fullname = "Обществознание 7 класс"
        elif 'Obsh9' in name or 'обществознанию, 8' in name:
            translation_scale = obsh8
            fullname = "Обществознание 8 класс"


        elif 'Bio6' in name or 'биологии, 5' in name:
            translation_scale = bio5
            fullname = "Биология 5 класс"
        elif 'Bio7' in name or 'биологии, 6' in name:
            translation_scale = bio6
            fullname = "Биология 6 класс"
        elif 'Bio8' in name or '(по образцу 7 класса)' in name:
            translation_scale = bio7
            fullname = "Биология 7 класс"
        elif '(по образцу 8 класса)' in name:
            translation_scale = bio8
            fullname = "Биология 7 класс(по образцу 8 класса)"
        elif 'Bio9' in name or 'биологии, 8' in name:
            translation_scale = bio8
            fullname = "Биология 8 класс"
        elif 'биологии, 11' in name:
            translation_scale = bio11
            fullname = "Биология 11 класс"


        elif 'Geo7' in name or 'географии, 6' in name:
            translation_scale = geo6
            fullname = "География 6 класс"
        elif 'Geo8' in name or 'географии, 7' in name:
            translation_scale = geo7
            fullname = "География 7 класс"
        elif 'Geo9' in name or 'географии, 8' in name:
            translation_scale = geo8
            fullname = "География 8 класс"
        elif 'географии, 10' in name:

            translation_scale = geo10
            fullname = "География 10 класс"
        elif 'географии, 11' in name:

            translation_scale = geo11
            fullname = "География 11 класс"

        elif 'Eng8' in name or "английскому языку, 7 класс" in name:

            translation_scale = eng7
            fullname = "Английский язык 7 класс"
        elif 'английскому языку, 11' in name:

            translation_scale = eng11
            fullname = "Английский язык 11 класс"


        elif 'Him9' in name or 'химии, 8' in name:

            translation_scale = him8
            fullname = "Химия 8 класс"
        elif 'химии, 11' in name:

            translation_scale = him11
            fullname = "Химия 11 класс"

        elif 'Ist6' in name or 'истории, 5' in name:

            translation_scale = ist5
            fullname = "История 5 класс"
        elif 'Ist7' in name or 'истории, 6' in name:

            translation_scale = ist6
            fullname = "История 6 класс"
        elif 'Ist8' in name or 'истории, 7' in name:

            translation_scale = ist7
            fullname = "История 7 класс"
        elif 'Ist9' in name or 'истории, 8' in name:

            translation_scale = ist8
            fullname = "История 8 класс"
        elif 'истории, 11' in name:
            translation_scale = ist11
            fullname = "История 11 класс"


        elif 'окру' in name:
            translation_scale = om4
            fullname = "Окружающий мир 4 класс"

        return translation_scale, fullname, subtrahend

# vpr = VPR("excel/vpr_results/10/Проведение работы по географии, 10 класс. ВПР 2021.xlsx")
# print(vpr.get_schools_and_liters())