from BU.futures.api import adminapi
from common import slacksend
import time
tradeTyp='linearPerpetual'
def liquidation():
    try:
        a=adminapi.admin_memory_query_position(tradeTyp=tradeTyp)
        tt=['该uid有问题，保证率大于1，但是没爆仓掉：']
        for tmp in  a['data']['list']:
            if tmp['marginRate']>1:
                tt.append(tmp)
            #print(tmp)
        #print(tt)
        slacksend.send_Slack(tt)
    except Exception as e:
        print(e)
if __name__ == '__main__':
    for i in  range(1000):
        time.sleep(60 * 60)
        liquidation()