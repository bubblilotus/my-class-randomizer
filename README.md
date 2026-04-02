# 🏆 Classroom Random Name Picker

A fun, interactive web app for teachers to randomly select students without picking the same person twice in a single round.

## 🎮 Features
- **Fair Picking:** Uses weighted logic so everyone gets exactly one turn.
- **Video Game FX:** Plays a "Victory" sound effect and shows balloons when a name is picked.
- **Custom Lists:** Upload any `.txt` file with student names to get started.
- **Suspenseful Reveal:** Includes a short delay and "Drumroll" animation to build excitement in the classroom.

## 🚀 How to Use
1. **Upload:** Drop a text file with student names into the sidebar.
2. **Click:** Hit the "Pick a Student" button.
3. **Celebrate:** Listen for the win sound and see the winner on screen!

## 💻 Tech Stack
- **Python** 🐍
- **Streamlit** (Web Framework)
- **Base64** (For custom audio injection)

## 📂 Project Structure
- `app.py`: The main logic for the randomizer.
- `win_sound.mp3`: The victory sound effect.
- `requirements.txt`: Tells the server to install Streamlit.