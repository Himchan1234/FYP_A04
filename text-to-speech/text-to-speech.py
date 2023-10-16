# import os
#
# os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.join('key', 'credentials.json')
#
# def __enter__(self):
#     self._audio_interface = pyaudio.PyAudio()
#     self._audio_stream = self._audio_interface.open(
#         format=pyaudio.paInt16,
#         channels=1,
#         rate=self._rate,
#         input=True,
#         frames_per_buffer=self._chunk,
#         stream_callback=self._fill_buffer,
#     )
#     self.closed = False
#     return self
#
# def generator(self):
#     while not self.closed:
#         chunk = self._buff.get()
#         if chunk is None:
#             return
#         data = [chunk]
#
#         while True:
#             try:
#                 chunk = self._buff.get(block=False)
#                 if chunk is None:
#                     return
#                 data.append(chunk)
#             except queue.Empty:
#                 break
#         yield b"".join(data)
#
# def listen_print_loop(responses):
#        num_chars_printed = 0
#     for response in responses:
#         if not response.results:
#             continue
#              result = response.results[0]
#         if not result.alternatives:
#             continue
#
#                transcript = result.alternatives[0].transcript
#         overwrite_chars = " " * (num_chars_printed - len(transcript))
#
#         if not result.is_final:
#             sys.stdout.write(transcript + overwrite_chars + "\r")
#             sys.stdout.flush()
#
#             num_chars_printed = len(transcript)
#
#         else:
#             print(transcript + overwrite_chars)
#             if re.search(r"\b(exit|quit)\b", transcript, re.I):
#                 print("Exiting..")
#                 break
#
#             num_chars_printed = 0
#
# def main():
#     # See http://g.co/cloud/speech/docs/languages
#     # for a list of supported languages.
#     language_code = "en-US"  # a BCP-47 language tag
#
#     client = speech.SpeechClient()
#     config = speech.RecognitionConfig(
#         encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
#         sample_rate_hertz=RATE,
#         language_code=language_code,
#     )
#
#     streaming_config = speech.StreamingRecognitionConfig(
#         config=config, interim_results=True
#     )
#
#     with MicrophoneStream(RATE, CHUNK) as stream:
#         audio_generator = stream.generator()
#         requests = (
#             speech.StreamingRecognizeRequest(audio_content=content)
#             for content in audio_generator
#         )
#
#         responses = client.streaming_recognize(streaming_config, requests)
#
#         listen_print_loop(responses)