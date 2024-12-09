# gui.py

import tkinter as tk
from tkinter import font, messagebox
import re
from PIL import Image, ImageTk, ImageDraw
import music
import threading
import time
import ai  # Import the AI module
import random  # Import random for GDP animation

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
    comment_font = font.Font(family="Courier New", size=12)  # For comments
    counter_font = font.Font(family="Courier New", size=48, weight="bold")  # Large size for visibility

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

    # Initialize counter variables
    initial_gdp = 20000000000000  # $20,000,000,000,000
    counter_var = tk.StringVar()
    counter_var.set("${:,.0f}".format(initial_gdp))
    counter_label = tk.Label(
        main_frame,
        textvariable=counter_var,
        font=counter_font,
        bg="#F8F0E3",
        fg="black"
    )
    counter_label.pack(side='bottom', pady=20)

    # Initialize current counter value
    current_counter_value = initial_gdp
    # Define the maximum digits as per the initial display
    # $000,000,000,000,000 has 15 digits (excluding $ and commas)
    # So maximum is 999,999,999,999,999
    max_counter_value = 999999999999999

    # Initialize relationships
    relationships = {
        "China": "Neutral",
        "India": "Neutral",
        "Russia": "Neutral"
    }

    # Lock to prevent multiple simultaneous counter updates
    counter_lock = threading.Lock()

    # Function to format the counter value
    def format_counter(value):
        return "${:,.0f}".format(value)

    # Function to animate the counter increment/decrement
    def animate_counter(target, duration_ms=5000, stop_music=False):
        nonlocal current_counter_value
        start_value = current_counter_value
        total_change = target - start_value
        start_time = None

        def step():
            nonlocal current_counter_value, start_time
            if start_time is None:
                start_time = time.time()  # Record the start time

            elapsed_time = (time.time() - start_time) * 1000  # Elapsed time in milliseconds
            if elapsed_time < duration_ms:
                progress = elapsed_time / duration_ms
                # Calculate the new counter value
                new_value = int(start_value + total_change * progress)
                if new_value != current_counter_value:
                    current_counter_value = new_value
                    counter_var.set(format_counter(current_counter_value))
                # Schedule the next update
                root.after(50, step)  # Update every 50ms
            else:
                # Animation complete
                current_counter_value = target
                counter_var.set(format_counter(current_counter_value))
                if stop_music:
                    music.stop_points_sound()

        # Start the animation
        step()

    # Function to start the counter animation
    def update_counter_animation(change_amount_trillion):
        nonlocal current_counter_value
        # Convert trillions to the actual amount
        change_amount = change_amount_trillion * 1_000_000_000_000
        new_target = current_counter_value + change_amount
        print(f"Current GDP: {current_counter_value}")
        print(f"Change Amount: {change_amount}")
        print(f"New Target GDP: {new_target}")
        if new_target > max_counter_value:
            new_target = max_counter_value
        elif new_target < 0:
            new_target = 0  # Prevent negative GDP

        # Determine if GDP is increasing or decreasing
        direction = "increase" if change_amount >= 0 else "decrease"

        # Start the animation, indicating to stop music when done
        root.after(0, lambda: animate_counter(new_target, duration_ms=5000, stop_music=True))

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

            # Create the top part of the tweet (avatar and user info)
            top_frame = tk.Frame(tweet_frame, bg="#FFFFFF")
            top_frame.pack(fill='x', pady=10, padx=10)

            # Avatar
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
                text="President",
                font=retro_font,
                bg="#FFFFFF",
                fg="black"
            )
            user_name_label.pack(anchor='w')

            # Username Label
            username_label = tk.Label(
                user_info_frame,
                text="@USPresident",
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

            # Create a loading label
            loading_label = tk.Label(
                tweet_frame,
                text="Loading AI responses...",
                font=retro_font,
                bg="#FFFFFF",
                fg="#555555"
            )
            loading_label.pack(pady=(10, 0))

            # Start the random GDP animation while waiting for AI response
            start_random_gdp_animation()

            # Call the AI to generate responses
            # Define the current situation, global players, and GDP
            situation = "The UN proposes a lottery to distribute pieces of the moon to nations. Everyone is lobbying for a larger slice."
            global_players = ["China", "India", "Russia"]
            current_gdp = current_counter_value

            def handle_ai_response(ai_data):
                if ai_data:
                    # Schedule GUI updates in the main thread
                    root.after(0, lambda: process_ai_data(ai_data))
                else:
                    root.after(0, lambda: handle_ai_error())

            def process_ai_data(ai_data):
                try:
                    loading_label.destroy()
                except:
                    pass
                stop_random_gdp_animation()
                display_ai_responses(ai_data)

            def handle_ai_error():
                try:
                    loading_label.destroy()
                except:
                    pass
                stop_random_gdp_animation()
                messagebox.showerror("AI Error", "Failed to generate AI responses.")

            ai.generate_responses(
                situation=situation,
                global_players=global_players,
                current_gdp=current_gdp,
                user_tweet=content,
                callback=handle_ai_response
            )

    # Variables to manage random GDP animation
    random_gdp_thread = None
    random_gdp_running = False

    def start_random_gdp_animation():
        """
        Starts a thread that randomly animates the GDP counter while waiting for AI response.
        """
        global random_gdp_thread, random_gdp_running

        random_gdp_running = True

        # Start playing the music when starting random GDP animation
        music.play_points_sound()

        def random_animation():
            while random_gdp_running:
                # Randomly decide to increase or decrease by up to 0.1 trillion
                change = random.uniform(-0.1, 0.1)
                # Update the GDP counter accordingly
                root.after(0, lambda: random_gdp_change(change))
                # Wait for a short interval before next change
                time.sleep(0.5)

        random_gdp_thread = threading.Thread(target=random_animation, daemon=True)
        random_gdp_thread.start()

    def stop_random_gdp_animation():
        """
        Stops the random GDP animation thread.
        """
        global random_gdp_running
        random_gdp_running = False

    def random_gdp_change(change_trillion):
        """
        Applies a small random change to the GDP counter.
        """
        nonlocal current_counter_value
        change_amount = change_trillion * 1_000_000_000_000  # Convert to actual amount
        new_target = current_counter_value + change_amount
        if new_target > max_counter_value:
            new_target = max_counter_value
        elif new_target < 0:
            new_target = 0  # Prevent negative GDP

        # Start the animation to the new target
        animate_counter(new_target, duration_ms=400)  # Shorter duration for random changes

    # Function to display AI responses as comments
    def display_ai_responses(ai_data):
        """
        Displays AI-generated responses below the user's tweet, updates GDP and relationships, and shows a summary popup.
        """
        nonlocal current_counter_value, relationships

        # Extract data from ai_data
        responses = ai_data.get("responses", {})
        gdp_impact = ai_data.get("gdp_impact", {})
        relationships_update = ai_data.get("relationships", {})

        # Update relationships
        for country, status in relationships_update.items():
            relationships[country] = status

        # Update GDP
        direction = gdp_impact.get("direction", "increase")
        amount_trillion = gdp_impact.get("amount_trillion", 0)
        print(f"Original amount_trillion: {amount_trillion}")
        # Ensure amount_trillion is within -1 and +1
        amount_trillion = max(-1, min(amount_trillion, 1))
        print(f"Clamped amount_trillion: {amount_trillion}")
        change_amount_trillion = amount_trillion if direction == "increase" else -amount_trillion
        print(f"Change amount_trillion: {change_amount_trillion}")
        update_counter_animation(change_amount_trillion)

        # Display responses as comments
        for country, tweet in responses.items():
            comment_frame = tk.Frame(tweet_frame, bg="#F0F0F0", bd=1, relief="solid")
            comment_frame.pack(fill='x', padx=60, pady=5)

            # Comment User Info
            comment_user_frame = tk.Frame(comment_frame, bg="#F0F0F0")
            comment_user_frame.pack(fill='x', pady=5, padx=5)

            comment_user_label = tk.Label(
                comment_user_frame,
                text=country,
                font=retro_font,
                bg="#F0F0F0",
                fg="black"
            )
            comment_user_label.pack(side='left')

            # Comment Text
            comment_text = tk.Text(
                comment_frame,
                font=comment_font,
                bg="#F0F0F0",
                fg="black",
                width=50,
                height=2,
                wrap='word',
                borderwidth=0,
                highlightthickness=0
            )
            comment_text.pack(padx=5, pady=(0, 5))
            comment_text.insert("1.0", tweet)
            comment_text.config(state='disabled')  # Make it read-only

        # Show the final popup after displaying all responses
        show_final_popup(change_amount_trillion, relationships_update)

    # Function to show the final popup with GDP shift and relationships
    def show_final_popup(change_amount_trillion, relationships_update):
        """
        Displays a popup summarizing the GDP shift and relationship changes.
        """
        popup = tk.Toplevel(root)
        popup.title("Situation Outcome")
        popup.geometry("500x300")
        popup.resizable(False, False)
        popup.configure(bg="#F8F0E3")  # Off-white background

        # Make the pop-up modal
        popup.grab_set()

        # Center the pop-up on the screen
        root.update_idletasks()
        x = (root.winfo_screenwidth() // 2) - (500 // 2)
        y = (root.winfo_screenheight() // 2) - (300 // 2)
        popup.geometry(f"+{x}+{y}")

        # Title Label
        title_label = tk.Label(
            popup,
            text="Situation Outcome",
            font=font.Font(family="Courier New", size=24, weight="bold"),
            bg="#F8F0E3",
            fg="black"
        )
        title_label.pack(pady=20)

        # GDP Shift
        gdp_direction = "Increased" if change_amount_trillion >= 0 else "Decreased"
        gdp_shift_label = tk.Label(
            popup,
            text=f"GDP {gdp_direction} by ${abs(change_amount_trillion)} Trillion",
            font=retro_font,
            bg="#F8F0E3",
            fg="black"
        )
        gdp_shift_label.pack(pady=10)

        # Relationships
        relationships_label = tk.Label(
            popup,
            text="Current Relationships:",
            font=retro_font,
            bg="#F8F0E3",
            fg="black"
        )
        relationships_label.pack(pady=10)

        # List of Relationships
        for country, status in relationships_update.items():
            rel_label = tk.Label(
                popup,
                text=f"{country}: {status}",
                font=retro_font,
                bg="#F8F0E3",
                fg="black"
            )
            rel_label.pack(anchor='w', padx=50)

        # Close Button
        close_button = tk.Button(
            popup,
            text="OK",
            font=retro_font,
            bg="#1DA1F2",
            fg="#000000",
            activebackground="#1DA1F2",
            activeforeground="#000000",
            highlightbackground="#1DA1F2",
            highlightthickness=0,
            command=popup.destroy
        )
        close_button.pack(pady=20)

        # Ensure the pop-up stays on top
        popup.transient(root)
        popup.focus_set()
        popup.wait_window()

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
        # Show the pop-up when 'DONE' is clicked
        show_popup()

    # Function to create and display the initial pop-up
    def show_popup():
        popup = tk.Toplevel(root)
        popup.title("Situation")
        popup.geometry("500x300")
        popup.resizable(False, False)
        popup.configure(bg="#F8F0E3")  # Off-white background

        # Make the pop-up modal
        popup.grab_set()

        # Center the pop-up on the screen
        root.update_idletasks()
        x = (root.winfo_screenwidth() // 2) - (500 // 2)
        y = (root.winfo_screenheight() // 2) - (300 // 2)
        popup.geometry(f"+{x}+{y}")

        # Situation Message
        message_label = tk.Label(
            popup,
            text="Situation 1:\n\n\n\nThe UN proposes a lottery to distribute \npieces of the moon to nations. \n\n\n\nEveryone is lobbying for a larger slice.",
            font=font.Font(family="Courier New", size=16, weight="bold"),
            bg="#F8F0E3",
            fg="black",
            justify="center"
        )
        message_label.pack(pady=40)

        # BEGIN! button
        begin_button = tk.Button(
            popup,
            text="BEGIN!",
            font=retro_font,
            bg="#1DA1F2",
            fg="#000000",
            activebackground="#1DA1F2",
            activeforeground="#000000",
            highlightbackground="#1DA1F2",
            highlightthickness=0,
            command=popup.destroy
        )
        begin_button.pack(pady=20)

        # Ensure the pop-up stays on top
        popup.transient(root)
        popup.focus_set()
        popup.wait_window()

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

    # Show the initial pop-up when the GUI starts
    root.after(100, show_popup)  # Use after to ensure the main window is fully initialized

    # Start the Tkinter main loop
    root.mainloop()
