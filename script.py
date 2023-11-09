import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter


# Function to extract and format the transcript
def get_transcript(video_url):
    # Extract the video ID from the URL
    video_id = video_url.split('v=')[1]

    # Fetch the transcript
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
    except Exception as e:
        return f"An error occurred: {e}"

    # Initialize the formatter
    formatter = TextFormatter()

    # Format the transcript as text
    text_transcript = formatter.format_transcript(transcript)

    return text_transcript


# Streamlit app
def main():
    st.title('YouTube Video Transcript Generator')

    # Text input for YouTube URL
    video_url = st.text_input('Enter the YouTube video URL:', '')

    # Button to generate transcript
    if st.button('Get Transcript'):
        if video_url:
            transcript = get_transcript(video_url)
            #st.text_area('Transcript', transcript, height=300)
            st.write(transcript)

        else:
            st.error('Please enter a YouTube video URL.')


# Run the app
if __name__ == "__main__":
    main()
