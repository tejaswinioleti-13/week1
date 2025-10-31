# ====================================================================
# PART 1 OF 5: IMPORTS AND CONFIGURATION
# ====================================================================

import customtkinter as ctk
from datetime import datetime
import tkinter as tk

# --- CustomTkinter Global Setup ---
ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

# Color Palette (Matching the dashboard feel)
COLORS = {
    "primary": "#007bff",  # Blue
    "danger": "#dc3545",  # Red (Overdue)
    "success": "#28a745",  # Green (Completed)
    "warning": "#ffc107",  # Yellow (Pending)
    "sidebar_bg": "#ffffff",
    "dashboard_bg": "#f4f7f6",
    "text": "#343a40",
    "secondary_text": "#6c757d",
}

# Task Storage (List of dictionaries)
# Statuses: 'overdue', 'completed', 'pending'
TASKS = [
    {"name": "Review quarterly reports", "due_date": "2025-09-15", "status": "overdue"},
    {"name": "Plan weekend trip", "due_date": "2025-10-05", "status": "pending"},
    {"name": "Update project documentation", "due_date": "2025-09-25", "status": "overdue"},
    {"name": "Buy groceries", "due_date": "2025-10-01", "status": "completed"},
    {"name": "Pay bills", "due_date": "2025-10-10", "status": "pending"},
]


