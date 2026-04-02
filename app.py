import streamlit as st
import random
import time
import base64
# --- ui ---
st.title("Classroom Name Picker")
st.write("Click the button to pick a student fairly!")

#methods
# open file and get names
# def get_student_names(file_name):
#
#     with open(file_name, "r") as file:
#         names = [line.strip() for line in file.readlines()]
#     return names
#this reads names from a file upload
def get_student_names(uploaded_file):
    #turn bytes to regular text
    content = uploaded_file.read().decode("utf-8")
    names = [line.strip() for line in content.splitlines() if line.strip()]
    return names

#check if anyone was picked already
def get_picking_history(history_file_name):
    # see if we picked anyone yesterday
    try:
        with open(history_file_name, "r") as file:
            already_picked = [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        already_picked = []
    return already_picked
def reset_memory(list_of_names, history_of_picks, session_key):
    # if everyone has been picked already, reset
    # compare how many students we have
    # vs how many have been picked
    names_picked_so_far = len(history_of_picks)
    if names_picked_so_far >= len(list_of_names):
        # print("everyone has had a turn! Resetting memory~")
        # with open(history_file_name, "w") as file:
        #     file.write("")  # .write overwrites so this resets the file
        st.info("everyone has had a turn! Resetting memory~")
        st.session_state[session_key] = []
        history_of_picks = [] #clears history
    return history_of_picks
def set_weights(list_of_names, history_of_picks):
    # everyone gets a weight to 10 to start
    # creates let's say we have 3 students then
    # [10, 10, 10]
    # unless student was picked yesterday then set to 1
    student_weights = []
    for name in list_of_names:
        if name in history_of_picks:
            # if student got picked yesterday, set weight to 1
            student_weights.append(0)  # harder to pick
        else:
            student_weights.append(10)  # easier to pick
    return student_weights
def add_student_to_history(history_of_picks, picked_name):
    # save who was picked so they don't get picked again later
    # with open(history_file, "a") as file:
    #     file.write(picked_name + "\n")
    history_of_picks.append(picked_name)
def play_victory_sound(sound_file):
    try:
        with open(sound_file, "rb") as f:
            data = f.read()

        # 1. Turn the sound into a data string
        b64 = base64.b64encode(data).decode()

        # 2. Create a random ID so the browser thinks it's a new player
        unique_id = f"player_{time.time()}"

        # 3. Create the HTML with that unique ID
        # The 'id' tag at the end is the secret sauce!
        md = f"""
                <audio autoplay="true" id="{unique_id}">
                <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
                </audio>
                """

        # 4. Use st.components.v1.html to force it to run
        import streamlit.components.v1 as components
        components.html(md, height=0)

    except FileNotFoundError:
        st.error(f"Could not find the sound file: {sound_file}")
#logic
#--- SIDEBAR ---
st.sidebar.title("Class Setup")
uploaded_file = st.sidebar.file_uploader("Upload your student .txt file", type="txt")
if uploaded_file is not None:
    #if a file is successfully uploaded, continue
    # Load student names
    student_names = get_student_names(uploaded_file)
    st.sidebar.success(f"Loaded {len(student_names)} students!")

    # memory_file = "memory.txt"
    #create session state so history is saved for the session
    #use file name as key so different files of students by the same teacher have different memory
    if(uploaded_file.name not in st.session_state):
        st.session_state[uploaded_file.name] = []
    # --- THE BUTTON ---
    if st.button('Pick a Student'):
        # Load memory of who has already been picked
        # history_of_picks = get_picking_history(memory_file)
        # get history from session
        history_of_picks = st.session_state[uploaded_file.name]
        # Reset if everyone was picked
        history_of_picks = reset_memory(student_names, history_of_picks, uploaded_file.name)
        # Set Weights
        student_weights = set_weights(student_names, history_of_picks)

        # Pick Winner
        picked_student = random.choices(student_names, weights=student_weights, k=1)[0]
        # Save to Memory
        add_student_to_history(history_of_picks, picked_student)

        # Show the result on the screen BIG
        st.header(f"✨ {picked_student} ✨")
        # 2. Sound: Play the "Level Up" noise!
        play_victory_sound("win_sound.mp3")
        # 4. Success: Show the name and balloons
        # st.success(f"## 🏆 {picked_student} 🏆")
        st.balloons()
        # 3. Suspense: A tiny pause for the music to start
        with st.spinner("Drumroll..."):
            time.sleep(1.2)


        # --- DEBUG SECTION ---
        # with st.sidebar.expander("🛠️ Admin: Check Memory"):
        #     st.write("Current Session Locker Name:", uploaded_file.name)
        #     st.write("Students already picked:", st.session_state[uploaded_file.name])
else:
    # If no file is uploaded yet, show a friendly message
    st.info("Please upload a .txt file in the sidebar to begin!")

