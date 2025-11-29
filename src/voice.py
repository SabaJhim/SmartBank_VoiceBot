#Add voice to BOT
import os
from dotenv import load_dotenv
import speech_recognition as sr
from pydub import AudioSegment
import tempfile
load_dotenv()

def speech_to_text(audio_file):
        wav_file_path = None
        try:
                # Convert audio to WAV format if needed (SpeechRecognition requires WAV)
                audio = AudioSegment.from_file(audio_file)
                wav_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
                wav_file_path = wav_file.name
                wav_file.close()  # Close the file handle before exporting
                
                audio.export(wav_file_path, format="wav")
                
                # Use Google Speech Recognition (free, no API key needed for basic usage)
                r = sr.Recognizer()
                with sr.AudioFile(wav_file_path) as source:
                        audio_data = r.record(source)
                transcript = r.recognize_google(audio_data)
                return transcript
                
        except sr.UnknownValueError:
                raise Exception("Could not understand the audio. Please speak more clearly.")
        except sr.RequestError as e:
                raise Exception(f"Error with speech recognition service: {str(e)}")
        except Exception as e:
                raise Exception(f"Error processing audio: {str(e)}")
        finally:
                # Clean up temp file in finally block to ensure it's deleted even on error
                if wav_file_path and os.path.exists(wav_file_path):
                        try:
                                # Wait a bit and retry if file is locked
                                import time
                                time.sleep(0.1)
                                os.unlink(wav_file_path)
                        except (OSError, PermissionError):
                                # If still locked, try to delete later (OS will clean up temp files)
                                pass

def text_to_speech(text):
        try:
                from gtts import gTTS
                import tempfile
                
                output_dir = os.path.join(os.getcwd(), "temp_audio")
                os.makedirs(output_dir, exist_ok=True)
                output = os.path.join(output_dir, "output_audio.mp3")
                
                # Use Google Text-to-Speech (free, no API key needed)
                tts = gTTS(text=text, lang='en', slow=False)
                tts.save(output)
                print(f"Audio file saved to: {output}")
                return output
        except Exception as e:
                raise Exception(f"Error generating speech: {str(e)}") 