class TaskSmartApp(ctk.CTk):
    def _init_(self):
        super()._init_()

        self.title("TaskSmart Dashboard (Functional)")
        self.geometry("1000x700")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self._setup_sidebar()
        self._setup_dashboard()

        # Initial data load and display
        self.update_dashboard_metrics()
        self.display_recent_tasks()

        # ====================================================================
        # PART 2 OF 5: SIDEBAR AND DASHBOARD SETUP
        # (Continue inside the TaskSmartApp class)
        # ====================================================================

        def _setup_sidebar(self):
            self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0, fg_color=COLORS["sidebar_bg"])
            self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
            self.sidebar_frame.grid_rowconfigure(6, weight=1)

            self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="TaskSmart",
                                           font=ctk.CTkFont(size=20, weight="bold"), text_color=COLORS["primary"])
            self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

            self.search_entry = ctk.CTkEntry(self.sidebar_frame, placeholder_text="Search tasks...")
            self.search_entry.grid(row=1, column=0, padx=20, pady=(10, 20), sticky="ew")

            self.new_task_button = ctk.CTkButton(self.sidebar_frame, text="➕ New Task", fg_color=COLORS["primary"],
                                                 hover_color="#0056b3", command=self._open_add_task_window)
            self.new_task_button.grid(row=2, column=0, padx=20, pady=(0, 30), sticky="ew")

            # Navigation
            self._create_nav_button("📊 Dashboard", 3, is_active=True)
            self._create_nav_button("📅 Today", 4)
            self._create_nav_button("📝 All Tasks", 5)
            self.settings_label = ctk.CTkLabel(self.sidebar_frame, text="⚙ Settings",
                                               text_color=COLORS["secondary_text"])
            self.settings_label.grid(row=7, column=0, padx=20, pady=(20, 20), sticky="s")

        def _create_nav_button(self, text, row, is_active=False):
            # Helper function for navigation buttons
            fg_color = COLORS["primary"] if is_active else COLORS["sidebar_bg"]
            text_color = "white" if is_active else COLORS["text"]
            hover_color = "#0056b3" if is_active else COLORS["dashboard_bg"]

            button = ctk.CTkButton(self.sidebar_frame, text=text, fg_color=fg_color,
                                   text_color=text_color, hover_color=hover_color,
                                   anchor="w", corner_radius=5)
            button.grid(row=row, column=0, padx=10, pady=2, sticky="ew")
            return button

        def _setup_dashboard(self):
            self.dashboard_frame = ctk.CTkScrollableFrame(self, fg_color=COLORS["dashboard_bg"])
            self.dashboard_frame.grid(row=0, column=1, sticky="nsew", padx=0, pady=0)
            self.dashboard_frame.grid_columnconfigure(0, weight=1)

            # Header
            header_frame = ctk.CTkFrame(self.dashboard_frame, fg_color="transparent")
            header_frame.grid(row=0, column=0, padx=30, pady=(30, 20), sticky="ew")
            header_frame.grid_columnconfigure(0, weight=1)

            ctk.CTkLabel(header_frame, text="Dashboard", font=ctk.CTkFont(size=24, weight="bold")).grid(row=0, column=0,
                                                                                                        sticky="w")
            ctk.CTkLabel(header_frame, text="Overview of your tasks and productivity",
                         text_color=COLORS["secondary_text"]).grid(row=1, column=0, sticky="w", pady=(0, 10))

            # Add Task Button
            add_task_btn = ctk.CTkButton(header_frame, text="➕ Add Task", fg_color=COLORS["danger"],
                                         hover_color="#c82333", width=100, command=self._open_add_task_window)
            add_task_btn.grid(row=0, column=1, rowspan=2, padx=(10, 0), sticky="e")

            # Metric Cards container
            self.metric_card_frame = ctk.CTkFrame(self.dashboard_frame, fg_color="transparent")
            self.metric_card_frame.grid(row=1, column=0, padx=30, pady=10, sticky="ew")
            self.metric_card_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

            self._create_quick_sections(self.dashboard_frame)

            # Recent Tasks Frame (where the list will appear)
            self.recent_tasks_container = ctk.CTkFrame(self.dashboard_frame, fg_color=COLORS["sidebar_bg"],
                                                       corner_radius=8)
            self.recent_tasks_container.grid(row=3, column=0, padx=30, pady=(0, 30), sticky="ew")
            self.recent_tasks_container.grid_columnconfigure(0, weight=1)

            # ====================================================================
            # PART 3 OF 5: METRIC CALCULATION AND UPDATE
            # (Continue inside the TaskSmartApp class)
            # ====================================================================

            def calculate_metrics(self):
                """Calculates current task metrics from the TASKS list."""
                today = datetime.now().strftime("%Y-%m-%d")

                total = len(TASKS)
                completed = sum(1 for task in TASKS if task["status"] == "completed")
                overdue = sum(1 for task in TASKS if task["status"] == "overdue")
                due_today = sum(1 for task in TASKS if task["due_date"] == today and task["status"] != "completed")

                completion_rate = round((completed / total) * 100) if total > 0 else 0

                return {
                    "Total Tasks": total,
                    "Completed": completed,
                    "Overdue": overdue,
                    "Due Today": due_today,
                    "Completion Rate": completion_rate
                }

            def update_dashboard_metrics(self):
                """Recreates the metric cards based on current TASKS data."""

                # Clear existing cards if any (prevents duplicates on update)
                for widget in self.metric_card_frame.winfo_children():
                    widget.destroy()

                metrics = self.calculate_metrics()

                cards = [
                    ("Total Tasks", metrics["Total Tasks"], None, None, "progress"),
                    ("Completed", metrics["Completed"], COLORS["success"], None, None),
                    ("Overdue", metrics["Overdue"], COLORS["danger"], COLORS["danger"], None),
                    ("Due Today", metrics["Due Today"], None, None, None),
                ]

                for i, (title, value, value_color, border_color, progress_type) in enumerate(cards):
                    card = self._create_card(self.metric_card_frame, title, str(value), value_color, border_color)
                    card.grid(row=0, column=i, padx=10, sticky="ew")

                    if progress_type == "progress":
                        progress_frame = ctk.CTkFrame(card, fg_color="transparent")
                        progress_frame.grid(row=2, column=0, sticky="ew", padx=15, pady=(5, 5))
                        progress_frame.grid_columnconfigure(0, weight=1)

                        # Progress Bar
                        progress_bar = ctk.CTkProgressBar(progress_frame, orientation="horizontal", height=8,
                                                          corner_radius=4)
                        progress_bar.set(metrics["Completion Rate"] / 100)
                        progress_bar.configure(fg_color="#e9ecef", progress_color=COLORS["danger"])
                        progress_bar.grid(row=0, column=0, sticky="ew")

                        completion_rate_label = ctk.CTkLabel(card, text=f'{metrics["Completion Rate"]}% Complete',
                                                             text_color=COLORS["danger"], font=ctk.CTkFont(size=10))
                        completion_rate_label.grid(row=3, column=0, padx=15, sticky="w", pady=(0, 10))

                # ====================================================================
                # PART 4 OF 5: DYNAMIC TASK LIST AND MANAGEMENT LOGIC
                # (Continue inside the TaskSmartApp class)
                # ====================================================================

                def display_recent_tasks(self):
                    """Populates the Recent Tasks section with dynamic, interactive data."""

                    # Clear existing content in the Recent Tasks container
                    for widget in self.recent_tasks_container.winfo_children():
                        widget.destroy()

                    # Header for the section
                    ctk.CTkLabel(self.recent_tasks_container, text="Recent Tasks",
                                 font=ctk.CTkFont(size=18, weight="bold")).grid(row=0, column=0, padx=15, pady=(15, 5),
                                                                                sticky="w")

                    metrics = self.calculate_metrics()
                    summary_frame = ctk.CTkFrame(self.recent_tasks_container, fg_color="transparent")
                    summary_frame.grid(row=1, column=0, padx=15, pady=(0, 10), sticky="w")

                    pending_count = metrics["Total Tasks"] - metrics["Completed"]

                    summary_text = ctk.CTkLabel(summary_frame,
                                                text=f"{metrics['Total Tasks']} total | {pending_count} pending |",
                                                text_color=COLORS["secondary_text"], anchor="w")
                    summary_text.grid(row=0, column=0, sticky="w")

                    overdue_text = ctk.CTkLabel(summary_frame, text=f" {metrics['Overdue']} overdue",
                                                text_color=COLORS["danger"], font=ctk.CTkFont(weight="bold"))
                    overdue_text.grid(row=0, column=1, sticky="w")

                    # Task List Frame
                    task_list_frame = ctk.CTkFrame(self.recent_tasks_container, fg_color="transparent")
                    task_list_frame.grid(row=2, column=0, padx=15, pady=(5, 15), sticky="ew")
                    task_list_frame.grid_columnconfigure(0, weight=1)  # Name column

                    # Add a header row for the task list
                    ctk.CTkLabel(task_list_frame, text="Task", font=ctk.CTkFont(weight="bold"),
                                 text_color=COLORS["secondary_text"]).grid(row=0, column=0, sticky="w", pady=5)
                    ctk.CTkLabel(task_list_frame, text="Due Date", font=ctk.CTkFont(weight="bold"),
                                 text_color=COLORS["secondary_text"]).grid(row=0, column=1, padx=10, sticky="w")
                    ctk.CTkLabel(task_list_frame, text="Status", font=ctk.CTkFont(weight="bold"),
                                 text_color=COLORS["secondary_text"]).grid(row=0, column=2, padx=10, sticky="w")
                    ctk.CTkLabel(task_list_frame, text="Complete", font=ctk.CTkFont(weight="bold"),
                                 text_color=COLORS["secondary_text"]).grid(row=0, column=3, padx=10, sticky="w")

                    # Display each task
                    for i, task in enumerate(TASKS):
                        row = i + 1

                        # 1. Task Name
                        task_name_label = ctk.CTkLabel(task_list_frame, text=task["name"], anchor="w")
                        task_name_label.grid(row=row, column=0, sticky="w", pady=5, padx=(0, 20))

                        # 2. Due Date
                        due_date_label = ctk.CTkLabel(task_list_frame, text=task["due_date"],
                                                      text_color=COLORS["secondary_text"])
                        due_date_label.grid(row=row, column=1, padx=10, sticky="w")

                        # 3. Status
                        status = task["status"]
                        status_color = COLORS.get(status, COLORS["secondary_text"])
                        status_label = ctk.CTkLabel(task_list_frame, text=status.capitalize(), text_color=status_color,
                                                    font=ctk.CTkFont(weight="bold"))
                        status_label.grid(row=row, column=2, padx=10, sticky="w")

                        # 4. Completion Checkbox
                        checkbox = ctk.CTkCheckBox(
                            master=task_list_frame,
                            text="",
                            width=10,
                            command=lambda t=task: self._toggle_task_status(t),
                        )
                        if task["status"] == "completed":
                            checkbox.select()
                            task_name_label.configure(text_color=COLORS["success"], text=f"✓ {task['name']}")

                        checkbox.grid(row=row, column=3, padx=25, sticky="w")

                        # Separator line
                        separator = ctk.CTkFrame(task_list_frame, height=1, fg_color="#e9ecef")
                        separator.grid(row=row + 0.5, column=0, columnspan=4, sticky="ew", pady=(0, 0))

                        # ====================================================================
                        # PART 5 OF 5: HELPERS AND MAIN EXECUTION
                        # (Continue inside the TaskSmartApp class and end the file)
                        # ====================================================================

                        def update_ui(self):
                            """A single function to call all necessary update methods."""
                            self.update_dashboard_metrics()
                            self.display_recent_tasks()

                        # --- Helper Functions ---
                        def _create_card(self, parent, title, value, value_color=None, border_color=None):
                            """Helper to create a single stylish metric card."""
                            card = ctk.CTkFrame(parent, fg_color=COLORS["sidebar_bg"], corner_radius=8)
                            card.grid_columnconfigure(0, weight=1)
                            if border_color:
                                card.configure(border_width=5, border_color=border_color)

                            title_label = ctk.CTkLabel(card, text=title, text_color=COLORS["secondary_text"],
                                                       font=ctk.CTkFont(size=14))
                            title_label.grid(row=0, column=0, padx=15, pady=(15, 0), sticky="w")

                            value_label = ctk.CTkLabel(card, text=value, font=ctk.CTkFont(size=30, weight="bold"))
                            if value_color:
                                value_label.configure(text_color=value_color)
                            value_label.grid(row=1, column=0, padx=15, pady=(0, 5), sticky="w")

                            return card

                        def _create_quick_sections(self, parent):
                            """Creates the Quick Overview and Recent Activity sections."""
                            section_frame = ctk.CTkFrame(parent, fg_color="transparent")
                            section_frame.grid(row=2, column=0, padx=30, pady=20, sticky="ew")
                            section_frame.grid_columnconfigure((0, 1), weight=1)

                            metrics = self.calculate_metrics()

                            # --- Quick Overview ---
                            quick_frame = ctk.CTkFrame(section_frame, fg_color=COLORS["sidebar_bg"], corner_radius=8)
                            quick_frame.grid(row=0, column=0, padx=(0, 15), sticky="nsew")

                            ctk.CTkLabel(quick_frame, text="Quick Overview",
                                         font=ctk.CTkFont(size=18, weight="bold")).grid(row=0, column=0, padx=15,
                                                                                        pady=(15, 5), sticky="w")

                            overview_details = [
                                ("Tasks due today", str(metrics["Due Today"])),
                                ("Overdue tasks", str(metrics["Overdue"]), COLORS["danger"]),
                                ("Completion rate", f'{metrics["Completion Rate"]}%'),
                            ]
                            for i, (label_text, value_text, *color_tuple) in enumerate(overview_details):
                                item_frame = ctk.CTkFrame(quick_frame, fg_color="transparent")
                                item_frame.grid(row=i + 1, column=0, padx=15, pady=5, sticky="ew")
                                item_frame.grid_columnconfigure(0, weight=1)

                                ctk.CTkLabel(item_frame, text=label_text).grid(row=0, column=0, sticky="w")
                                value_label = ctk.CTkLabel(item_frame, text=value_text, font=ctk.CTkFont(weight="bold"))
                                if color_tuple:
                                    value_label.configure(text_color=color_tuple[0])
                                value_label.grid(row=0, column=1, padx=(5, 0), sticky="e")

                            # --- Recent Activity (Static list for demonstration) ---
                            activity_frame = ctk.CTkFrame(section_frame, fg_color=COLORS["sidebar_bg"], corner_radius=8)
                            activity_frame.grid(row=0, column=1, padx=(15, 0), sticky="nsew")
                            ctk.CTkLabel(activity_frame, text="Recent Activity",
                                         font=ctk.CTkFont(size=18, weight="bold")).grid(row=0, column=0, padx=15,
                                                                                        pady=(15, 5), sticky="w")

                            activities = [
                                "Review quarterly reports",
                                "Plan weekend trip",
                                "Update project documentation",
                                "Buy groceries",
                            ]
                            for i, activity in enumerate(activities):
                                label = ctk.CTkLabel(activity_frame, text=f"• {activity}",
                                                     text_color=COLORS["secondary_text"], anchor="w")
                                label.grid(row=i + 1, column=0, padx=25, pady=5, sticky="ew")

                    if _name_ == "_main_":
                        app = TaskSmartApp()
                        app.mainloop()

