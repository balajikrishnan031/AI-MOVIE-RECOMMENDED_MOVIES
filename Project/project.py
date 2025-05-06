import tkinter as tk
from tkinter import ttk, messagebox, font
import json
import random
from datetime import datetime
import time

class CineMate:
    def __init__(self, root):
        self.root = root
        self.root.title("CineMate - AI Movie Recommendations")
        self.root.geometry("1000x750")
        
        # Available themes
        self.themes = {
            "Modern": {
                "bg": "#2c3e50",
                "fg": "#ecf0f1",
                "accent": "#3498db",
                "secondary": "#34495e",
                "highlight": "#e74c3c",
                "success": "#2ecc71",
                "warning": "#f39c12",
                "font_title": ("Montserrat", 24, "bold"),
                "font_subtitle": ("Open Sans", 12),
                "font_body": ("Open Sans", 10)
            },
            "Classic": {
                "bg": "#f5f5f5",
                "fg": "#333333",
                "accent": "#8e44ad",
                "secondary": "#bdc3c7",
                "highlight": "#c0392b",
                "success": "#27ae60",
                "warning": "#d35400",
                "font_title": ("Times New Roman", 24, "bold"),
                "font_subtitle": ("Georgia", 12),
                "font_body": ("Georgia", 10)
            },
            "Futuristic": {
                "bg": "#121212",
                "fg": "#00ffaa",
                "accent": "#ff00aa",
                "secondary": "#333333",
                "highlight": "#00aaff",
                "success": "#00ff00",
                "warning": "#ffaa00",
                "font_title": ("Orbitron", 24, "bold"),
                "font_subtitle": ("Rajdhani", 12),
                "font_body": ("Rajdhani", 10)
            }
        }
        
        # Set default theme
        self.current_theme = "Modern"
        self.apply_theme()
        
        # Movie database
        self.movie_db = [
            {"id": "1", "title": "Inception", "genres": ["Sci-Fi", "Action"], "rating": 8.8, "year": 2010, "duration": 148},
            {"id": "2", "title": "The Shawshank Redemption", "genres": ["Drama"], "rating": 9.3, "year": 1994, "duration": 142},
            {"id": "3", "title": "Pulp Fiction", "genres": ["Crime", "Drama"], "rating": 8.9, "year": 1994, "duration": 154},
            {"id": "4", "title": "The Dark Knight", "genres": ["Action", "Crime", "Drama"], "rating": 9.0, "year": 2008, "duration": 152},
            {"id": "5", "title": "Fight Club", "genres": ["Drama"], "rating": 8.8, "year": 1999, "duration": 139},
            {"id": "6", "title": "Forrest Gump", "genres": ["Drama", "Romance"], "rating": 8.8, "year": 1994, "duration": 142},
            {"id": "7", "title": "The Matrix", "genres": ["Action", "Sci-Fi"], "rating": 8.7, "year": 1999, "duration": 136},
            {"id": "8", "title": "Goodfellas", "genres": ["Crime", "Drama"], "rating": 8.7, "year": 1990, "duration": 146},
            {"id": "9", "title": "The Silence of the Lambs", "genres": ["Crime", "Thriller"], "rating": 8.6, "year": 1991, "duration": 118},
            {"id": "10", "title": "Interstellar", "genres": ["Adventure", "Drama", "Sci-Fi"], "rating": 8.6, "year": 2014, "duration": 169},
        ]
        
        self.current_user = None
        self.load_user_data()
        
        if self.current_user:
            self.create_main_interface()
        else:
            self.create_login_interface()

    def apply_theme(self):
        theme = self.themes[self.current_theme]
        self.root.configure(bg=theme["bg"])
        
        # Configure styles
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Base styles
        self.style.configure('.', background=theme["bg"], foreground=theme["fg"], font=theme["font_body"])
        self.style.configure('TFrame', background=theme["bg"])
        self.style.configure('TLabel', background=theme["bg"], foreground=theme["fg"], font=theme["font_body"])
        self.style.configure('TButton', font=theme["font_body"], padding=5)
        self.style.configure('TNotebook', background=theme["bg"], borderwidth=0)
        self.style.configure('TNotebook.Tab', background=theme["secondary"], foreground=theme["fg"], 
                           font=theme["font_body"], padding=[10, 5])
        self.style.map('TNotebook.Tab', background=[('selected', theme["accent"])])
        
        # Custom styles
        self.style.configure('Accent.TButton', background=theme["accent"], foreground=theme["fg"])
        self.style.configure('Success.TLabel', foreground=theme["success"])
        self.style.configure('Warning.TLabel', foreground=theme["warning"])
        self.style.configure('Highlight.TLabel', foreground=theme["highlight"])

    def load_user_data(self):
        try:
            with open('cinemate_user.json', 'r') as f:
                data = json.load(f)
                if data:
                    self.current_user = data
        except (FileNotFoundError, json.JSONDecodeError):
            self.current_user = None

    def save_user_data(self):
        with open('cinemate_user.json', 'w') as f:
            json.dump(self.current_user, f)

    def create_login_interface(self):
        self.clear_window()
        theme = self.themes[self.current_theme]
        
        # Main frame
        main_frame = ttk.Frame(self.root, padding=20, style='TFrame')
        main_frame.pack(expand=True, fill=tk.BOTH)
        
        # Theme selector
        theme_frame = ttk.Frame(main_frame, style='TFrame')
        theme_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(theme_frame, text="Theme:", style='TLabel').pack(side=tk.LEFT)
        self.theme_var = tk.StringVar(value=self.current_theme)
        for theme_name in self.themes.keys():
            rb = ttk.Radiobutton(theme_frame, text=theme_name, variable=self.theme_var, 
                                value=theme_name, command=self.change_theme)
            rb.pack(side=tk.LEFT, padx=5)
        
        # Title
        title_label = ttk.Label(main_frame, text="CineMate", font=theme["font_title"], foreground=theme["accent"])
        title_label.pack(pady=10)
        
        subtitle_label = ttk.Label(main_frame, text="AI-Powered Movie Recommendations", 
                                 font=theme["font_subtitle"], foreground=theme["fg"])
        subtitle_label.pack(pady=(0, 20))
        
        # Form frame
        form_frame = ttk.Frame(main_frame, style='TFrame')
        form_frame.pack(pady=10)
        
        # Form fields
        fields = [
            ("Name", "name", ""),
            ("Email", "email", ""),
            ("Age", "age", "18"),
            ("Favorite Genres (comma separated)", "genres", ""),
            ("Bio (optional)", "bio", ""),
            ("Password", "password", "", True)
        ]
        
        self.entries = {}
        for label_text, field_name, default, *is_password in fields:
            frame = ttk.Frame(form_frame, style='TFrame')
            frame.pack(fill=tk.X, pady=5)
            
            label = ttk.Label(frame, text=label_text, width=25, anchor='w', 
                            font=theme["font_body"])
            label.pack(side=tk.LEFT)
            
            if is_password and is_password[0]:
                entry = ttk.Entry(frame, show="*")
            else:
                entry = ttk.Entry(frame)
                
            entry.insert(0, default)
            entry.pack(side=tk.RIGHT, expand=True, fill=tk.X)
            self.entries[field_name] = entry
        
        # Register button
        register_btn = ttk.Button(main_frame, text="Register", command=self.register_user, 
                                style='Accent.TButton')
        register_btn.pack(pady=20)

    def change_theme(self):
        self.current_theme = self.theme_var.get()
        self.apply_theme()
        
        if hasattr(self, 'notebook'):
            # Recreate the interface with new theme
            if self.current_user:
                self.create_main_interface()
            else:
                self.create_login_interface()

    def register_user(self):
        user_data = {
            "name": self.entries["name"].get(),
            "email": self.entries["email"].get(),
            "age": int(self.entries["age"].get()),
            "genres": [g.strip() for g in self.entries["genres"].get().split(",") if g.strip()],
            "bio": self.entries["bio"].get(),
            "password": self.entries["password"].get(),
            "watched_movies": [],
            "registration_date": datetime.now().strftime("%Y-%m-%d"),
            "preferred_theme": self.current_theme
        }
        
        # Simple validation
        if not user_data["name"]:
            messagebox.showerror("Error", "Name is required")
            return
        if not user_data["email"] or "@" not in user_data["email"]:
            messagebox.showerror("Error", "Valid email is required")
            return
        if user_data["age"] < 13:
            messagebox.showerror("Error", "You must be at least 13 years old")
            return
        if len(user_data["password"]) < 6:
            messagebox.showerror("Error", "Password must be at least 6 characters")
            return
        
        self.current_user = user_data
        self.save_user_data()
        self.create_main_interface()

    def create_main_interface(self):
        self.clear_window()
        theme = self.themes[self.current_theme]
        
        # Create notebook (tabs)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill=tk.BOTH)
        
        # Profile tab
        profile_tab = ttk.Frame(self.notebook, style='TFrame')
        self.notebook.add(profile_tab, text="Profile")
        self.create_profile_tab(profile_tab)
        
        # Recommendations tab
        rec_tab = ttk.Frame(self.notebook, style='TFrame')
        self.notebook.add(rec_tab, text="Recommendations")
        self.create_recommendations_tab(rec_tab)
        
        # Watched movies tab
        watched_tab = ttk.Frame(self.notebook, style='TFrame')
        self.notebook.add(watched_tab, text="Watched Movies")
        self.create_watched_tab(watched_tab)
        
        # Theme selector and logout button
        bottom_frame = ttk.Frame(self.root, style='TFrame')
        bottom_frame.pack(fill=tk.X, pady=10)
        
        theme_frame = ttk.Frame(bottom_frame, style='TFrame')
        theme_frame.pack(side=tk.LEFT, padx=20)
        
        ttk.Label(theme_frame, text="Theme:", style='TLabel').pack(side=tk.LEFT)
        self.theme_var = tk.StringVar(value=self.current_theme)
        for theme_name in self.themes.keys():
            rb = ttk.Radiobutton(theme_frame, text=theme_name, variable=self.theme_var, 
                                value=theme_name, command=self.change_theme)
            rb.pack(side=tk.LEFT, padx=5)
        
        logout_btn = ttk.Button(bottom_frame, text="Logout", command=self.logout, 
                              style='Accent.TButton')
        logout_btn.pack(side=tk.RIGHT, padx=20)

    def create_profile_tab(self, parent):
        theme = self.themes[self.current_theme]
        
        # Header
        header_frame = ttk.Frame(parent, style='TFrame')
        header_frame.pack(fill=tk.X, pady=10)
        
        title_label = ttk.Label(header_frame, text="Your Profile", 
                              font=theme["font_title"], foreground=theme["accent"])
        title_label.pack(side=tk.LEFT)
        
        # Profile content
        content_frame = ttk.Frame(parent, style='TFrame')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Profile details
        details = [
            ("Name:", self.current_user["name"]),
            ("Email:", self.current_user["email"]),
            ("Age:", str(self.current_user["age"])),
            ("Member Since:", self.current_user["registration_date"]),
            ("Bio:", self.current_user["bio"] if self.current_user["bio"] else "Not provided")
        ]
        
        for label_text, value in details:
            frame = ttk.Frame(content_frame, style='TFrame')
            frame.pack(fill=tk.X, pady=5)
            
            label = ttk.Label(frame, text=label_text, width=15, anchor='w', 
                            font=theme["font_body"])
            label.pack(side=tk.LEFT)
            
            value_label = ttk.Label(frame, text=value, anchor='w', 
                                  font=theme["font_body"])
            value_label.pack(side=tk.LEFT, padx=10)
        
        # Favorite genres
        genres_frame = ttk.Frame(content_frame, style='TFrame')
        genres_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(genres_frame, text="Favorite Genres:", width=15, anchor='w', 
                font=theme["font_body"]).pack(side=tk.LEFT)
        
        if self.current_user["genres"]:
            for genre in self.current_user["genres"]:
                genre_label = ttk.Label(genres_frame, text=genre, background=theme["accent"], 
                                      foreground="white", padding=3, borderwidth=1, 
                                      relief="solid", font=theme["font_body"])
                genre_label.pack(side=tk.LEFT, padx=5)
        else:
            ttk.Label(genres_frame, text="Not specified", font=theme["font_body"]).pack(side=tk.LEFT)

    def create_recommendations_tab(self, parent):
        theme = self.themes[self.current_theme]
        
        # Header
        header_frame = ttk.Frame(parent, style='TFrame')
        header_frame.pack(fill=tk.X, pady=10)
        
        title_label = ttk.Label(header_frame, text="Personalized Recommendations", 
                              font=theme["font_title"], foreground=theme["accent"])
        title_label.pack(side=tk.LEFT)
        
        refresh_btn = ttk.Button(header_frame, text="Refresh", command=self.refresh_recommendations,
                               style='Accent.TButton')
        refresh_btn.pack(side=tk.RIGHT)
        
        # Loading indicator
        self.loading_label = ttk.Label(parent, text="Generating recommendations...", 
                                     font=theme["font_subtitle"], style='TLabel')
        self.loading_label.pack(pady=20)
        
        # Recommendations container
        self.rec_container = ttk.Frame(parent, style='TFrame')
        self.rec_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Simulate AI processing
        self.root.after(1500, self.generate_recommendations)

    def generate_recommendations(self):
        theme = self.themes[self.current_theme]
        self.loading_label.pack_forget()
        
        # Calculate scores for each movie
        scored_movies = []
        for movie in self.movie_db:
            score = 0
            
            # Score based on genre matches
            for genre in movie["genres"]:
                if genre in self.current_user["genres"]:
                    score += 30
            
            # Score based on rating
            score += movie["rating"] * 2
            
            # Penalize mature content for young users
            if self.current_user["age"] < 18 and movie["rating"] > 8.5:
                score -= 10
            
            # Add random factor to make it more interesting
            score += random.randint(0, 20)
            
            scored_movies.append({
                **movie,
                "match_score": min(100, max(0, score))
            })
        
        # Sort by score and take top 5
        scored_movies.sort(key=lambda x: x["match_score"], reverse=True)
        self.recommendations = scored_movies[:5]
        
        # Display recommendations
        self.display_recommendations()

    def display_recommendations(self):
        theme = self.themes[self.current_theme]
        
        # Clear previous recommendations
        for widget in self.rec_container.winfo_children():
            widget.destroy()
        
        if not self.recommendations:
            ttk.Label(self.rec_container, text="No recommendations available", 
                     font=theme["font_body"]).pack()
            return
        
        for movie in self.recommendations:
            movie_frame = ttk.Frame(self.rec_container, style='TFrame', padding=10, 
                                  relief="solid", borderwidth=1)
            movie_frame.pack(fill=tk.X, pady=5)
            
            # Match score indicator
            if movie["match_score"] > 70:
                score_color = theme["success"]
            elif movie["match_score"] > 40:
                score_color = theme["warning"]
            else:
                score_color = theme["highlight"]
                
            score_frame = ttk.Frame(movie_frame, style='TFrame')
            score_frame.pack(fill=tk.X)
            
            ttk.Label(score_frame, text=f"Match: {movie['match_score']:.0f}%", 
                     background=score_color, foreground="white", padding=3,
                     font=theme["font_body"]).pack(side=tk.RIGHT)
            
            # Movie title
            ttk.Label(movie_frame, text=movie["title"], 
                     font=theme["font_subtitle"]).pack(anchor='w')
            
            # Movie details
            details_frame = ttk.Frame(movie_frame, style='TFrame')
            details_frame.pack(fill=tk.X, pady=5)
            
            ttk.Label(details_frame, text=f"Year: {movie['year']}", 
                     font=theme["font_body"]).pack(side=tk.LEFT, padx=10)
            ttk.Label(details_frame, text=f"Rating: {movie['rating']}", 
                     font=theme["font_body"]).pack(side=tk.LEFT, padx=10)
            ttk.Label(details_frame, text=f"Duration: {movie['duration']} min", 
                     font=theme["font_body"]).pack(side=tk.LEFT, padx=10)
            
            # Genres
            genres_frame = ttk.Frame(movie_frame, style='TFrame')
            genres_frame.pack(fill=tk.X, pady=5)
            
            for genre in movie["genres"]:
                if genre in self.current_user["genres"]:
                    genre_color = theme["accent"]
                else:
                    genre_color = theme["secondary"]
                    
                ttk.Label(genres_frame, text=genre, background=genre_color, 
                         foreground="white", padding=3, font=theme["font_body"]).pack(side=tk.LEFT, padx=2)
            
            # Action buttons
            btn_frame = ttk.Frame(movie_frame, style='TFrame')
            btn_frame.pack(fill=tk.X, pady=(10, 0))
            
            if movie["title"] in self.current_user["watched_movies"]:
                ttk.Label(btn_frame, text="✓ Already watched", 
                         foreground=theme["success"], font=theme["font_body"]).pack(side=tk.LEFT)
            else:
                ttk.Button(btn_frame, text="Mark as Watched", 
                          command=lambda m=movie["title"]: self.mark_as_watched(m),
                          style='Accent.TButton').pack(side=tk.LEFT)

    def mark_as_watched(self, movie_title):
        if movie_title not in self.current_user["watched_movies"]:
            self.current_user["watched_movies"].append(movie_title)
            self.save_user_data()
            self.display_recommendations()
            self.create_watched_tab(self.notebook.nametowidget(self.notebook.tabs()[2]))

    def refresh_recommendations(self):
        theme = self.themes[self.current_theme]
        self.loading_label.config(font=theme["font_subtitle"])
        self.loading_label.pack(pady=20)
        self.rec_container.pack_forget()
