import sys
import os
from typing import Union
import argparse

import exceptions
import extractors
from pdf2txtev import pdf_2_txt_file
from sberbankPDFtext2Excel import sberbankPDFtext2Excel, genarate_PDFtext2Excel_argparser





def sberbankPDF2Excel(input_file_name:str,
                      output_file_name:Union[str, None] =None,
                      format:str= 'auto',
                      leave_intermediate_txt_file:str = False,
                      perform_balance_check = True,
                      output_file_type:str="xlsx") ->str:
    """
    function converts pdf or text file with Sperbank extract to Excel or CSV format
    input_file_name:
    output_excel_file_name:
    format: str - format of the Sberbank extract. If "auto" then tool tryes to work out the format itself
    leave_intermediate_txt_file: if True, does not delete intermediate txt file
    """

    print(f"{format=}")

    print("*"*30)
    print("Конвертируем файл " + input_file_name)

    path, extension = os.path.splitext(input_file_name)

    extension = extension.lower()

    if extension == ".pdf":
        tmp_txt_file_name = os.path.splitext(input_file_name)[0] + ".txt"

    elif extension == ".txt":
        tmp_txt_file_name = input_file_name

    else:
        raise exceptions.InputFileStructureError("Неподдерживаемое расширение файла: "+ extension)


    if not output_file_name:
        output_file_name = path 

    try:
        if extension == ".pdf":
            pdf_2_txt_file(input_file_name, tmp_txt_file_name)

        result = sberbankPDFtext2Excel(tmp_txt_file_name,
                                       output_file_name,
                                       format=format,
                                       perform_balance_check = perform_balance_check,
                                       output_file_type=output_file_type)

        if (not leave_intermediate_txt_file) and (not extension == ".txt"):
            os.remove(tmp_txt_file_name)

    except:
        raise


    return result


def main():

    parser = argparse.ArgumentParser(description='Конвертация выписки банка из формата PDF или из промежуточного текстового файла в формат Excel или CSV.',
                                        parents=[genarate_PDFtext2Excel_argparser()])
   
    parser.add_argument('-i','--interm', action='store_true', default=False, dest='leave_intermediate_txt_file', help='Не удалять промежуточный текстовый файт')

    args = parser.parse_args()

    print(args)

    sberbankPDF2Excel(input_file_name = args.input_file_name,
                      output_file_name = args.output_Excel_file_name,
                      format = args.format,
                      leave_intermediate_txt_file = args.leave_intermediate_txt_file,
                      perform_balance_check = args.perform_balance_check,
                      output_file_type=args.output_file_type)

if __name__ == '__main__':
    main()