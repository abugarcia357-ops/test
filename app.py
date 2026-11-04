# app.py
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def main():
    # (a) Create a Streamlit interface for the Student Marks Analysis System
    st.title("Course: Python Programming")
    st.write("Enter data for THREE (3) students only.")
    
    names = []
    genders = []
    marks_list = []
    
    # Input collection form for THREE students
    for i in range(1, 4):
        st.subheader(f"Student {i}")
        # Text input for Student Name
        name = st.text_input(f"Enter Student Name {i}", key=f"name_{i}")
        # Radio button for Gender
        gender = st.radio(f"Select Gender {i}", ["Male", "Female"], key=f"gender_{i}")
        # Number input for Marks (range 0-100)
        marks = st.number_input(f"Enter Marks {i}", min_value=0.0, max_value=100.0, step=1.0, key=f"marks_{i}")
        
        names.append(name)
        genders.append(gender)
        marks_list.append(marks)
        
    # Button labelled "Submit"
    submit_button = st.button("Submit")
    
    if submit_button:
        # (b) Apply exception handling using try-except to validate inputs
        try:
            # Check if any student name is empty
            for name in names:
                if not name.strip():
                    raise ValueError("Error: Student name cannot be empty! Please fill in all names.")
            
            # Ensure we have exactly 3 sets of data
            if len(names) != 3 or len(marks_list) != 3:
                raise ValueError("Error: Data must be provided for exactly THREE (3) students.")

            st.success("Data successfully validated and processed!")
            
            # (c) Store marks in a NumPy array and analyze
            marks_array = np.array(marks_list)
            mean_marks = np.mean(marks_array)
            max_marks = np.max(marks_array)
            
            st.markdown("### Analysis")
            st.write(f"*Mean Marks:* {mean_marks:.2f}")
            st.write(f"*Maximum Marks:* {max_marks}")
            
            # (e) Data Processing: Result classification (Pass if >= 50, Fail if < 50)
            results = ["Pass" if m >= 50 else "Fail" for m in marks_list]
            
            # (d) Create a Pandas DataFrame
            df = pd.DataFrame({
                "Student Name": names,
                "Gender": genders,
                "Course": ["Python Programming"] * 3,
                "Marks": marks_list,
                "Result": results
            })
            
            # (e) Sorting marks in ascending order for display
            df_sorted = df.sort_values(by="Marks", ascending=True)
            
            st.markdown("### Sorted Student Records")
            st.dataframe(df_sorted)
            
            # (e) Display a graph to visualize student marks
            st.markdown("### Marks Graph")
            fig, ax = plt.subplots(figsize=(8, 4))
            ax.bar(df_sorted["Student Name"], df_sorted["Marks"], color=['skyblue' if r=='Pass' else 'salmon' for r in df_sorted["Result"]])
            ax.set_xlabel("Student Name")
            ax.set_ylabel("Marks")
            ax.set_title("Student Marks Visualization")
            ax.set_ylim(0, 100)
            
            # Render plot in Streamlit
            st.pyplot(fig)
            
        except ValueError as e:
            # Display appropriate error message as required by rubric
            st.error(str.format(str(e)))
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")

if _name_ == "_main_":
    main()