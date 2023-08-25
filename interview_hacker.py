import os
import azure.cognitiveservices.speech as speechsdk
import openai
openai.api_type = "azure"
openai.api_version = "2023-03-15-preview"
openai.api_base = "## ==> Azure gpt url"
openai.api_key = "## ==> Api key"
language = "zh-CN"

def recognize_from_microphone():
    speech_config = speechsdk.SpeechConfig(subscription='## 订阅的ID', region='## 部署的地区')
    speech_config.speech_recognition_language=language

    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    print("Speak into your microphone.")
    speech_recognition_result = speech_recognizer.recognize_once_async().get()

    if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print("Recognized: {}".format(speech_recognition_result.text))
        return speech_recognition_result.text
    elif speech_recognition_result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized: {}".format(speech_recognition_result.no_match_details))
        return "ERR"
    elif speech_recognition_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_recognition_result.cancellation_details
        print("Speech Recognition canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))
            print("Did you set the speech resource key and region values?")
        return "ERR"
    
def ask(question):
  messages = [{"role":"system","content":"你现在是一个软件工程师面试辅助机器人,你会收到一些面试中面试者说的话。\n你需要做的首先是判断面试者说的话是不是向面试官重复一个计算机领域的问题。\n如果不是请忽略,输出“非计算机问题”\n如果是计算机的问题,请帮助面试者作弊,也就是根据问题给出答案."},
      {"role":"user","content":"我叫张三,毕业于北京大学,有三年工作经验,很高兴参加这一场面试"},
      {"role":"assistant","content":"非计算机问题"},
      {"role":"user","content":"我理解您的问题,你想知道C语言中Int占几个字节是吧？"},
      {"role":"assistant","content":"C语言中Int一般占4个字节"},
      {"role":"user","content":question}]
  response = openai.ChatCompletion.create(
    engine="interview",
    messages = messages,
    temperature=0.5,
    max_tokens=800,
    top_p=0.95,
    frequency_penalty=0,
    presence_penalty=0,
    stop=None)
  decoded_text = response["choices"][0]["message"]["content"]
  print("Answer",decoded_text)

while(1):
    question = recognize_from_microphone()
    ask(question)

