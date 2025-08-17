import requests

def test_with_audio():
    """Test your endpoint with the audio file you created"""
    
    # Make sure your Flask app is running first!
    url = "http://127.0.0.1:5000/analyze"
    
    # Use the audio file you created
    with open("test_audio.wav", "rb") as audio_file:
        files = {"audio": audio_file}
        
        print("🔄 Testing your AI pipeline...")
        print("Sending audio file...")
        
        try:
            response = requests.post(url, files=files)
            
            if response.status_code == 200:
                result = response.json()
                print("🎉 SUCCESS! Your AI is working!")
                print()
                
                #stt tester
                print("stt tester")
                print(result.get('transcript', 'N/A'))
                print()
                
                # sentiment tester
                print('sentiment tester')
                sentiment = result.get('sentiment', {})
                print(sentiment['sentiment'])
                print(sentiment['compound'])
                print(sentiment['positive'])
                print(sentiment['negative'])
                print(sentiment['neutral'])
                print()

                # response tester (in text)
                print('response tester')
                print(result.get('response', 'N/A'))
                print()

                # response tester (tts)
                print(" AI's spoken response:")
                print(result.get('audio_url', 'N/A'))
                
            else:
                print(f"❌ Error: {response.status_code}")
                print(f"Response: {response.text}")
                
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_with_audio() 