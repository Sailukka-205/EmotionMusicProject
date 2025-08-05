import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import cv2
from deepface import DeepFace
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# ---------------- Spotify Setup ---------------- #
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id="6e101187d7174df0ae6f608b80c792c3",
    client_secret="af258fdc98634027b7e0f47a28b115e7",
    redirect_uri="http://127.0.0.1:8888/callback",
    scope="user-read-playback-state,user-modify-playback-state,user-read-currently-playing"
))

# Emotion → Playlist mapping
emotion_to_playlist = {
    "happy": "31QRrcO8enAOkSXo4EHpgR",
    "sad": "189Sow1xr7R94oSKs4kISc",
    "angry": "0zG7Wuh9CkLgixpfrSFWzq",
    "surprise": "3CFtRs6NUi2CNH7gejWfVN",
    "neutral": "5IL5pllGVsViQ5gamGTE"
}

current_emotion = None

# ---------------- Camera Setup ---------------- #
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    try:
        result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
        emotion = result[0]['dominant_emotion']

        # Show emotion on video feed
        cv2.putText(frame, f'Emotion: {emotion}', (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

        # Play playlist if emotion changed
        if emotion != current_emotion and emotion in emotion_to_playlist:
            playlist_id = emotion_to_playlist[emotion]
            try:
                # Ensure there’s an active Spotify device
                devices = sp.devices()
                if not devices['devices']:
                    print("⚠️ No active Spotify device found. Start playback on Spotify manually first.")
                else:
                    sp.start_playback(context_uri=f"spotify:playlist:{playlist_id}")
                    print(f"🎵 Now playing {emotion} playlist!")
                    current_emotion = emotion
            except Exception as spotify_error:
                print("Spotify error:", spotify_error)

    except Exception as e:
        print("Emotion detection error:", e)

    cv2.imshow("Emotion Detector", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
