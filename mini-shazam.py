import pyaudio
import wave
from shazamio import Shazam
import requests
from bs4 import BeautifulSoup
import asyncio


def record_audio(filename, duration=10):
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True, frames_per_buffer=CHUNK)

    frames = []

    for _ in range(0, int(RATE / CHUNK * duration)):
        data = stream.read(CHUNK)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    p.terminate()

    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))


async def identify_song(audio_file):
    shazam = Shazam()
    result = await shazam.recognize_song(audio_file)
    return result


def fetch_lyrics(song_title, artist_name):
    query = f"{song_title} {artist_name} lyrics"
    url = f"https://www.google.com/search?q={query}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.text, 'html.parser')
    snippets = soup.find_all("span")
    
    lyrics = None
    for snippet in snippets:
        if "lyrics" in snippet.text.lower():
            lyrics = snippet.text
            break

    return lyrics or "Lyrics not found."


async def main():
    audio_file = "music_sample.wav"
    record_audio(audio_file, duration=10)

    song_info = await identify_song(audio_file)

    if song_info.get("track") and song_info["track"].get("title") and song_info["track"].get("subtitle"):
        song_title = song_info["track"]["title"]
        artist_name = song_info["track"]["subtitle"]

        lyrics = fetch_lyrics(song_title, artist_name)
        print(f"Identified Song: {song_title} by {artist_name}")
        print(f"\nLyrics:\n{lyrics}")
    else:
        print("Song could not be identified.")


if __name__ == "__main__":
    asyncio.run(main())
