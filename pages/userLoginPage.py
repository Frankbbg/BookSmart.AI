import tkinter as tk
import customtkinter as ctk

class userLoginPage(ctk.CTkFrame):
	def __init__(self, master):
		super().__init__(master)
		self.master = master
		# Create login form frame
		form = ctk.CTkFrame(self)
		form.pack(expand=True)

		# Create header of the form
		formHeader = ctk.CTkFrame(form, fg_color="transparent")
		formHeading = ctk.CTkLabel(formHeader, text="Login", font=("Helvetica", 32))
		self.formErrorMessage = ctk.CTkLabel(formHeader, text="")
		
		# Create the input section with form fields 
		formFieldsSection = ctk.CTkFrame(form)

		formFields = [
			{
				"labelText": "Username"
			},
			{
				"labelText": "Password",
				"isHidden": True,
			}
		]
		# Create list of form entries to get input later
		self.formEntryList = []
		for x in range(len(formFields)):
			label = ctk.CTkLabel(formFieldsSection, text=formFields[x]["labelText"])
			entry = ctk.CTkEntry(formFieldsSection)
			# If it's the password field, hide the input
			if (formFields[x].get("isHidden")):
				entry.configure(show="*")
			label.grid(row=x, column=0, pady=10, ipadx=10)
			entry.grid(row=x, column=1, pady=10, ipadx=10)
			self.formEntryList.append(entry)

		# Create section to have form buttons/actions
		formBtnsSection = ctk.CTkFrame(form, fg_color="transparent")
		confirmLoginBtn = ctk.CTkButton(formBtnsSection, text="Confirm Login", command=self.loginUser)
		openRegisterAccountBtn = ctk.CTkButton(formBtnsSection, text="Register New Account", command=lambda: self.master.openPage("userRegisterPage")) #type: ignore
		
		# Structure the remaining elements of the page
		formHeader.grid(row=0, column=0, pady=10)
		formHeading.grid(row=0, column=0)
		self.formErrorMessage.grid(row=1, column=0)

		formFieldsSection.grid(row=1, column=0, pady=10, ipadx=10)
		
		formBtnsSection.grid(row=2, column=0, pady=10)
		openRegisterAccountBtn.grid(row=0, column=0, padx=10, pady=10)
		confirmLoginBtn.grid(row=0, column=1, padx=10, pady=10)
		
	def loginUser(self):
		print("User Login button was clicked")
		pass











		