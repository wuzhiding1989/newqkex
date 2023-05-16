import BU.NTS.dataCheck.dataCheck as dataCheck
from common.util import countCaseNumber as u,printl,Count,t as _t
import common.util as ut
def UserFrozenMarginDataCheckCase(NTS,log_level=None,title=''):
    r=dataCheck.frozenMaringCheck(NTS, 'BTCUSDT', log_level, title=title+'冻结保证金: 验证成功')
    if r:        u(1);printl(log_level,title+'冻结保证金: 验证成功')
    else:   u(0)
    return r

def UserPositionDataCheckCase(NTS,log_level=None,title=''):
    # if NTS.source=='web':
    r=dataCheck.PositionCalculater(NTS,log_level=log_level);u(1);printl(log_level,title+'仓位: 验证成功') if r else u(0)
    # else:
    #     r=dataCheck.openApiPositionCalculater(NTS,log_level=log_level);u(1);printl(log_level,title+'仓位: 验证成功') if r else u(0)
    return r

def UserAccountDataCheckCase(NTS,log_level=None,title=''):
    r=dataCheck.AccountCalculater(NTS,NTS.user_id,log_level=log_level,title=title);u(1);printl(log_level,title+'资金: 验证成功') if r else u(0)
    return r

def UsderDataCheckCase(NTS,log_level=None,option=None,title='',Flag=None):
    r=0;r1=0;r2=0;r3=0
    if not option or  '1' in option:    r1=UserFrozenMarginDataCheckCase(NTS,log_level,title=title);
    if not option or '2' in option:     r2=UserPositionDataCheckCase(NTS,log_level,title=title);
    if not option or '3' in option:     r3=UserAccountDataCheckCase(NTS, log_level,title=title);
    if r1:
        r = r+1;
        if  Flag and (not option or '1' in option):
            Count('挂单冻结保证金公式',1,TestResult=r1,Flag=Flag)
    if r2:
        r = r+1;
        if Flag and (not option or '2' in option) : Count('持仓接口相关公式',1,TestResult=r2,Flag=Flag)
    if r3:
        r = r+1;
        if Flag and (not option or '3' in option) : Count('资金接口相关公式',1,TestResult=r3,Flag=Flag)
    return r

if __name__ == '__main__':
    from BU.NTS.WebOrder import n_order
    NTS = n_order(6, user_id=97201973);
    printl(UsderDataCheckCase(NTS))
    print('【Case】', '总数:', ut._all, '通过:', ut._pass, '失败:', ut._all - ut._pass - ut._block, '阻塞:', ut._block,'通过率: ' + str(ut.truncate(ut._pass / ut._all * 100, 2)) + '%');