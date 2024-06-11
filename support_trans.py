import json
import os
import urllib.request
from random import randint


class SupportTrans:
    @classmethod
    def translate(cls, text, source='ja', target='ko', api_type=None):
        if api_type == None:
            from .setup import P
            api_type = P.ModelSetting.get('base_trans_type')
        func = cls.get_func(api_type)
        return func(text, source=source, target=target)

    @classmethod
    def get_func(cls, api_type):
        if api_type == 'google_api':
            return cls.trans_google_api
        elif api_type == 'google_web2':
            return cls.trans_google_web2
        elif api_type == 'deepl_api':
            return cls.trans_deepl_api

    @classmethod
    def trans_google_api(cls, text, source='ja', target='ko', google_apikey=None):
        if google_apikey == None:
            from .setup import P
            google_apikey = P.ModelSetting.get('base_trans_google_apikey')
        if google_apikey == '' or google_apikey is None:
            return text
        data = "key=%s&source=%s&target=%s&q=%s" % (google_apikey, source, target, text)
        url = "https://www.googleapis.com/language/translate/v2"
        requesturl = urllib.request.Request(url)
        requesturl.add_header("X-HTTP-Method-Override", "GET")

        response = urllib.request.urlopen(requesturl, data = data.encode("utf-8"))
        data = json.load(response)
        rescode = response.getcode()
        if rescode == 200:
            return data['data']['translations'][0]['translatedText']
        else:
            return text


    @classmethod
    def trans_google_web2(cls, text, source='ja', target='ko'):
        try:
            import requests
            url = 'https://translate.google.com/translate_a/single'
            headers = {'User-Agent': 'GoogleTranslate/6.27.0.08.415126308 (Linux; U; Android 7.1.2; PIXEL 2 XL)'}
            params = {'q': text, 'sl': source, 'tl': target,
                    'hl': 'ko-KR', 'ie': 'UTF-8', 'oe': 'UTF-8', 'client': 'at',
                    'dt': ('t', 'ld', 'qca', 'rm', 'bd', 'md', 'ss', 'ex', 'sos')}
            
            response = requests.get(url, params=params, headers=headers).json()
            translated_text = ''
            for sentence in response[0][:-1]:
                translated_text += sentence[0].strip() + ' '
            return translated_text
        except Exception as e: 
            return text



    @classmethod
    def trans_deepl_api(cls, text, source='ja', target='ko'):
        try:
            import deepl
        except:
            os.system("pip install deepl")
        try:
            import deepl

            from .setup import P
            deepl_apikeys = P.ModelSetting.get_list('base_trans_deepl_apikey')
            if len(deepl_apikeys) == 0:
                return text
            translator = deepl.Translator(deepl_apikeys[randint(0, len(deepl_apikeys)-1)])

            result = translator.translate_text(text, target_lang=target)
            return result.text

        except Exception as e: 
            return text