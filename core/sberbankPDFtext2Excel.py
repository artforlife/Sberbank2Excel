"""
*********************************************
при использовании из командной строки
*********************************************


Программа не читает PDF файл непосредственно. Сначала надо скофертировать выписку Сбербанка в текстовый формат утилитой pdf2txtev


*********************************************
при использовании в качестве модуля
*********************************************
Надо использовать функцию sberbankPDFtext2Excel()
"""

import sys
import os

# importing own modules out of project
import pandas as pd

from core import utils
from extactors_generic import determine_extractor

def sberbankPDFtext2Excel(input_txt_file_name:str,output_excel_file_name:str=None, format='auto') -> str:
    """
    Функция конвертирует текстовый файл Сбербанка, полученный из выписки PDF помощью конвертации Foxit PDF reader в Excel формат
    Если output_excel_file_name не задан, то он создаётся из input_txt_file_name путём замены расширения файла на xlsx
    """

    # creating output file name for Excel file, if not provided
    if not output_excel_file_name:
        pre, ext = os.path.splitext(input_txt_file_name)
        output_excel_file_name = pre+'.xlsx'

    # считываем входной файл в текст
    with open(input_txt_file_name, encoding="utf8") as file:
        file_text = file.read()

    if format=='auto':
        extractor_type = determine_extractor(file_text)
        print(r"Формат файла определён как " + extractor_type.__name__)

    #TODO: update this function for the sitiation, when the format is provided
    else:
        print(r"Конвертируем файл как формат "+format)

    # in thi case extractor_type is not a function, but a class
    # if you call it like this extractor_type() it returns an object with the type of extractor_type
    extractor = extractor_type(file_text)

    # extracting entries (operations) from big text to list of dictionaries
    individual_entries = extractor.get_entries()

    # converting list of dictionaries to pandas dataframe
    df = pd.DataFrame(individual_entries)

    # getting balance, written in the bank statement
    extracted_balance = extractor.get_period_balance()

    # checking, if balance, extracted from text file is equal to the balance, found by summing column in Pandas dataframe
    utils.check_transactions_balance(df, extracted_balance, extractor.get_column_name_for_balance_calculation())

    # Defining header in Russian.  
    # russian_headers = [
    #     'Дата операции',
    #     'дата обработки',
    #     'код авторизации',
    #     'Описание операции',
    #     'категория',
    #     'Сумма в валюте счёта',
    #     'cумма в валюте операции',
    #     'валюта операции',
    #     'Остаток по счёту в валюте счёта']
   
    # Сохраняем pandas в Excel
    # utils.pd_to_Excel(df, russian_headers, output_excel_file_name)

    writer = pd.ExcelWriter(output_excel_file_name,
                            engine='xlsxwriter',
                            datetime_format='dd.mm.yyyy HH:MM')

    df.to_excel(writer, sheet_name='Sheet1', index=False)

    writer.close()

    return output_excel_file_name

# TODO: Add menu to be able to provide several arguments
def main():
    if len(sys.argv) < 2:
        print('Недостаточно аргументов')
        print(__doc__)
        return None
    
    elif len(sys.argv)==2:
        outputFileName = None

    elif len(sys.argv)==3:
        outputFileName=sys.argv[2]

    sberbankPDFtext2Excel(sys.argv[1], outputFileName)


if __name__=='__main__':
    main()