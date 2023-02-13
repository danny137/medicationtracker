import tkinter as tk
import csv

from tkinter import ttk
from tkinter import messagebox
from datetime import datetime


class App(tk.Tk):
	def __init__(self):
		super().__init__()
		self.title("Medication Tracker")
		self.geometry("510x400")
		self.resizable(False, False)
		self.medications = {}
		self.doses = []
		self.read_file()
		self.create_widgets()
		self.create_tabs()
		self.create_new_delivery_tab()
		self.create_dose_tab()
		self.create_view_medications_tab()
		self.create_exit_button()
		self.create_view_doses_tab()
		self.tab_control.grid(row=0, column=0, columnspan=2, pady=10)

	def read_file(self):
		try:
			with open("medication.csv", "r") as f:
				reader = csv.reader(f)
				for row in reader:
					self.medications[row[0]] = float(row[1])
			try:
				self.create_view_medications_tab()
				self.create_new_delivery_tab()
				self.create_dose_tab()
				self.create_view_doses_tab()

			except AttributeError:
				pass
		except FileNotFoundError:
			with open("medication.csv", "w") as f:
				pass

		try:
			with open("doses.csv", "r") as f:
				reader = csv.reader(f)
				for row in reader:
					self.doses.append((row[0], row[1], row[2]))

		except FileNotFoundError:
			with open("doses.csv", "w") as f:
				pass
		
	def write_file(self):
		with open("medication.csv", "w") as f:
			writer = csv.writer(f)
			for key, value in self.medications.items():
				writer.writerow([key, value])

	def write_doses_to_file(self):
		existing_doses = set()
		try:
			with open("doses.csv", "r") as f:
				reader = csv.reader(f)
				for row in reader:
					existing_doses.add(row[2])
		except FileNotFoundError:
			pass

		with open("doses.csv", "a") as f:
			writer = csv.writer(f)
			for dose in self.doses:
				if dose[2] not in existing_doses:
					writer.writerow(dose)
					existing_doses.add(dose[2])

	def create_widgets(self):
		self.tab_control = ttk.Notebook(self)

	def create_tabs(self):
		self.new_delivery_tab = ttk.Frame(self.tab_control)
		self.dose_tab = ttk.Frame(self.tab_control)
		self.view_medications_tab = ttk.Frame(self.tab_control)
		self.view_doses_tab = ttk.Frame(self.tab_control)
		self.tab_control.add(self.new_delivery_tab, text="New Delivery")
		self.tab_control.add(self.dose_tab, text="Dose")
		self.tab_control.add(self.view_medications_tab, text="View Medications")
		self.tab_control.add(self.view_doses_tab, text="View Doses")

	def create_new_delivery_tab(self):
		self.new_delivery_tab_label = ttk.Label(self.new_delivery_tab, text="New Delivery")
		self.new_delivery_tab_label.grid(row=0, column=0, columnspan=2, pady=10)
		self.new_delivery_tab_medication_label = ttk.Label(self.new_delivery_tab, text="Medication")
		self.new_delivery_tab_medication_label.grid(row=1, column=0, pady=10)
		self.new_delivery_tab_medication_entry = ttk.Combobox(self.new_delivery_tab, values=list(self.medications.keys()))
		self.new_delivery_tab_medication_entry.grid(row=1, column=1, pady=10)
		self.new_delivery_tab_quantity_label = ttk.Label(self.new_delivery_tab, text="Quantity")
		self.new_delivery_tab_quantity_label.grid(row=2, column=0, pady=10)
		self.new_delivery_tab_quantity_entry = ttk.Entry(self.new_delivery_tab)
		self.new_delivery_tab_quantity_entry.grid(row=2, column=1, pady=10)
		self.new_delivery_tab_add_button = ttk.Button(self.new_delivery_tab, text="Add", command=self.add_delivery)
		self.new_delivery_tab_add_button.grid(row=3, column=0, columnspan=2, pady=10)

	def add_delivery(self):
		medication = self.new_delivery_tab_medication_entry.get()
		quantity = self.new_delivery_tab_quantity_entry.get()
		if medication and quantity:
			try:
				if medication in self.medications:
					self.medications[medication] += float(quantity)
				else:
					self.medications[medication] = float(quantity)
			except ValueError:
				messagebox.showerror("Error", "Please enter a valid quantity")
				return
			self.new_delivery_tab_medication_entry.delete(0, "end")
			self.new_delivery_tab_quantity_entry.delete(0, "end")
			self.write_file()
			self.read_file()
			messagebox.showinfo("Success", "Delivery added successfully")
		else:
			messagebox.showerror("Error", "Please enter a medication and quantity")

	def create_dose_tab(self):
		self.dose_tab_label = ttk.Label(self.dose_tab, text="Dose")
		self.dose_tab_label.grid(row=0, column=0, columnspan=2, pady=10)
		self.dose_tab_medication_label = ttk.Label(self.dose_tab, text="Medication")
		self.dose_tab_medication_label.grid(row=1, column=0, pady=10)
		self.dose_tab_medication_combobox = ttk.Combobox(self.dose_tab, values=list(self.medications.keys()))
		self.dose_tab_medication_combobox.config(state="readonly")
		self.dose_tab_medication_combobox.grid(row=1, column=1, pady=10)
		self.dose_tab_quantity_label = ttk.Label(self.dose_tab, text="Quantity")
		self.dose_tab_quantity_label.grid(row=2, column=0, pady=10)
		self.dose_tab_quantity_entry = ttk.Entry(self.dose_tab)
		self.dose_tab_quantity_entry.grid(row=2, column=1, pady=10)
		self.dose_tab_take_button = ttk.Button(self.dose_tab, text="Take", command=self.take_dose)
		self.dose_tab_take_button.grid(row=3, column=0, columnspan=2, pady=10)

	def take_dose(self):
		medication = self.dose_tab_medication_combobox.get()
		quantity = self.dose_tab_quantity_entry.get()
		if medication and quantity:
			if medication in self.medications:
				if self.medications[medication] >= float(quantity):
					self.medications[medication] -= float(quantity)
					if self.medications[medication] == 0:
						res = messagebox.askyesno("Warning", "You have run out of this medication. Would you like to remove it?")
						if res:
							del self.medications[medication]
							messagebox.showinfo("Success", "Medication deleted successfully")
					self.write_file()
					self.doses.append((medication, quantity, datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
					self.write_doses_to_file()
					self.read_file()
					messagebox.showinfo("Success", "Dose taken successfully")
				else:
					messagebox.showerror("Error", "Not enough medication")
			else:
				messagebox.showerror("Error", "Medication not found")
		else:
			messagebox.showerror("Error", "Please enter a medication and quantity")

	def create_view_doses_tab(self):
		self.view_doses_tab_label = ttk.Label(self.view_doses_tab, text="View Doses")
		self.view_doses_tab_label.grid(row=0, column=0, columnspan=2, pady=10)
		self.view_doses_tab_treeview = ttk.Treeview(self.view_doses_tab)
		self.view_doses_tab_treeview.grid(row=1, column=0, columnspan=2, pady=10)
		self.view_doses_tab_treeview["columns"] = ("dosequantity", "datetime",)
		self.view_doses_tab_treeview.heading("#0", text="Medication")
		self.view_doses_tab_treeview.heading("dosequantity", text="Quantity")
		self.view_doses_tab_treeview.heading("datetime", text="Datetime")
		self.view_doses_tab_treeview.column("#0", width=150)
		self.view_doses_tab_treeview.column("dosequantity", width=150)
		self.view_doses_tab_treeview.column("datetime", width=150)
		self.doses = sorted(self.doses, key=lambda x: x[2], reverse=True)
		for dose in self.doses:
			self.view_doses_tab_treeview.insert("", "end", text=dose[0], values=(f"{dose[1]}g",dose[2]))


	def create_view_medications_tab(self):
		self.view_medications_tab_label = ttk.Label(self.view_medications_tab, text="View Medications")
		self.view_medications_tab_label.grid(row=0, column=0, columnspan=2, pady=10)
		self.view_medications_tab_treeview = ttk.Treeview(self.view_medications_tab)
		self.view_medications_tab_treeview.grid(row=1, column=0, columnspan=2, pady=10)
		self.view_medications_tab_treeview["columns"] = ("quantity",)
		self.view_medications_tab_treeview.heading("#0", text="Medication")
		self.view_medications_tab_treeview.heading("quantity", text="Quantity")
		self.view_medications_tab_treeview.column("#0", width=150)
		self.view_medications_tab_treeview.column("quantity", width=150)
		for key, value in self.medications.items():
			self.view_medications_tab_treeview.insert("", "end", text=key, values=(f"{value}g",))
		self.view_medications_tab_treeview.bind("<Double-1>", self.view_medications_tab_treeview_double_click)

	def view_medications_tab_treeview_double_click(self, event):
		try:
			item = self.view_medications_tab_treeview.selection()[0]
			medication = self.view_medications_tab_treeview.item(item, "text")
			quantity = self.view_medications_tab_treeview.item(item, "values")[0]
			self.view_medications_tab_treeview.delete(item)
			del self.medications[medication]
			self.write_file()
			messagebox.showinfo("Success", "Medication deleted successfully")
		except IndexError:
			pass

	def create_exit_button(self):
		self.exit_button = ttk.Button(self, text="Exit", command=self.destroy)
		self.exit_button.grid(row=4, column=0, columnspan=2, pady=10)
			
if __name__ == "__main__":
	app = App()
	app.mainloop()
