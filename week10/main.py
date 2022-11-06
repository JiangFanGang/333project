import tkinter as tk
from tkinter import *
from tkinter import messagebox

import pymssql

server="titan.csse.rose-hulman.edu"
user="SodaBaseUsercaiy"
password1="Password123"
database="10_MealPlan"

username=""
name=""
userpassword=""

def callsp(spname, args):
    print(spname, args)
    try:
        with pymssql.connect(server, user, password1, database) as conn:
            with conn.cursor(as_dict=True) as cursor:
                # cursor = conn.cursor(as_dict=True)
                cursor.callproc(spname, args)
                r = []
                for row in cursor:
                    r.append(row)
                    # print(row)
                conn.commit()
                print("finish stored procedure")
                # cnt=cursor.fetchall()
                # print(r)

                if r:
                    # return query
                    return r
                else:
                    # successfully run without error but no return
                    return 1

    except pymssql._pymssql.DatabaseError as e:
        print("DatabaseError on stored procedure \"", spname, "\" with args", args)
        print(e)
        error = (str(e) + "b\'DB-Lib").split("b\'")[1]
        error = error.split("DB-Lib")[0]
        messagebox.showerror('error', error)
    except pymssql._mssql.MSSQLDatabaseException as e:
        print("MSSQLDatabaseException on stored procedure \"", spname, "\" with args", args)
        error = (str(e) + "b\'DB-Lib").split("b\'")[1]
        error = error.split("DB-Lib")[0]
        messagebox.showerror('error', error)
    except:
        print("Unknown error on stored procedure \"", spname, "\" with args", args)
        messagebox.showerror('error', "error")
    # run with error
    return False

def editFoodDialog():
    def editFoodOnClick(foodName, newFoodName, newInstruction):
        # print(foodName, newFoodName, newInstruction)
        callsp("edit_food", (foodName, newFoodName, newInstruction))
        dialog.destroy()

    def deleteFoddOnClick(foodName):
        callsp("delete_food", (foodName,))
        dialog.destroy()


    dialog = tk.Toplevel()
    dialog.geometry("500x150")

    # instruction label - food
    foodLabel = tk.Label(dialog, text = "chose a food that you would like to edit")
    foodLabel.grid(column = 0 , row = 0)

    # option menu
    editableFood = callsp("getFoodNotOnPlan", ())
    chooseList = []
    for item in editableFood:
        chooseList.append(item["name"])
    inputFoodName = tk.StringVar(dialog, "food")
    shooseFoodMenu = tk.OptionMenu(dialog, inputFoodName, *chooseList)
    shooseFoodMenu.grid(column = 1, row = 0)

    # instruction label - newFood
    newFoodLabel = tk.Label(dialog, text = "new foodName")
    newFoodLabel.grid(column = 0, row = 1)

    #input new food name
    inputNewFoodName = tk.Entry(dialog)
    inputNewFoodName.grid(column = 1, row = 1)

    newInstructionLabel = tk.Label(dialog, text = "new instruction")
    newInstructionLabel.grid(column = 0, row = 2)

    inputNewInstruction = tk.Entry(dialog)
    inputNewInstruction.grid(column = 1, row =2)

    tk.Button(dialog, text = "edit", command = lambda: editFoodOnClick(inputFoodName.get(), inputNewFoodName.get(), inputNewInstruction.get())).grid(column = 0, row = 3)
    tk.Button(dialog, text = "delete",command = lambda: deleteFoddOnClick(inputFoodName.get())).grid(column = 1, row = 3)




username = "jiangy10"
window = tk.Tk()
window.geometry("300x200")
tk.Button(window, text = "edit an existing food",command = editFoodDialog).pack()
tk.Button(window, text = "edit an existing ingredient").pack()
window.mainloop()