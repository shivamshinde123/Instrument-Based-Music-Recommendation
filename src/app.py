import streamlit as st
import os
import tempfile
import logging
from step0_utility_functions import Utility
from step3_calculate_similarity_scores import generate_recommendations


def webapp():
    # # Streamlit UI Part

    st.set_page_config(
            page_title = "Music Recommendation App",
            page_icon="🎹",
            initial_sidebar_state="expanded",
            # layout='wide'
        )
    
    st.markdown("""
    <style>
        /* Ensure the full width usage for the overall container */
        .reportview-container {
            max-width: 100% !important;
        }

        /* Center the content container and set it to 60% width */
        .block-container {
            max-width: 60%;    /* Set the content width to 60% of the screen */
            margin: 0 auto;    /* Center the container horizontally */
            padding-left: 20px !important;
            padding-right: 20px !important;
        }

        /* Apply full width to main content section */
        .main {
            max-width: 100% !important;
        }

        /* Center all headers (h1, h2, etc.) */
        h1, h2, h3, h4, h5, h6 {
            text-align: center;
        }

        /* Center all text content */
        .stMarkdown, .stText {
            text-align: center;
        }
    </style>
    """, unsafe_allow_html=True)

    st.title("Instrument-Based Music Recommendation 🎹")

    st.caption('A project by Shivam Shinde, Prasham Soni, and Manav Mepani')

    st.image('Header_Image.jpg')

    st.divider()

    st.subheader('Upload a song file')
    uploaded_file = st.file_uploader("", type=["wav"])

    if uploaded_file:
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as temp_file:
            temp_file.write(uploaded_file.getbuffer())
            temp_file_path = temp_file.name
            
        if not os.path.exists('user_ip_wavfile_folder'):
            os.makedirs('user_ip_wavfile_folder')
            
        file_path = os.path.join('user_ip_wavfile_folder', 'wavfile.wav')
        
        with open(file_path, 'wb') as f:
            f.write(uploaded_file.getbuffer())
        
        st.audio(temp_file_path)

        st.subheader("Tell us your instrument preferences:")
        guitar_pref = st.radio("Do you prefer Guitar:guitar: in recommendations?", ["No", "Yes"])
        drums_pref = st.radio("Do you prefer Drums:drum_with_drumsticks: in recommendations?", ["No", "Yes"])
        piano_pref = st.radio("Do you prefer Piano:musical_keyboard: in recommendations?", ["No", "Yes"])
        bass_pref = st.radio("Do you prefer Bass:notes: in recommendations?", ["No", "Yes"])
        others_pref = st.radio("Do you prefer other:musical_score: instruments in recommendations?", ["No", "Yes"])

        preferences = [
            1 if guitar_pref == "Yes" else 0,
            1 if drums_pref == "Yes" else 0,
            1 if piano_pref == "Yes" else 0,
            1 if bass_pref == "Yes" else 0,
            1 if others_pref == "Yes" else 0,
        ]    
        

        if st.button("Submit"):
            with st.spinner():
                recommendations = generate_recommendations()
                print(f"******************Recommendations: {recommendations}")
                if recommendations:
                    st.success("Preferences submitted successfully! Here is your recommendation:")
                    # for rec in recommendations:
                    #     st.write(f"- {rec}")
                    st.audio(os.path.join('Database', 'Input', f"{recommendations}"))
                else:
                    st.warning("No recommendations available based on your preferences. Try adjusting your inputs.")

        try:
            os.remove(temp_file_path)
        except Exception as e:
            st.error(f"Error cleaning up the file: {e}")
    else:
        st.info("Please upload a song to proceed.")
    
    
if __name__ == "__main__":

    os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

    # SETTING UP THE LOGGING MECHANISM
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    Utility().create_folder('Logs')
    params = Utility().read_params()

    main_log_folderpath = params['Logs']['Logs_Folder']
    frontend = params['Logs']['Frontend']

    file_handler = logging.FileHandler(os.path.join(
        main_log_folderpath, frontend))
    formatter = logging.Formatter(
        '%(asctime)s : %(levelname)s : %(filename)s : %(message)s')

    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    # STARTING THE EXECUTION OF FUNCTIONS
    logger.info('Webapp launched successfully.')

    webapp()

    logger.info('Webapp Disconnected.')

