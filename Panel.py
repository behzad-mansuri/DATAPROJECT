import pandas as pd
from data_sample import get_numpy , get_pandas
from d_visual import Visualz 
import unit_test 
import unittest
while True:
    print("Welcome to Earthquake data analysis in Japan")
    print("1.Get csv files")
    print("2.Pandas & Numpy")
    print("3.Storing data in SQL database")
    print("4.Data visualization")
    print("5.Unittest and validation")
    print("6.Exit")
    print("Please enter a number:")
    n = input()

    if n == "1":
        #کد نازیلا
        print("Please enter 1 to return or 0 to exit" )
        a = input()
        if a == "0":
            break
        elif a == "1":
            df_geofon = pd.read_csv('JAPAN_GEOFON.csv')
            df_usgs = pd.read_csv('JAPAN_USGS.csv')
            print(df_geofon , df_usgs)

    elif n == "2":
        while True:
            print("Please enter a package (Numpy/Pandas) or 1 to return:")
            name = input()
            if name == "1":
                break
            elif name.lower() == "numpy":
                #بخش اول کد محمدمهدی
                print("Please enter 1 to return or 0 to show panel" )
                a = input()
                if a == "0":
                    break
                elif a == "1":
                    get_numpy()
            elif name.lower() == "pandas":
                #بخش دوم کد محمدمهدی
                print("Please enter 1 to return or 0 to show panel" )
                a = input()
                if a == "0":
                    break
                elif a == "1":
                    get_pandas()
            else:
                print("Wrong package!")
                print("Please enter 1 to return or 0 to exit" )
                a = input()
                if a == "0":
                    break
                elif a == "1":
                    continue
    elif n == "3":
        # کد بخش ذخیره سازی در sql
        print("Please enter 1 to return or 0 to exit" )
        a = input()
        if a == "0":
            break
        elif a == "1":
            excel_file_path = "earthquake_analysis.xlsx"
            df = pd.read_excel(excel_file_path)
            print(df)
    
    elif n == "4":
        while True:
            print("Please Please enter the number corresponding to the chart type:")
            print("1.Return")
            print("2.Histogram")
            print("3.Line chart")
            print("4.Scatter plot")
            print("5.Boxplot")
            name = input()

            df_usgs = pd.read_csv('JAPAN_USGS.csv')
            df_geofon = pd.read_csv('JAPAN_GEOFON.csv')
            vis = Visualz(df_usgs , df_geofon)
            if name == "1":
                break
            elif name == "2":
                #کد هیستوگرام
                print("Please enter 1 to return or 0 to show panel" )
                a = input()
                if a == "0":
                    break
                elif a == "1":
                    vis.hist()
            elif name == "3":
                #کد نمودار خطی
                print("Please enter 1 to return or 0 to show panel" )
                a = input()
                if a == "0":
                    break
                elif a == "1":
                    vis.line()
            elif name == "4":
                #کد نمودار پراکندگی
                print("Please enter 1 to return or 0 to show panel" )
                a = input()
                if a == "0":
                    break
                elif a == "1":
                    vis.scatter()
            elif name == "5":
                #کد نمودار باکس
                print("Please enter 1 to return or 0 to show panel" )
                a = input()
                if a == "0":
                    break
                elif a == "1":
                    vis.box()
            
            else:
                print("Wrong package!")
                print("Please enter 1 to return or 0 to show panel" )
                a = input()
                if a == "0":
                    break
                elif a == "1":
                    continue

    elif n == "5":
        # کد بخش تست نویسی
        print("Please enter 1 to return or 0 to exit" )
        a = input()
        if a == "0":
            break
        elif a == "1":
            if __name__ == '__main__':
                suite = unittest.defaultTestLoader.loadTestsFromModule(unit_test)
                runner = unittest.TextTestRunner()
                runner.run(suite)
        
    elif n == "6":
        break
    else:
        print("Wrong number!")
        print("Please type 1 to show panel or 0 to exit" )
        a = input()
        if a == "0":
            break
        elif a == "1":
            continue