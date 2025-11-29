import gradio as gr
from app import bot_response
from voice import speech_to_text,text_to_speech 

def main(audio):
        if audio is None:
                return "Please provide an audio input.", None
        try:
                print(f"Processing audio: {audio}")
                text=speech_to_text(audio)
                print(f"Transcribed text: {text}")
                reply=bot_response(text)
                print(f"Bot reply: {reply}")
                out_audio=text_to_speech(reply)
                print(f"Generated audio file: {out_audio}")
                return reply, out_audio
        except Exception as e:
                error_msg = f"Error: {str(e)}"
                print(f"Error in main: {error_msg}")
                return error_msg, None 

ui=gr.Interface(
        fn=main,
        inputs=gr.Audio(sources=["microphone"],type="filepath"),
        outputs=[gr.Textbox(),gr.Audio()]
)

ui.launch()