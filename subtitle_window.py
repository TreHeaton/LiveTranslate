
import tkinter as tk
from tkinter import ttk


class SubtitleWindow:
    def __init__(self, root):
        self.root = root

        self.root.title("LiveTranslate v0.7")
        self.root.geometry("750x450")
        self.root.configure(bg="#111827")

        # Main heading
        title = tk.Label(
            root,
            text="LiveTranslate",
            font=("Arial", 24, "bold"),
            fg="white",
            bg="#111827"
        )
        title.pack(pady=(25, 5))

        # Application status
        self.status_label = tk.Label(
            root,
            text="Ready",
            font=("Arial", 12),
            fg="#34D399",
            bg="#111827"
        )
        self.status_label.pack(pady=5)

        # English subtitle heading
        english_label = tk.Label(
            root,
            text="ORIGINAL - ENGLISH",
            font=("Arial", 11, "bold"),
            fg="#9CA3AF",
            bg="#111827"
        )
        english_label.pack(pady=(25, 5))

        # English subtitle
        self.english_text = tk.Label(
            root,
            text="Waiting for speech...",
            font=("Arial", 18),
            fg="white",
            bg="#1F2937",
            wraplength=650,
            width=45,
            height=3
        )
        self.english_text.pack(padx=25, pady=5)

        # Translation heading
        self.translation_label = tk.Label(
            root,
            text="TRANSLATED",
            font=("Arial", 11, "bold"),
            fg="#9CA3AF",
            bg="#111827"
        )
        self.translation_label.pack(pady=(20, 5))

        # Translated subtitle
        self.translated_text = tk.Label(
            root,
            text="Translation will appear here...",
            font=("Arial", 20, "bold"),
            fg="#60A5FA",
            bg="#1F2937",
            wraplength=650,
            width=40,
            height=3
        )
        self.translated_text.pack(padx=25, pady=5)

    def update_subtitles(
        self,
        english,
        translated,
        language="French"
    ):
        """Update the displayed subtitles."""

        self.english_text.config(text=english)

        self.translated_text.config(text=translated)

        self.translation_label.config(
            text=f"TRANSLATED - {language.upper()}"
        )

        self.status_label.config(
            text="Translation completed"
        )


def main():
    root = tk.Tk()

    app = SubtitleWindow(root)

    # Temporary test subtitles
    app.update_subtitles(
        "How are you guys doing today?",
        "Comment ça va, les gars ?",
        "French"
    )

    root.mainloop()


if __name__ == "__main__":
    main()
