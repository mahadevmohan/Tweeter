# gui.py

import tkinter as tk
from tkinter import font
import re
from PIL import Image, ImageTk, ImageDraw  # Import Pillow modules


def start_gui():
    """
    Initializes and runs the Tkinter GUI.
    """
    # Create the main window
    root = tk.Tk()
    root.title("Retro Themed GUI")
    root.geometry("1000x750")
    root.resizable(False, False)  # Prevent window resizing for consistent layout

    # Set background color to Twitter blue
    root.configure(bg="#1DA1F2")

    # Create the main frame with off-white background and 10-pixel border
    main_frame = tk.Frame(root, bg="#F8F0E3")
    main_frame.place(relx=0, rely=0, relwidth=1, relheight=1, x=10, y=10, width=-20, height=-20)

    # Define the retro fonts
    title_font = font.Font(family="Courier New", size=36, weight="bold")
    retro_font = font.Font(family="Courier New", size=16, weight="bold")
    tweet_font = font.Font(family="Courier New", size=16)  # For tweet text

    # Create a label with the word 'tweeter' at the top
    title_label = tk.Label(
        main_frame,
        text="tweeter",
        font=title_font,
        bg="#F8F0E3",
        fg="black"
    )
    title_label.pack(pady=(20, 10))

    # Frame to hold either the text box or the tweet
    content_frame = tk.Frame(main_frame, bg="#F8F0E3")
    content_frame.pack(pady=10, fill='both', expand=True)

    # Create a Text widget to simulate the post box
    text_box = tk.Text(
        content_frame,
        font=retro_font,
        bg="#FFFFFF",
        fg="black",
        width=60,
        height=10,
        wrap='word',
        borderwidth=2,
        relief="groove"
    )
    text_box.pack(pady=10)

    # Configure tag for hashtags
    text_box.tag_configure("hashtag", foreground="#1DA1F2", font=retro_font)

    # Function to highlight hashtags
    def highlight_hashtags(event=None):
        text_box.tag_remove("hashtag", "1.0", "end")
        text = text_box.get("1.0", "end-1c")
        for match in re.finditer(r'#[\w]+', text):
            start_index = f"1.0+{match.start()}c"
            end_index = f"1.0+{match.end()}c"
            text_box.tag_add("hashtag", start_index, end_index)

    # Bind the function to key release event
    text_box.bind("<KeyRelease>", highlight_hashtags)

    # Variable to hold tweet_frame
    tweet_frame = None

    # Function to handle 'TWIT' button click
    def post_tweet():
        nonlocal tweet_frame
        content = text_box.get("1.0", "end-1c").strip()
        if content:
            # Hide the text box
            text_box.pack_forget()
            # Change the button text to 'DONE' and update its command
            post_button.config(text="DONE", command=reset_interface)

            # Create the tweet frame with a white background and padding
            tweet_frame = tk.Frame(content_frame, bg="#FFFFFF", bd=2, relief="groove")
            tweet_frame.pack(fill='x', expand=False, pady=10, padx=50)  # Added padx=50 for left and right padding

            # Debugging: Add a border color to visualize the frame
            # tweet_frame.configure(highlightbackground="red", highlightthickness=1)

            # Create the top part of the tweet (avatar and user info)
            top_frame = tk.Frame(tweet_frame, bg="#FFFFFF")
            top_frame.pack(fill='x', pady=10, padx=10)

            #Avatar
            avatar_size = 50
            avatar_canvas = tk.Canvas(top_frame, width=avatar_size, height=avatar_size, bg="#FFFFFF", highlightthickness=0)
            avatar_canvas.pack(side='left')

            # Load and display the avatar image
            try:
                # Path to your avatar image
                avatar_image_path = "Assets/avatar.png"  # Update this path as needed

                # Open the image using PIL
                avatar_image = Image.open(avatar_image_path).convert("RGBA")
                print("Avatar image loaded successfully.")

                # Resize the image to fit the avatar size
                avatar_image = avatar_image.resize((avatar_size, avatar_size), Image.Resampling.LANCZOS)

                # Create a circular mask
                mask = Image.new("L", (avatar_size, avatar_size), 0)
                draw = ImageDraw.Draw(mask)
                draw.ellipse((0, 0, avatar_size, avatar_size), fill=255)

                # Apply the mask to the image
                avatar_image.putalpha(mask)

                # Convert the image to a PhotoImage
                avatar_photo = ImageTk.PhotoImage(avatar_image)

                # Add the image to the canvas
                avatar_canvas.create_image(avatar_size//2, avatar_size//2, image=avatar_photo)

                # Keep a reference to prevent garbage collection
                avatar_canvas.image = avatar_photo
                print("Avatar image displayed successfully.")

            except Exception as e:
                print(f"Error loading avatar image: {e}")
                # Fallback: Draw a simple circular avatar (placeholder)
                avatar_canvas.create_oval(2, 2, avatar_size-2, avatar_size-2, fill="#A9A9A9", outline="")
                print("Displayed placeholder avatar.")


            # User Info Frame
            user_info_frame = tk.Frame(top_frame, bg="#FFFFFF")
            user_info_frame.pack(side='left', padx=10)

            # User Name Label
            user_name_label = tk.Label(
                user_info_frame,
                text="Twit User",
                font=retro_font,
                bg="#FFFFFF",
                fg="black"
            )
            user_name_label.pack(anchor='w')

            # Username Label
            username_label = tk.Label(
                user_info_frame,
                text="@TwitUser_69",
                font=font.Font(family="Courier New", size=12),
                bg="#FFFFFF",
                fg="grey"
            )
            username_label.pack(anchor='w')

            # Tweet Text
            tweet_text_widget = tk.Text(
                tweet_frame,
                font=tweet_font,
                bg="#FFFFFF",
                fg="black",
                width=60,
                height=5,  # Adjusted height for better visibility
                wrap='word',
                borderwidth=0,
                highlightthickness=0
            )
            tweet_text_widget.pack(padx=10, pady=(0, 10))
            tweet_text_widget.insert("1.0", content)
            tweet_text_widget.config(state='disabled')  # Make it read-only

            # Configure tag for hashtags in tweet
            tweet_text_widget.tag_configure("hashtag", foreground="#1DA1F2", font=retro_font)

            # Apply hashtag formatting
            for match in re.finditer(r'#[\w]+', content):
                start = f"1.0+{match.start()}c"
                end = f"1.0+{match.end()}c"
                tweet_text_widget.tag_add("hashtag", start, end)

            # Create counters frame aligned to the left
            counters_frame = tk.Frame(tweet_frame, bg="#FFFFFF")
            counters_frame.pack(anchor='w', padx=10, pady=(0, 10))

            # Define counter labels
            counters = {
                "Likes": 0,
                "Comments": 0,
                "Retweets": 0
            }

            # Create and pack counter labels
            for idx, (key, value) in enumerate(counters.items()):
                counter_label = tk.Label(
                    counters_frame,
                    text=f"{key}: {value}",
                    font=retro_font,
                    bg="#FFFFFF",
                    fg="black",
                    padx=10
                )
                counter_label.grid(row=0, column=idx, padx=10, sticky='w')

        else:
            # If the text box is empty, you might want to handle it (currently nothing)
            pass

    # Function to reset the interface back to the text box
    def reset_interface():
        nonlocal tweet_frame
        if tweet_frame:
            tweet_frame.destroy()
            tweet_frame = None
        # Re-pack the text box
        text_box.pack(pady=10)
        # Reset the button to 'TWIT' and its command
        post_button.config(text="TWIT", command=post_tweet)
        # Clear the text box
        text_box.delete("1.0", "end")

    # Create a 'TWIT' button below the text box
    post_button = tk.Button(
        main_frame,
        text="TWIT",
        font=retro_font,
        bg="#1DA1F2",
        fg="#000000",
        activebackground="#1DA1F2",
        activeforeground="#000000",
        highlightbackground="#1DA1F2",
        highlightthickness=0,
        command=post_tweet  # Assign the command
    )
    post_button.pack(pady=20)

    # Start the Tkinter main loop
    root.mainloop()
