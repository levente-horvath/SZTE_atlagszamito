import tkinter as tk
from tkinter import ttk
from tkinter import messagebox  

file = open("atlag.txt")
l = []
for i in file:
    l.append(i.strip().split("\t")[1:3] + [5])  
file.close()

root = tk.Tk()
root.title("SZTE Átlagszámító")

def on_double_click(event):
    item = tree.identify('item', event.x, event.y)
    column = tree.identify_column(event.x)
    if item and column in ('#3', '#2', '#1'):  
        entry_edit = tk.Entry(root, width=10)
        if column == '#3':  
            entry_edit.insert(0, tree.item(item, 'values')[2])  
        elif column == '#2':  
            entry_edit.insert(0, tree.item(item, 'values')[1])  
        else:  
            entry_edit.insert(0, tree.item(item, 'values')[0])  

        def save_edit(event=None):  
            tree.set(item, column=column, value=entry_edit.get())  
            entry_edit.destroy()

        entry_edit.bind('<Return>', save_edit)

        entry_edit.bind('<FocusOut>', lambda e: save_edit())

        x, y, width, height = tree.bbox(item, column)
        entry_edit.place(x=x, y=y, width=width, height=height)
        entry_edit.focus()


def add_row():
    default_values = ('New Tárgy', 'New Kredit', 'New Jegy')
    tree.insert('', tk.END, values=default_values)



def get_treeview_data():
    data_list = []
    for item in tree.get_children():
        item_data = tree.item(item, 'values')
        data_list.append(item_data)
    return data_list





def show_message():
    treeview_data = get_treeview_data()
    kreditek = []
    jegyek = []
    for i in treeview_data:
        kreditek.append(i[1])
        jegyek.append(i[2])

    kreditek = list(map(int, kreditek))
    jegyek = list(map(int, jegyek))

    #Súlyozott tanulmányi
    Grade_pont_avg = 0
    c = 0
    for i in range(len(kreditek)):
        if jegyek[i] > 1:
            Grade_pont_avg += jegyek[i]*kreditek[i]
            c += kreditek[i]
    Grade_pont_avg = Grade_pont_avg/c
    
    #KreditIndex
    credit_index = 0
    for i in range(len(kreditek)):
        if jegyek[i] > 1:
            credit_index += jegyek[i]*kreditek[i]
    credit_index = credit_index/30


    print(c)
    #KKI - Korrigált KreditIndex
    corrected_credit_index = 0
    for i in range(len(kreditek)):
        if jegyek[i] > 1:
            corrected_credit_index += jegyek[i]*kreditek[i]
    corrected_credit_index = corrected_credit_index/(30*(c/sum(kreditek)))
    


    sg = f"Súlyozott tanulmányi átlag: {round(Grade_pont_avg, 2)} \n Kreditindex: {round(credit_index, 2)} \n Korrigált Kredindex: {round(corrected_credit_index, 2)}"
    
    messagebox.showinfo("Az Átlagok", sg)

tree = ttk.Treeview(root, columns=('Value1', 'Value2', 'Value3'), show='headings')
tree.heading('Value1', text='Tárgy')
tree.heading('Value2', text='Kredit')
tree.heading('Value3', text='Jegy')

for item in l:
    tree.insert('', tk.END, values=item)

tree.bind('<Double-1>', on_double_click)

tree.pack(expand=True, fill='both')

add_button = tk.Button(root, text="Add New Row", command=add_row)
add_button.pack(side=tk.TOP, pady=10)

message_button = tk.Button(root, text="Show Message", command=show_message)
message_button.pack(side=tk.TOP, pady=5)

root.mainloop()
