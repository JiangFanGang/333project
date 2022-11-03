import tkinter as tk
from tkinter import ttk, messagebox,simpledialog
import pymssql
import hashlib


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

# def login(username, password):
#     password = hashlib.sha256(password.encode('utf-8')).hexdigest()
#
#     r=callsp("exist_Person",(username_str,password_str))
#     if r and r!=1:
#         print("successfully log in with",r)
#         username=username
#         userpassword=password_str
#         name=r[0]["name"]
#         generateMealPlan(username)
#     else:
#         messagebox.showerror('error',"not exist user or incorrect password")
#
#
# def SignUp(username, password):
#     return 0
    

def generateMealPlan(username):

    
    def loadFoodToPlan(food, type, ingredient, createdDate):
        plan.insert("",0, text = food, values = (type, ingredient, createdDate))

    def updatePlan():
        for item in plan.get_children():
            plan.delete(item)
        allfood = callsp("get_personFood", (username,))
        if allfood and allfood != 1:
            for food in allfood:
                foodingredient = callsp("get_foodIngredient", (food["FoodName"],))
                ingredients = [i["IngredientName"] for i in foodingredient]
                loadFoodToPlan(food["FoodName"], food["type"], ingredients, food["date"])

        
    def addFoodDialog():
        def addToPlan():
            # print(inputFood.get())
            callsp("addFoodToMealPlan", (username, inputFood.get(), inputType.get(),))
            updatePlan()
            add.destroy()
        def cancel():
            add.destroy()

        add = tk.Toplevel(window)
        add.title("Add a Food to Meal Plan")
        add.geometry("400x100")

        typeLable = tk.Label(add, text="select a type")
        typeLable.grid(column=0, row=0)
        inputType = tk.StringVar(add)
        inputType.set("Type")
        types = ["break first", "lunch", "dinner", "other"]
        typeList = tk.OptionMenu(add, inputType, *types)
        typeList.grid(column = 1, row = 0)

        addLable = tk.Label(add, text = "choose the Food You would like to add")
        addLable.grid(column = 0, row = 1)
        inputFood = tk.StringVar(add)
        inputFood.set("Food")
        foodList = callsp("get_Food",())
        choice = []
        for food in foodList:
            choice.append(food["name"])
        chooseList = tk.OptionMenu(add,inputFood, *choice)
        chooseList.grid(column = 1, row = 1)
        ttk.Button(add, text="confirm Addition", command = addToPlan).grid(column=0, row=2)
        ttk.Button(add, text="Cancel", command = cancel).grid(column=1, row=2)
        add.mainloop()

    def editFoodDialog():
        def editFood():
            callsp("editFoodOnPlan",(username, inputFood.get(), inputChangeTo.get(),))
            updatePlan()
            edit.destroy()
        def deleteFood():
            callsp("deleteFoodOnPlan",(username, inputFood.get(),))
            updatePlan()
            edit.destroy()
        edit = tk.Toplevel(window)
        edit.title("Edit a Food to Meal Plan")
        edit.geometry("400x150")
        chooseEdit = tk.Label(edit, text="Choose the Food you would like to edit")
        chooseEdit.grid(column = 0, row = 0)
        editTo = tk.Label(edit, text="Choose the Food you would like it to be")
        editTo.grid(column = 0, row = 1)
        inputFood = tk.StringVar(edit)
        inputFood.set("Food")
        inputChangeTo = tk.StringVar(edit)
        inputChangeTo.set("Food")
        userFood = callsp("get_personFood",(username,))
        choice = []
        for food in userFood:
            choice.append(food["FoodName"])
        chooseList = tk.OptionMenu(edit, inputFood, *choice)
        chooseList.grid(column = 1, row = 0)
        changeTo = []
        food = callsp("get_Food",())
        for item in food:
            changeTo.append(item["name"])
        foodList = tk.OptionMenu(edit, inputChangeTo, *changeTo)
        foodList.grid(column = 1, row = 1)
        ttk.Button(edit, text = "Update Edit",command = editFood).grid(column = 0 ,row = 2)
        ttk.Button(edit, text = "Delete this Food", command = deleteFood).grid(column = 1 ,row = 2)
        edit.mainloop()


    def createFoodDialog():
        def notContain(list, item):
            for i in list:
                if i == item:
                    return False
            return True

        def addIngredient(col, list):
            if notContain(list, inputIngredient.get()):
                addedIngredient = tk.Label(createFood, text = inputIngredient.get())
                addedIngredient.grid(column = col[0], row = 2)
                col[0] += 1
                list.append(inputIngredient.get())

        def createFoodOnclick(food, ingredient, instruction):
            callsp("insert_Food",(food, instruction,))#create a food name with instruction
            for item in ingredient:
                callsp("insert_IsIngredientOf",(food, item,))
            createFood.destroy()



        createFood = tk.Toplevel(window)
        createFood.title("create food")
        createFood.geometry("400x200")
        foodName = tk.Label(createFood, text="foodName")
        foodName.grid(column = 0, row = 0)
        inputFoodName = tk.Entry(createFood)
        inputFoodName.grid(column = 1, row = 0)
        availableIngredient = []
        ingredientList = callsp("get_Ingredient",())
        for item in ingredientList:
            availableIngredient.append(item["name"])
        inputIngredient = tk.StringVar()
        inputIngredient.set("ingredient")
        chooseIngredientList = tk.OptionMenu(createFood, inputIngredient, *availableIngredient)
        col = [0]
        chosenIngredient = []
        chooseIngredientList.grid(column = 0, row = 1)
        instructionLabel = tk.Label(createFood, text = "instruction")
        instructionLabel.grid(column = 0, row = 3)
        inputInstruction = tk.Entry(createFood)
        inputInstruction.grid(column = 1, row = 3)
        tk.Button(createFood, text = "add", command = lambda:addIngredient(col, chosenIngredient)).grid(column = 1, row = 1)
        tk.Button(createFood, text = "create", command = lambda: createFoodOnclick(inputFoodName.get(),chosenIngredient,inputInstruction.get())).grid(column = 1, row = 4)





    def createIngredientDialog():
        def createIngredientOnClick(ingredient):
            callsp("insert_Ingredient", (ingredient,))
            createIngredient.destroy()

        createIngredient = tk.Toplevel(window)
        createIngredient.title("create ingredients")
        createIngredient.geometry("300x200")
        ingredientName = tk.Label(createIngredient, text = "ingredientName")
        ingredientName.grid(column = 0, row = 0)
        inputIngredientName = tk.Entry(createIngredient)
        inputIngredientName.grid(column = 1, row = 0)
        tk.Button(createIngredient, text = "create", command = lambda: createIngredientOnClick(inputIngredientName.get())).grid(column = 0, row =1)

        
    
    window = tk.Tk()
    window.title("My Meal Plan")
    window.geometry("700x500")
    
    plan = ttk.Treeview(window)


    plan["columns"] = ("type", "ingredient", "createdDate")
    plan.column("type", width = 100)
    plan.column("ingredient", width = 150)
    plan.column("createdDate", width = 130)
    plan.heading("type", text = "type")
    plan.heading("ingredient", text = "Ingredient")
    plan.heading("createdDate", text = "Created Date")

    allfood=callsp("get_personFood",(username,))
    if allfood and allfood!=1:
        for food in allfood:
            foodingredient=callsp("get_foodIngredient",(food["FoodName"],))
            ingredients=[i["IngredientName"] for i in foodingredient]
            loadFoodToPlan(food["FoodName"],food["type"],ingredients,food["date"])
    plan.pack()
    ttk.Button(window, text="Add Food To Meal Plan", command=addFoodDialog).pack()
    ttk.Button(window, text = "Edit current Food on the Meal Plan", command = editFoodDialog).pack()
    ttk.Button(window, text = "create food",command = createFoodDialog).pack()
    ttk.Button(window, text = "create ingredient",command = createIngredientDialog).pack()

    window.mainloop()









#main
# login = tk.Tk()
# login.title("LogIn")
# login.geometry("400x300")
# username = tk.Label(login, text = "user name")
# username_str = tk.StringVar(login)
# username_str.set("enter your username here")
# usernameEntry = tk.Entry(login,textvariable = username_str)
# password = tk.Label(login, text = "password")
# password_str = tk.StringVar(login)
# password_str.set("enter your password here")
# passwordEntry = tk.Entry(login,textvariable = password_str)
# username.grid(column = 0, row = 0)
# usernameEntry.grid(column = 1, row = 0)
# password.grid(column = 0, row = 1)
# passwordEntry.grid(column = 1, row = 1)
# ttk.Button(login, text = "login", command = generateMealPlan("2")).grid(column = 0, row = 2)
# login.mainloop()
generateMealPlan("jiangy10")



