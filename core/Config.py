hosts = ['edu.cn']
methods = ['post', 'get']
accepts = ['json']
post_content_type = ['application/x-www-form-urlencoded', 'application/json', 'multipart/form-data']
response_type = ['json']
params = {
    'common': ['.*user.*', '.*year.*', '.*page.*', '.*page.*', '.*size.*'],
    'sensitive': [
        '.*acc.*',
        '.*birth.*',
        '.*card.*', '.*college.*',
        '.*date.*',
        '.*email.*', '.*edu.*',
        '.*gen.*',
        '.*id.*',
        '.*list.*',
        '.*major.*', '.*mail.*', '.*more.*',
        '.*name.*',
        '.*person.*', '.*phone.*', '.*pro.*', '.*pos.*',
        '.*sex.*', '.*status.*', '.*school.*',
        '.*table.*', '.*type.*', '.*tel.*',
        '.*user.*', '.*uid.*',
        '.*where.*', '.*work.*',
        '.*year.*'
    ]
}
intStep = 10

privacy_tpl = [
    # personalIdentity
    '.*name.*', '.*ry.*', '.*xm.*', '.*mc.*',
    '.*gender.*', '.*sex.*', '.*xingbie.*', '.*xb.*',
    '.*birth.*', '.*shengri.*', '.*age.*', '.*sr.*', '.*year.*',
    '.*nation.*', '.*guoji.*', '.*gj.*',
    '.*id.*', '.*shenfenzheng.*', '.*sfz.*', '.*zj.*',
    '.*pass.*', '.*huzhao.*', '.*hz.*',
    '.*driver.*', '.*jiazhao.*', '.*jz.*',
    '.*social.*', '.*shebao.*', '.*sb.*', '.*family.*', '.*friend.*',
    '.*place.*', '.*addr.*', '.*loc.*', '.*post.*', '.*dizhi.*', '.*dz.*',
    '.*mar.*', '.*hunyin.*', '.*hy.*',
    '.*religious.*', '.*zongjiao.*', '.*zj.*',
    '.*mac.*', '.*ip.*', '.*gps.*', '.*latitude.*', '.*lat.*', '.*longitude.*', '.*lng.*',
    '.*acc.*', '.*user.*', '.*uid.*', '.*role.*', '.*avatar.*', '.*file.*', '.*photo.*', '.*pic.*', '.*img.*',
    '.*school.*', '.*college.*', '.*institute.*', '.*university.*', '.*dept.*', '.*bm.*',
    '.*edu.*', '.*pos.*', '.*tit.*',
    '.*employ.*', '.*job.*', '.*company.*', '.*salary.*',
    '.*official_rank.*', '.*zhiwu.*', '.*zw.*',  
    '.*title.*', '.*zhicheng.*', '.*zc.*',  
    '.*exam_monitor.*', '.*jiankao.*', '.*jk.*', 
    '.*campus_card.*', '.*xiaoyikatong.*', '.*yky.*',  
    '.*iris.*', '.*hongmo.*', '.*hm.*',  
    '.*palm.*', '.*zhangwen.*', '.*zw.*', 
    '.*voiceprint.*', '.*shengwen.*', 
    '.*student_id.*', '.*xuehao.*', '.*xh.*', 
    '.*admission.*', '.*ruxue.*', '.*rx.*', 
    '.*transcript.*', '.*chengji.*', '.*cj.*',  
    '.*scholarship.*', '.*jiangxuejin.*', '.*jxj.*', 
    '.*disciplinary.*', '.*chufen.*', '.*cf.*', 
    '.*academic.*', '.*xueshu.*', '.*xs.*',  
    '.*tuition.*', '.*xuefei.*', '.*xf.*',  
    '.*dorm.*', '.*sushe.*', '.*ss.*',  
    '.*mentor.*', '.*daoshi.*', '.*ds.*', 
    '.*enrollment.*', '.*zhaosheng.*', '.*zs.*', 
    '.*huji.*', '.*hj.*', '.*household.*', 
    '.*approval.*', '.*sp.*', '.*shenpi.*',  
    '.*public_safety.*', '.*gongan.*', '.*ga.*',  
    '.*tax.*', '.*shuiwu.*', '.*sw.*',  
    '.*pension.*', '.*yanglao.*', '.*yl.*', 
    '.*housing_fund.*', '.*gjj.*', 
    '.*subsidy.*', '.*butie.*', '.*bt.*', 
    '.*military.*', '.*junshi.*', '.*js.*', 
    '.*political.*', '.*zhengzhi.*', '.*zz.*', 
    '.*complaint.*', '.*jubao.*', '.*jb.*',  
    '.*archive.*', '.*dangan.*', '.*da.*', 
    # contact
    '.*tel.*', '.*mob.*', '.*phone.*', '.*shouji.*', '.*sj.*', '.*dianhua.*', '.*dh.*',
    '.*email.*', '.*mail.*', '.*youxiang.*', '.*yx.*', '.*youjian.*', '.*yj.*', '.*yx.*',
    '.*qq.*', '.*wechat.*', '.*weixin.*', '.*wx.*', '.*weibo.*', '.*wb.*',
    '.*twitter.*', '.*facebook.*', '.*fb.*', '.*instagram.*', '.*ins.*', '.*youtube.*',
    # financial
    '.*account.*', '.*bank.*', '.*card.*',
    '.*pay.*', '.*alipay.*', '.*wepay.*', '.*zhifubao.*',
    '.*asset.*', '.*property.*', '.*zichan.*', '.*baoxian.*',
    # financial
    '.*government_allowance.*', '.*zhengfubutie.*', '.*zfbt.*',  
    '.*special_fund.*', '.*zhuanxiangzijin.*', '.*zxzj.*',  
    # confidentialFiles
    '.*internal_doc.*', '.*neibu.*',  
    '.*classified.*', '.*jimi.*', 
    '.*sensitive_report.*', '.*baogao.*',  
    '.*audit.*', '.*shenji.*', 
    # health
    '.*medical.*',
    '.*prescription.*',
    '.*disease.*',
    '.*health.*',
    '.*genetic.*',
    '.*bio.*', '.*fin.*', '.*fac.*',
    '.*fit.*', '.*weight.*', '.*height.*',

]

