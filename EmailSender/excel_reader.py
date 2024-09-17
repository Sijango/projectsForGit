import pandas as pd


class ExcelReader:
    df_from_excel: pd.DataFrame
    df_result: pd.DataFrame
    status: bool = False
    file_name: str
    SHEET_NAME: str = "Контрагенты"
    REQUIRED_COLUMNS = ["ФИО руководителя", "Электронная почта"]

    def __init__(self, file_name: str):
        self.file_name = file_name

    def initial_dataframe(self):
        try:
            self.df_from_excel = pd.read_excel(self.file_name, sheet_name=self.SHEET_NAME, engine="openpyxl")
            return True, ""
        except FileNotFoundError:
            return False, f"Файл {self.file_name} не найден!"
        except ValueError:
            return False, f"Лист {self.SHEET_NAME} не найден в файле {self.file_name}!"

    def start(self):
        missing_columns = [col for col in self.REQUIRED_COLUMNS if col not in self.df_from_excel.columns]
        if missing_columns:
            return False, f"Отсутствуют необходимые столбцы: {', '.join(missing_columns)}"

        self.df_result = self.df_from_excel[self.REQUIRED_COLUMNS]
        return True, self.df_result


if __name__ == "__main__":
    file_path = "data/Перечень для рассылки.xlsx"
    converter = ExcelReader(file_path)

    status, error_msg = converter.initial_dataframe()
    if not status:
        print(error_msg)
        exit()

    status, df = converter.start()
    if not status:
        print(df)
        exit()

    print(df)
