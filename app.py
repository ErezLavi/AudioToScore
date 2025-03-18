import streamlit as st
import tempfile
import shutil
from pathlib import Path
from st_audiorec import st_audiorec
from basic_pitch.inference import predict_and_save
from basic_pitch import ICASSP_2022_MODEL_PATH


out_path = Path("output")

############## Streamlit UI Audio upload ##############
st.title("🎵 Audio to Score 🎵")
st.write("Upload an audio file (WAV, MP3) or record audio and get a MIDI file for each instrument!")

# Option to either upload or record audio
st.write("**Choose an input method:**")
option = st.radio("opt", ["Upload Audio", "Record Audio"], label_visibility='hidden')

audio_path = None

if option == "Upload Audio":
    uploaded_file = st.file_uploader("Choose an audio file", type=["wav", "mp3"], label_visibility='hidden')

    if uploaded_file:
        with open(uploaded_file.name, "wb") as f:
            f.write(uploaded_file.getbuffer())
        audio_path = uploaded_file.name
        st.audio(audio_path)

else:
    # Record audio
    wav_audio_data = st_audiorec()
    if wav_audio_data:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
            tempfile_path = Path(temp_audio.name)
            temp_audio.write(wav_audio_data)
            audio_path = tempfile_path


############## MIDI Conversion ##############
if audio_path:
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_audio_path = Path(tmp_dir) / "input_audio.mp3"
        shutil.copy(audio_path, tmp_audio_path)

        # Convert to MIDI
        st.write("Processing...")
        output_dir = Path(tmp_dir) / out_path
        output_dir.mkdir(exist_ok=True)

        # Use predict_and_save to process the audio
        predict_and_save(
            audio_path_list=[tmp_audio_path],
            output_directory=output_dir,
            save_midi=True,
            sonify_midi=False,
            save_model_outputs=False,
            save_notes=True,
            model_or_model_path=ICASSP_2022_MODEL_PATH,
        )

        # Check if MIDI file was created
        midi_files = list(output_dir.glob("*.mid"))

        if midi_files:
            midi_output_path = midi_files[0]

            # Provide download link for MIDI
            with open(midi_output_path, "rb") as midi_file:
                st.download_button("Download MIDI File", midi_file, file_name=midi_output_path.name)
        else:
            st.error("MIDI conversion failed. No MIDI file found.")
            
        


