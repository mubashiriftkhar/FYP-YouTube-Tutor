from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from youtube_transcript_api.formatters import TextFormatter
from Backend.BaseClass import BaseClass
from Backend.state import State
from bs4 import BeautifulSoup
import requests
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
from youtube_transcript_api.formatters import TextFormatter
import re

class Trancript(BaseClass):
    def execute(self, state: State) -> State:
        link = state["link"]
        try:
            
            r = requests.get(link)
            soup = BeautifulSoup(r.text, "html.parser") 

            title_tag = soup.find("title")  
            if title_tag:
                title = title_tag.text.strip() 
            else:
                title = "Unknown Title"

            state["vedioTitle"] = title
            
            # Extract video ID
            videoID = re.search(r"(?:v=|youtu\.be/)([^&]+)", link).group(1)
            
            # List all available transcripts
            yta=YouTubeTranscriptApi()
            transcript_list = yta.list(videoID)
            
            english_transcript = None

            # Try to find any English transcript (manual or generated)
            for t in transcript_list:
                if t.language_code.lower().startswith("en"):
                    english_transcript = t
                    break

            # If no English transcript found, fallback to first available
            if not english_transcript:
                try:
                    english_transcript = list(transcript_list)[0]  # pick first available
                    # if it's translatable, translate to English
                    if english_transcript.is_translatable:
                        english_transcript = english_transcript.translate('en')
                        state["isEnglishAvailable"] = True
                    else:
                        state["isEnglishAvailable"] = False
                except Exception:
                    state["isEnglishAvailable"] = False
                    return state
            else:
                state["isEnglishAvailable"] = True

            # Fetch the transcript
            transcript_data = english_transcript.fetch()

            # Format transcript text
            formatter = TextFormatter()
            transcript_text = formatter.format_transcript(transcript_data)
            state["EnglishTranscript"] = transcript_text

            return state

        except TranscriptsDisabled:
            state["isEnglishAvailable"] = False
            return state
        except NoTranscriptFound:
            state["isEnglishAvailable"] = False
            return state
        except Exception as e:
            print(f"Error fetching transcript: {e}")
            state["isEnglishAvailable"] = False
            return state




  
# sample_state = {
#         "link":"https://youtu.be/62wEk02YKs0",
#         "query": "What this Video is Explaining?",
#         "vedioTitle": "",
#         "TitledQuery":"",
#         "isEnglishAvailable": False,
#         "EnglishTranscript": "",
# }
# transcript=Trancript()
# print(transcript.execute(state=sample_state))