privacy_lib = {
    'personalIdentity': {
        'name': ['.*name.*', '.*ry.*', '.*xm.*', '.*mc.*'],
        'gender': ['.*gender.*', '.*sex.*', '.*xingbie.*', '.*xb.*'],
        'birth': ['.*birth.*', '.*shengri.*', '.*age.*', '.*sr.*', '.*year.*'],
        'nationality': ['.*nation.*', '.*guoji.*', '.*gj.*'],
        'idCard': ['.*id.*', '.*shenfenzheng.*', '.*sfz.*', '.*zj.*'],
        'passport': ['.*pass.*', '.*huzhao.*', '.*hz.*'],
        'driverLicense': ['.*driver.*', '.*jiazhao.*', '.*jz.*'],
        'social': ['.*social.*', '.*shebao.*', '.*sb.*', '.*family.*', '.*friend.*'],
        'place': ['.*place.*', '.*addr.*', '.*loc.*', '.*post.*', '.*dizhi.*', '.*dz.*'],
        'maritalStatus': ['.*mar.*', '.*hunyin.*', '.*hy.*'],
        'religiousBeliefs': ['.*religious.*', '.*zongjiao.*', '.*zj.*'],
        'networkAddress': ['.*mac.*', '.*ip.*', '.*gps.*', '.*latitude.*', '.*lat.*', '.*longitude.*', '.*lng.*'],
        'account': ['.*acc.*', '.*user.*', '.*uid.*', '.*role.*', '.*avatar.*', '.*file.*', '.*photo.*', '.*pic.*', '.*img.*'],
        'school': ['.*school.*', '.*college.*', '.*institute.*', '.*university.*', '.*dept.*', '.*bm.*'],
        'educational': ['.*edu.*', '.*pos.*', '.*tit.*'],
        'employment': ['.*employ.*', '.*job.*', '.*company.*', '.*salary.*']
    },
    'contact': {
        'phone': ['.*tel.*', '.*mob.*', '.*phone.*', '.*shouji.*', '.*sj.*', '.*dianhua.*', '.*dh.*'],
        'email': ['.*email.*', '.*mail.*', '.*youxiang.*', '.*yx.*', '.*youjian.*', '.*yj.*', '.*yx.*'],
        'socialMediaAccounts': ['.*qq.*', '.*wechat.*', '.*weixin.*', '.*wx.*', '.*weibo.*', '.*wb.*',
                                '.*twitter.*', '.*facebook.*', '.*fb.*', '.*instagram.*', '.*ins.*', '.*youtube.*']
    },
    'financial': {
        'bank': ['.*account.*', '.*bank.*', '.*card.*'],
        'pay': ['.*pay.*', '.*alipay.*', '.*wepay.*', '.*zhifubao.*'],
        'asset': ['.*asset.*', '.*property.*', '.*zichan.*', '.*baoxian.*']
    },
    'health': {
        'medical': ['.*medical.*'],
        'prescription': ['.*prescription.*'],
        'disease': ['.*disease.*'],
        'health': ['.*health.*'],
        'genetic': ['.*genetic.*'],
        'biometric': ['.*bio.*', '.*fin.*', '.*fac.*'],
        'fitness': ['.*fit.*', '.*weight.*', '.*height.*']
    }
}
