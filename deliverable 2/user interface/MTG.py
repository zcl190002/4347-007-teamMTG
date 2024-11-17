import sqlite3
import customtkinter
from tkinter import messagebox
import pyperclip
import platform
from tkinter import ttk

# changes the appearance to a dark version of customtkinter
customtkinter.set_appearance_mode("dark")

if platform.system() == "Windows":
    try:
        from ctypes import windll
        windll.user32.SetProcessDPIAware()
    except Exception:
        pass
else:
    customtkinter.set_widget_scaling(1.0)
    customtkinter.set_window_scaling(1.0)

# connects to the database
def connect_to_db():
    conn = sqlite3.connect("mtg.db")
    return conn


# creates the condition frame for the search criteria
class ConditionFrame:
    def __init__(self, parent, index, columns, on_remove=None):
        self.frame = customtkinter.CTkFrame(parent, corner_radius=15)
        self.frame.grid(row=index * 2, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
        self.frame.grid_columnconfigure(1, weight=1)

        self.attribute_var = customtkinter.StringVar(value=columns[0])
        self.attribute_dropdown = customtkinter.CTkOptionMenu(
            self.frame,
            values=columns,
            variable=self.attribute_var,
            font=("Arial", 12)
        )
        self.attribute_dropdown.grid(row=0, column=0, padx=10, pady=5, sticky="ew")

        self.condition_entry = customtkinter.CTkEntry(
            self.frame,
            placeholder_text="Enter a condition... (e.g. = 5, > 3, 'Banishing Light')",
            font=("Arial", 12)
        )
        self.condition_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        if on_remove and index > 0:
            self.remove_btn = customtkinter.CTkButton(
                self.frame,
                text="✕",
                width=30,
                command=lambda: on_remove(self),
                font=("Arial", 12)
            )
            self.remove_btn.grid(row=0, column=2, padx=5, pady=5)

        if index > 0:
            self.operator_var = customtkinter.StringVar(value="AND")
            self.operator_dropdown = customtkinter.CTkOptionMenu(
                parent,
                values=["AND", "OR"],
                variable=self.operator_var,
                width=100,
                font=("Arial", 12)
            )
            self.operator_dropdown.grid(row=(index * 2) - 1, column=0, columnspan=2, pady=2)

# creates the table tab to display and interact with the data
class TableTab:
    def __init__(self, parent, table_name, columns, window, column_widths=None):
        self.table_name = table_name
        self.columns = columns
        self.window = window
        self.column_widths = column_widths or {col: 150 for col in columns}

        self.main_frame = customtkinter.CTkFrame(parent, corner_radius=15)
        self.main_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)

        self.main_frame.grid_rowconfigure(0, weight=1) # search frame
        self.main_frame.grid_rowconfigure(1, weight=0) # first button frame
        self.main_frame.grid_rowconfigure(2, weight=5) # table view
        self.main_frame.grid_rowconfigure(3, weight=0) # second button frame
        self.main_frame.grid_rowconfigure(4, weight=0) # function frames
        self.main_frame.grid_columnconfigure(0, weight=1)


        self.create_search_section()
        self.create_table_view()
        self.result_box = customtkinter.CTkTextbox(self.main_frame, height=1)
        self.result_box.grid_remove()
        self.create_control_buttons()
        self.create_function_frames()

    def create_search_section(self):
        self.conditions_frame = customtkinter.CTkScrollableFrame(self.main_frame)
        self.conditions_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.conditions_frame.grid_columnconfigure(0, weight=1)

        self.conditions = []
        self.add_condition()

        # first button frame
        button_frame = customtkinter.CTkFrame(self.main_frame)
        button_frame.grid(row=1, column=0, padx=10, pady=5)

        btn_add_condition = customtkinter.CTkButton(
            button_frame,
            text="Add Condition",
            command=self.add_condition,
            width=150
        )
        btn_add_condition.grid(row=0, column=0, padx=10, pady=5)

        btn_search = customtkinter.CTkButton(
            button_frame,
            text="Search",
            command=self.search,
            width=150
        )
        btn_search.grid(row=0, column=1, padx=10, pady=5)

        btn_quit = customtkinter.CTkButton(
            button_frame,
            text="Quit",
            command= self.window.destroy,
            width=150
        )
        btn_quit.grid(row=0, column=2, padx=10, pady=5)

    def create_table_view(self):
        table_frame = customtkinter.CTkFrame(self.main_frame)
        table_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        table_frame.grid_columnconfigure(0, weight=1)
        table_frame.grid_rowconfigure(0, weight=1)

        style = ttk.Style()
        style.theme_use('clam')

        default_font = ("Segoe UI", 8)


        style.configure("Treeview",
                        background="#2b2b2b",
                        foreground="white",
                        fieldbackground="#2b2b2b",
                        borderwidth=0,
                        font= default_font,
                        rowheight=35)

        style.configure("Treeview.Heading",
                        background="#404040",
                        foreground="white",
                        borderwidth=1)

        style.map('Treeview',
                  background=[('selected', '#404040')],
                  foreground=[('selected', 'white')])

        self.tree = ttk.Treeview(table_frame, show="headings", height=10, style="Treeview")
        self.tree["columns"] = self.columns

        for col in self.columns:
            col_width = self.column_widths.get(col, 150)
            self.tree.column(col, anchor="w", stretch=True, width=col_width, minwidth=col_width)
            self.tree.heading(col, text=col)

        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")

        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

    def create_control_buttons(self):
        # second buttons frame
        control_buttons_frame = customtkinter.CTkFrame(self.main_frame)
        control_buttons_frame.grid(row=3, column=0, padx=10, pady=10, sticky="ew")
        control_buttons_frame.grid_columnconfigure((0, 1), weight=1)

        btn_copy = customtkinter.CTkButton(
            control_buttons_frame,
            text="Copy to Clipboard",
            command=lambda: self.copy_to_clipboard()
        )
        btn_copy.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        btn_export = customtkinter.CTkButton(
            control_buttons_frame,
            text="Export to File",
            command=lambda: self.export_to_file()
        )
        btn_export.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

    def create_function_frames(self):
        operations_scroll_frame = customtkinter.CTkScrollableFrame(self.main_frame)
        operations_scroll_frame.grid(row=4, column=0, padx=10, pady=10, sticky="nsew")
        operations_scroll_frame.grid_columnconfigure(0, weight=1)
        operations_scroll_frame.grid_rowconfigure((0, 1, 2), weight=1)

        self.create_insert_frame(operations_scroll_frame)
        self.create_update_frame(operations_scroll_frame)
        self.create_delete_frame(operations_scroll_frame)

    def create_insert_frame(self, parent):
        insert_frame = customtkinter.CTkFrame(parent, corner_radius=15)
        insert_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        insert_frame.grid_columnconfigure(1, weight=1)

        insert_title = customtkinter.CTkLabel(insert_frame, text=f"Insert New {self.table_name}",
                                              font=("Arial", 16, "bold"))
        insert_title.grid(row=0, column=0, columnspan=2, padx=10, pady=(10, 5), sticky="w")

        self.insert_entries = []
        for i, col in enumerate(self.columns, start=1):
            customtkinter.CTkLabel(insert_frame, text=col, font=("Arial", 12)).grid(
                row=i, column=0, padx=10, pady=5, sticky="w")
            entry = customtkinter.CTkEntry(insert_frame, font=("Arial", 12))
            entry.grid(row=i, column=1, padx=10, pady=5, sticky="ew")
            self.insert_entries.append(entry)

        btn_insert = customtkinter.CTkButton(
            insert_frame,
            text=f"Insert {self.table_name}",
            command=self.insert_record
        )
        btn_insert.grid(row=len(self.columns) + 1, column=0, columnspan=2, pady=10)

    def create_update_frame(self, parent):
        update_frame = customtkinter.CTkFrame(parent, corner_radius=15)
        update_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        update_frame.grid_columnconfigure(1, weight=1)

        update_title = customtkinter.CTkLabel(
            update_frame,
            text=f"Update {self.table_name}",
            font=("Arial", 16, "bold")
        )
        update_title.grid(row=0, column=0, columnspan=2, padx=10, pady=(10, 5), sticky="w")

        customtkinter.CTkLabel(
            update_frame,
            text=f"{self.columns[0]} to Update",
            font=("Arial", 12)
        ).grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.update_key_entry = customtkinter.CTkEntry(update_frame, font=("Arial", 12))
        self.update_key_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        self.update_entries = []
        for i, col in enumerate(self.columns[1:], start=2):
            customtkinter.CTkLabel(
                update_frame,
                text=col,
                font=("Arial", 12)
            ).grid(row=i, column=0, padx=10, pady=5, sticky="w")

            entry = customtkinter.CTkEntry(update_frame, font=("Arial", 12))
            entry.grid(row=i, column=1, padx=10, pady=5, sticky="ew")
            self.update_entries.append(entry)

        btn_update = customtkinter.CTkButton(
            update_frame,
            text=f"Update {self.table_name}",
            command=self.update_record,
            font=("Arial", 12)
        )
        btn_update.grid(row=len(self.columns) + 1, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

    def create_delete_frame(self, parent):
        delete_frame = customtkinter.CTkFrame(parent, corner_radius=15)
        delete_frame.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
        delete_frame.grid_columnconfigure(1, weight=1)

        delete_title = customtkinter.CTkLabel(
            delete_frame,
            text=f"Delete {self.table_name}",
            font=("Arial", 16, "bold")
        )
        delete_title.grid(row=0, column=0, columnspan=2, padx=10, pady=(10, 5), sticky="w")

        customtkinter.CTkLabel(
            delete_frame,
            text=f"{self.columns[0]} to Delete",
            font=("Arial", 12)
        ).grid(row=1, column=0, padx=10, pady=5, sticky="w")

        self.delete_entry = customtkinter.CTkEntry(delete_frame, font=("Arial", 12))
        self.delete_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        btn_delete = customtkinter.CTkButton(
            delete_frame,
            text=f"Delete {self.table_name}",
            command=self.delete_record,
            font=("Arial", 12)
        )
        btn_delete.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

    def add_condition(self):
        index = len(self.conditions)
        condition = ConditionFrame(self.conditions_frame, index, self.columns, self.remove_condition)
        self.conditions.append(condition)

    def remove_condition(self, condition):
        self.conditions.remove(condition)
        condition.frame.destroy()
        if hasattr(condition, 'operator_dropdown'):
            condition.operator_dropdown.destroy()
        for i, cond in enumerate(self.conditions):
            cond.frame.grid(row=i * 2, column=0)
            if hasattr(cond, 'operator_dropdown'):
                cond.operator_dropdown.grid(row=(i * 2) - 1, column=0)

    def build_query(self):
        query_parts = []
        params = []
        for i, condition in enumerate(self.conditions):
            if i > 0 and hasattr(condition, 'operator_dropdown'):
                query_parts.append(condition.operator_var.get())

            attr = condition.attribute_var.get()
            cond = condition.condition_entry.get().strip()

            if cond.startswith((">", "<", "=")):
                op = ''.join(c for c in cond if c in "><=")
                value = ''.join(c for c in cond if c not in "><=").strip()
                try:
                    float(value)
                    query_parts.append(f'"{attr}" {op} ?')
                    params.append(value)
                except ValueError:
                    continue
            else:
                query_parts.append(f'"{attr}" LIKE ?')
                params.append(f"%{cond}%")

        return " ".join(query_parts) if query_parts else "1=1", params

    def search(self):
        query_condition, params = self.build_query()
        conn = connect_to_db()
        cursor = conn.cursor()

        # try to execute the search query
        try:
            full_query = f"SELECT * FROM {self.table_name} WHERE {query_condition}"
            cursor.execute(full_query, params)
            results = cursor.fetchall()

            self.result_box.delete("1.0", customtkinter.END)
            for item in self.tree.get_children():
                self.tree.delete(item)

            if results:
                for row in results:
                    self.tree.insert("", "end", values=row)
                    formatted_row = ", ".join(f"{col}: {val}" for col, val in zip(self.columns, row))
                    self.result_box.insert(customtkinter.END, f"{formatted_row}\n")
            else:
                self.tree.insert("", "end", values=["No matching records found."])
                self.result_box.insert(customtkinter.END, "No matching records found.")
        except sqlite3.Error as e:
            error_msg = f"Error: {e}"
            self.tree.insert("", "end", values=[error_msg])
            self.result_box.delete("1.0", customtkinter.END)
            self.result_box.insert(customtkinter.END, error_msg)
        finally:
            conn.close()

    def insert_record(self):
        values = [entry.get() for entry in self.insert_entries]
        placeholders = ", ".join(["?" for _ in self.columns])
        columns = ", ".join([f'"{col}"' for col in self.columns])
        query = f"""
                    INSERT INTO {self.table_name} 
                    ({columns}) 
                    VALUES ({placeholders})
                    """
        # insert the record
        try:
            conn = connect_to_db()
            cursor = conn.cursor()
            cursor.execute(query, values)
            conn.commit()

            card_name = values[0]

            self.result_box.delete("1.0", customtkinter.END)
            self.result_box.insert("end", f"'{card_name}' record inserted into {self.table_name} successfully.\n")

            messagebox.showinfo("Insert Record", f"'{card_name}' inserted to {self.table_name} successfully.")
            self.refresh_tree_view(selected_key_value=card_name)

            for entry in self.insert_entries:
                entry.delete(0, customtkinter.END)

        except sqlite3.Error as e:
            self.result_box.delete("1.0", customtkinter.END)
            self.result_box.insert("end", f"Error: {e}\n")
        finally:
            conn.close()

    def update_record(self):
        key_value = self.update_key_entry.get().strip()
        if not key_value:
            messagebox.showwarning("Update Record", "Please enter the card name for the record you want to update.")
            return

        values = [entry.get().strip() for entry in self.update_entries if entry.get().strip()]
        if not values:
            messagebox.showwarning("Update Record", "Please enter at least one field to update.")
            return

        update_columns = [col for col, entry in zip(self.columns[1:], self.update_entries) if entry.get().strip()]
        set_clause = ", ".join(f'"{col}" = ?' for col in update_columns)
        query = f"""
                    UPDATE {self.table_name} 
                    SET {set_clause} 
                    WHERE "{self.columns[0]}" = ?
                    """

        try:
            conn = connect_to_db()
            cursor = conn.cursor()
            cursor.execute(query, (*values, key_value))
            conn.commit()

            cursor.execute('SELECT changes()')
            changes = cursor.fetchone()[0]

            self.result_box.delete("1.0", customtkinter.END)
            if changes > 0:
                self.result_box.insert("end", f"'{key_value}' in updated successfully in {self.table_name}.\n")
                messagebox.showinfo("Update Record", f"'{key_value}' updated successfully in {self.table_name}.")
                for entry in self.update_entries:
                    entry.delete(0, customtkinter.END)
                self.update_key_entry.delete(0, customtkinter.END)
                self.refresh_tree_view(selected_key_value=key_value)
            else:
                self.result_box.insert("end", f"No {self.table_name} record found with that card name.\n")
                messagebox.showwarning("Update Record", f"No {self.table_name} record found with that card name.")

        except sqlite3.Error as e:
            self.result_box.delete("1.0", customtkinter.END)
            self.result_box.insert("end", f"Error: {e}\n")
            messagebox.showerror("Update Record", f"Error: {e}")
        finally:
            conn.close()

    def delete_record(self):
        key_value = self.delete_entry.get()
        query = f'DELETE FROM {self.table_name} WHERE "{self.columns[0]}" = ?'

        if not key_value.strip():
            messagebox.showwarning("Delete Record", "Please enter a card to delete.")
            return

        confirm = messagebox.askyesno("Confirm Deletion",
                                      f"Are you sure you want to delete {self.table_name} record '{key_value}'?")
        if not confirm:
            return

        try:
            conn = connect_to_db()
            cursor = conn.cursor()
            cursor.execute(query, (key_value,))
            conn.commit()

            self.result_box.delete("1.0", customtkinter.END)
            if cursor.rowcount > 0:
                self.result_box.insert("end", f"{self.table_name} record deleted successfully.\n")
                self.delete_entry.delete(0, customtkinter.END)
                messagebox.showinfo("Delete Record", f"{self.table_name} record deleted successfully.")
            else:
                self.result_box.insert("end", f"No {self.table_name} record found with that card name.\n")
                messagebox.showwarning("Delete Record", f"No {self.table_name} record found with that card name.")

            self.refresh_tree_view()

        except sqlite3.Error as e:
            self.result_box.delete("1.0", customtkinter.END)
            self.result_box.insert("end", f"Error: {e}\n")
            messagebox.showerror("Delete Record", f"Error: {e}")
        finally:
            conn.close()

    def refresh_tree_view(self, selected_key_value=None):
        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            conn = connect_to_db()
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM {self.table_name}")
            results = cursor.fetchall()

            for row in results:
                item_id = self.tree.insert("", "end", values=row)
                if selected_key_value and str(row[0]) == str(selected_key_value):
                    self.tree.selection_set(item_id)
                    self.tree.focus(item_id)
                    self.tree.see(item_id)

        except sqlite3.Error as e:
            self.tree.insert("", "end", values=[f"Error: {e}"])
        finally:
            conn.close()

    def copy_to_clipboard(self):
        results_text = self.result_box.get("1.0", customtkinter.END).strip()
        if results_text:
            pyperclip.copy(results_text)
            messagebox.showinfo("Copy to Clipboard", "Results copied to clipboard.")
        else:
            messagebox.showwarning("Copy to Clipboard", "No results to copy.")

    def export_to_file(self):
        results_text = self.result_box.get("1.0", customtkinter.END).strip()
        if results_text:
            with open(f"{self.table_name}_results.txt", "w") as file:
                file.write(results_text)
            messagebox.showinfo("Export to File", f"Results exported to {self.table_name}_results.txt.")
        else:
            messagebox.showwarning("Export to File", "No results to export.")

def create_main_window():
    window = customtkinter.CTk()
    window.title("MTG Database Manager")

    # set window size
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    window.geometry(f"{int(screen_width * 0.8)}x{int(screen_height * 0.8)}")

    window.grid_rowconfigure(0, weight=1)
    window.grid_columnconfigure(0, weight=1)

    # create tabview
    tabview = customtkinter.CTkTabview(window)
    tabview.pack(expand=True, fill="both", padx=20, pady=20)

        # card info tab
    card_tab = tabview.add("Card Info")
    card_columns = ["card_name", "type_line", "power", "toughness",
                        "color_identity", "colors", "converted_mana_cost",
                        "mana_cost", "rarity"]
    card_widths = {
            "card_name": 150,
            "type_line": 150,
            "power": 50,
            "toughness": 50,
            "color_identity": 100,
            "colors": 100,
            "converted_mana_cost": 50,
            "mana_cost": 100,
            "rarity": 100
        }
    TableTab(card_tab, "CARD_INFO", card_columns, window,    card_widths)

        # card price tab
    price_tab = tabview.add("Card Prices")
    price_columns = ["card_name", "set", "set_number", "seller", "tix", "usd"]
    price_widths = {
            "card_name": 200,
            "set": 150,
            "set_number": 100,
            "seller": 200,
            "tix": 100,
            "usd": 100
        }
    TableTab(price_tab, "CARD_PRICE", price_columns, window, price_widths)

        # card print tab
    print_tab = tabview.add("Card Prints")
    print_columns = ["card_name", "set", "set_number", "artist_name", "url_to_unique_prints", "url_to_png_download", "flavor_text"]
    print_widths = {
            "card_name": 150,
            "set": 50,
            "set_number": 100,
            "artist_name": 150,
            "url_to_unique_prints": 500,
            "url_to_png_download": 575,
            "flavor_text": 1000
        }
    TableTab(print_tab, "CARD_PRINT", print_columns, window, print_widths)

        # commander analytics tab
    com_analytics_tab = tabview.add("Commander Analytics")
    com_analytics_columns = ["card_name", "format", "edhrec_rank", "salt_score"]
    com_analytics_widths = {
            "card_name": 250,
            "format": 200,
            "edhrec_rank": 200,
            "salt_score": 200
        }
    TableTab(com_analytics_tab, "COMMANDER_ANALYTICS", com_analytics_columns, window, com_analytics_widths)


        # limited analytics tab
    lim_analytics_tab = tabview.add("Limited Analytics")
    lim_analytics_columns = ["card_name", "format", "win_rate_in_main_deck", "play_rate", "win_rate_opening_hand", "win_rate_drawn"]
    lim_analytics_widths = {
            "card_name": 200,
            "format": 100,
            "win_rate_in_main_decks": 200,
            "play_rate": 100,
            "win_rate_opening_hand": 150,
            "win_rate_drawn": 100
        }
    TableTab(lim_analytics_tab, "LIMITED_ANALYTICS", lim_analytics_columns, window, lim_analytics_widths)

    window.mainloop()

if __name__ == "__main__":
        create_main_window()