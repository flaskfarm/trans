from .setup import *
from .support_trans import SupportTrans
name = 'base'

class ModuleBase(PluginModuleBase):
    db_default = {
        f'{name}_db_version' : '1',
        f'{name}_trans_type' : 'google_web2',
        f'{name}_trans_google_apikey' : '',
        f'{name}_trans_papago_key' : '',
    }

    def __init__(self, P):
        super(ModuleBase, self).__init__(P, name=name)
        #P.blueprint.template_folder = os.path.dirname(__file__)
        

    def process_menu(self, page, req):
        arg = P.ModelSetting.to_dict()
        try:
            return render_template(f'{__package__}_{name}.html', arg=arg)
        except Exception as e: 
            P.logger.error(f'Exception:{str(e)}')
            P.logger.error(traceback.format_exc())
            return render_template('sample.html', title=f"{__package__}/{name}/{page}")

    def process_command(self, command, arg1, arg2, arg3, req):
        if command == 'trans_test':
            if arg1 == '':
                return arg2
            ret = {}
            try:
                text = SupportTrans.translate(arg2, api_type=arg1)
                ret['ret'] = 'success'
                ret['data'] = text
            except Exception as e: 
                P.logger.error(f'Exception:{str(e)}')
                P.logger.error(traceback.format_exc())
                ret['ret'] = 'warning'
                ret['msg'] = str(e)
            return jsonify(ret)
            
