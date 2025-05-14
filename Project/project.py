import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime
import random
import os

class CineMate:
    def __init__(self, root):
        self.root = root
        self.root.title("CineMate - AI Movie Recommendations")
        self.root.geometry("1000x750")

        # Cinematic theme with updated background colors
        self.themes = {
            "Cinematic": {
                "bg": "#2c3e50",  # Dark blue background
                "fg": "#ecf0f1",  # Light foreground text
                "accent": "#e74c3c",  # Red accent for action buttons
                "highlight": "#f39c12",  # Yellow highlight for important info
                "secondary": "#34495e",  # Darker secondary color
                "success": "#2ecc71",  # Green for success indicators
                "warning": "#f39c12",  # Yellow for warning
                "font_title": ("Times New Roman", 28, "bold"),
                "font_subtitle": ("Times New Roman", 18),
                "font_body": ("Times New Roman", 12),
            }
        }

        self.current_theme = "Cinematic"
        self.apply_theme()

        self.movie_db = [
            {"title": "Inception", "genres": ["Sci-Fi", "Action"], "rating": 8.8, "year": 2010, "duration": 148},
            {"title": "The Shawshank Redemption", "genres": ["Drama"], "rating": 9.3, "year": 1994, "duration": 142},
            {"title": "Pulp Fiction", "genres": ["Crime", "Drama"], "rating": 8.9, "year": 1994, "duration": 154},
            {"title": "The Dark Knight", "genres": ["Action", "Crime", "Drama"], "rating": 9.0, "year": 2008, "duration": 152},
            {"title": "Fight Club", "genres": ["Drama"], "rating": 8.8, "year": 1999, "duration": 139},
            {"title": "Forrest Gump", "genres": ["Drama", "Romance"], "rating": 8.8, "year": 1994, "duration": 142},
            {"title": "The Matrix", "genres": ["Action", "Sci-Fi"], "rating": 8.7, "year": 1999, "duration": 136},
            {"title": "Goodfellas", "genres": ["Crime", "Drama"], "rating": 8.7, "year": 1990, "duration": 146},
            {"title": "The Silence of the Lambs", "genres": ["Crime", "Thriller"], "rating": 8.6, "year": 1991, "duration": 118},
            {"title": "Interstellar", "genres": ["Adventure", "Drama", "Sci-Fi"], "rating": 8.6, "year": 2014, "duration": 169},
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

        self.style = ttk.Style()
        self.style.theme_use('clam')

        self.style.configure('.', background=theme["bg"], foreground=theme["fg"], font=theme["font_body"])
        self.style.configure('TFrame', background=theme["bg"])
        self.style.configure('TLabel', background=theme["bg"], foreground=theme["fg"], font=theme["font_body"])
        self.style.configure('TButton', font=theme["font_body"], padding=10, relief="flat")
        self.style.configure('Accent.TButton', background=theme["accent"], foreground=theme["fg"], padding=10)
        self.style.map('TButton', background=[('active', theme["accent"])])

    def load_user_data(self):
        try:
            with open('cinemate_user.json', 'r') as f:
                self.current_user = json.load(f)
        except:
            self.current_user = None

    def save_user_data(self):
        with open('cinemate_user.json', 'w') as f:
            json.dump(self.current_user, f)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_login_interface(self):
        self.clear_window()
        theme = self.themes[self.current_theme]

        frame = ttk.Frame(self.root, padding=30)
        frame.pack(expand=True)

        ttk.Label(frame, text="Welcome to CineMate", font=theme["font_title"], foreground=theme["accent"]).pack(pady=20)
        ttk.Label(frame, text="Please Register to get started", font=theme["font_subtitle"]).pack(pady=10)

        self.entries = {}
        fields = [
            ("Name", "name"),
            ("Email", "email"),
            ("Age", "age"),
            ("Favorite Genres (comma separated)", "genres"),
            ("Bio", "bio"),
            ("Password", "password", True)
        ]

        for label, key, *password in fields:
            f = ttk.Frame(frame)
            f.pack(fill=tk.X, pady=10)
            ttk.Label(f, text=label, width=25).pack(side=tk.LEFT)
            entry = ttk.Entry(f, show="*" if password else "")
            entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
            self.entries[key] = entry

        ttk.Button(frame, text="Register", command=self.register_user, style='Accent.TButton').pack(pady=20)

    def register_user(self):
        try:
            data = {
                "name": self.entries["name"].get(),
                "email": self.entries["email"].get(),
                "age": int(self.entries["age"].get()),
                "genres": [g.strip() for g in self.entries["genres"].get().split(",")],
                "bio": self.entries["bio"].get(),
                "password": self.entries["password"].get(),
                "watched_movies": [],
                "registration_date": datetime.now().strftime("%Y-%m-%d"),
                "preferred_theme": self.current_theme
            }

            if not data["name"] or not data["email"] or "@" not in data["email"]:
                raise ValueError("Invalid name or email.")
            if data["age"] < 13 or len(data["password"]) < 6:
                raise ValueError("Age must be >=13 and password >=6 characters.")

            self.current_user = data
            self.save_user_data()
            self.create_main_interface()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def create_main_interface(self):
        self.clear_window()
        theme = self.themes[self.current_theme]

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill=tk.BOTH)

        tabs = [
            ("Profile", self.create_profile_tab),
            ("Recommendations", self.create_recommendations_tab),
            ("Watched Movies", self.create_watched_tab)
        ]

        for name, func in tabs:
            tab = ttk.Frame(self.notebook)
            self.notebook.add(tab, text=name)
            func(tab)

        bottom = ttk.Frame(self.root)
        bottom.pack(fill=tk.X, pady=15)
        ttk.Button(bottom, text="Logout", command=self.logout, style='Accent.TButton').pack(side=tk.RIGHT, padx=20)

    def create_profile_tab(self, parent):
        user = self.current_user
        theme = self.themes[self.current_theme]

        ttk.Label(parent, text="Your Profile", font=theme["font_title"], foreground=theme["accent"]).pack(pady=20)

        info = [
            ("Name", user["name"]),
            ("Email", user["email"]),
            ("Age", str(user["age"])),
            ("Member Since", user["registration_date"]),
            ("Bio", user["bio"] or "N/A")
        ]

        for label, value in info:
            row = ttk.Frame(parent)
            row.pack(anchor="w", padx=30, pady=10)
            ttk.Label(row, text=f"{label}:", width=18).pack(side=tk.LEFT)
            ttk.Label(row, text=value, font=("Times New Roman", 12)).pack(side=tk.LEFT)

        ttk.Label(parent, text="Favorite Genres:", font=("Times New Roman", 14)).pack(anchor="w", padx=30)
        genre_frame = ttk.Frame(parent)
        genre_frame.pack(anchor="w", padx=30)
        for g in user["genres"]:
            ttk.Label(genre_frame, text=g, background=theme["accent"], foreground="white", padding=5).pack(side=tk.LEFT, padx=5)

    def create_recommendations_tab(self, parent):
        theme = self.themes[self.current_theme]

        self.loading_label = ttk.Label(parent, text="Generating recommendations...", font=theme["font_subtitle"])
        self.loading_label.pack(pady=30)

        self.recommendations_frame = ttk.Frame(parent)
        self.recommendations_frame.pack(expand=True, fill=tk.BOTH, padx=30, pady=20)

        self.root.after(1500, self.generate_recommendations)

    def generate_recommendations(self):
        user = self.current_user
        scored = []
        for m in self.movie_db:
            score = sum(30 for g in m["genres"] if g in user["genres"])
            score += m["rating"] * 2
            if user["age"] < 18 and m["rating"] > 8.5:
                score -= 10
            score += random.randint(0, 20)
            m["match_score"] = min(100, max(0, score))
            scored.append(m)

        self.recommendations = sorted(scored, key=lambda x: x["match_score"], reverse=True)[:5]
        self.display_recommendations()

    def display_recommendations(self):
        theme = self.themes[self.current_theme]
        self.loading_label.pack_forget()

        for widget in self.recommendations_frame.winfo_children():
            widget.destroy()

        for movie in self.recommendations:
            card = ttk.Frame(self.recommendations_frame, padding=20, style="TFrame")
            card.pack(side=tk.LEFT, padx=20, pady=20)

            movie_card = tk.Frame(card, bg=theme["secondary"], relief="flat", width=200, height=300)
            movie_card.pack_propagate(False)  # Prevent the card from resizing

            title = ttk.Label(movie_card, text=movie["title"], font=("Times New Roman", 14, "bold"), foreground=theme["accent"], anchor="center")
            title.pack(pady=10)

            rating = ttk.Label(movie_card, text=f"Rating: {movie['rating']}", font=("Times New Roman", 12), anchor="center")
            rating.pack(pady=5)

            genres = ttk.Label(movie_card, text=", ".join(movie["genres"]), font=("Times New Roman", 12), anchor="center")
            genres.pack(pady=5)

            match_score = ttk.Label(movie_card, text=f"Match: {movie['match_score']}%", font=("Times New Roman", 12), anchor="center")
            match_score.pack(pady=5)

            movie_card.pack_propagate(False)
            movie_card.pack()

        # Add refresh button
        ttk.Button(self.recommendations_frame, text="Refresh", command=self.refresh_recommendations, style='Accent.TButton').pack(pady=20)

    def refresh_recommendations(self):
        self.generate_recommendations()

    def create_watched_tab(self, parent):
        theme = self.themes[self.current_theme]
        for widget in parent.winfo_children():
            widget.destroy()

        ttk.Label(parent, text="Watched Movies", font=theme["font_title"], foreground=theme["accent"]).pack(pady=30)

        if not self.current_user["watched_movies"]:
            ttk.Label(parent, text="You haven't marked any movies as watched yet.", font=theme["font_body"]).pack()
        else:
            for title in self.current_user["watched_movies"]:
                ttk.Label(parent, text=title, font=theme["font_body"]).pack(anchor="w", padx=30)

    def logout(self):
        self.current_user = None
        try:
            os.remove('cinemate_user.json')
        except FileNotFoundError:
            pass
        self.create_login_interface()

if __name__ == "__main__":
    root = tk.Tk()
    app = CineMate(root)
    root.mainloop()
