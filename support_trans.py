import json
import urllib.request


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
        elif api_type == 'papago_api':
            return cls.trans_papago_api
        elif api_type == 'google_web':
            return cls.trans_google_web
        elif api_type == 'google_web2':
            return cls.trans_google_web2
        elif api_type == 'papapgo_web':
            return cls.trans_papago_web


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
    def trans_papago_api(cls, text, source='ja', target='ko', papago_key=None):
        if papago_key == None:
            from .setup import P
            papago_key = P.ModelSetting.get_list('base_trans_papago_key')
        if papago_key == '' or papago_key is None:
            return text
        
        try:
            for tmp in papago_key:
                try:
                    client_id, client_secret = tmp.split(',')
                    if client_id == '' or client_id is None or client_secret == '' or client_secret is None:
                        return text
                    data = "source=%s&target=%s&text=%s" % (source, target, text)
                    url = "https://openapi.naver.com/v1/papago/n2mt"
                    requesturl = urllib.request.Request(url)
                    requesturl.add_header("X-Naver-Client-Id", client_id)
                    requesturl.add_header("X-Naver-Client-Secret", client_secret)
                    response = urllib.request.urlopen(requesturl, data = data.encode("utf-8"))
                    data = json.load(response)
                    rescode = response.getcode()
                    if rescode == 200:
                        return data['message']['result']['translatedText']
                    else:
                        continue
                except Exception as e:
                    if e.code == 429: continue
                    else: break
            return text
        except Exception as e:
            P.logger.error(f'{str(e)}')
            return text

    

    @classmethod
    def trans_google_web(cls, text, source='ja', target='ko'):
        from google_trans_new_embed import google_translator
        translator = google_translator()  
        translate_text = translator.translate(text, lang_src=source, lang_tgt=target)
        return translate_text
        

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
    def trans_papago_web(cls, text, source='ja', target='ko'):
        from papagopy import Papagopy
        translator = Papagopy()
        translate_text = translator.translate(text, sourceCode=source, targetCode=target)
        return translate_text
        
