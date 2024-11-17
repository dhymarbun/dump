import requests
import tkinter as tk
from tkinter import ttk, messagebox

GENIUS_API_KEY = "your_genius_api_key_here"


def search_songs_by_words(words):
    url = "https://api.genius.com/search"
    headers = {"Authorization": f"Bearer {GENIUS_API_KEY}"}
    params = {"q": words}

    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        return f"Error: Unable to fetch data (Status Code: {response.status_code})"

    data = response.json()
    hits = data.get("response", {}).get("hits", [])
    if not hits:
        return "No songs found."

    results = []
    for hit in hits:
        title = hit["result"]["title"]
        artist = hit["result"]["primary_artist"]["name"]
        url = hit["result"]["url"]
        results.append(f"{title} by {artist}\nLyrics: {url}")

    return results


def on_search():
    words = search_entry.get()
    if not words.strip():
        messagebox.showwarning("Input Error", "Please enter some words to search.")
        return

    results = search_songs_by_words(words)
    if isinstance(results, str):  # Error or no results message
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, results)
    else:
        result_text.delete("1.0", tk.END)
        for result in results:
            result_text.insert(tk.END, result + "\n\n")


root = tk.Tk()
root.title("Song Search")

frame = ttk.Frame(root, padding=10)
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

search_label = ttk.Label(frame, text="Enter words or phrases:")
search_label.grid(row=0, column=0, sticky=tk.W)

search_entry = ttk.Entry(frame, width=50)
search_entry.grid(row=0, column=1, sticky=(tk.W, tk.E))

search_button = ttk.Button(frame, text="Search", command=on_search)
search_button.grid(row=0, column=2, sticky=tk.W)

result_text = tk.Text(frame, width=80, height=20, wrap=tk.WORD)
result_text.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E))

scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=result_text.yview)
result_text.configure(yscrollcommand=scrollbar.set)
scrollbar.grid(row=1, column=3, sticky=(tk.N, tk.S))

root.mainloop()
