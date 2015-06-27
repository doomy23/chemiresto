# -*- coding: utf-8 -*-

#
#    Made by Dominic Roberge
#    Dont forget to update this dict and it's rates!
#
#    General rules :
#        - Out of Canada is free of taxes
#        - TVH replace TPS and any provincial taxes
#        - TVP and TVQ are provincial taxes
#

from decimal import Decimal

TPS = Decimal('0.05')
TVQ = Decimal('0.09975')

BC_TVP = Decimal('0.07')
MB_TVP = Decimal('0.08')
SK_TVP = Decimal('0.05')

ON_TVH = Decimal('0.13')
NB_TVH = Decimal('0.13')
NS_TVH = Decimal('0.15')
NL_TVH = Decimal('0.13')
PE_TVH = Decimal('0.14')

TAXES = {
    'CA':{
        'AB':[
            {
                'tax': 'TPS',
                'rate': TPS
            },    
        ],
        'BC':[
            {
                'tax': 'TPS',
                'rate': TPS
            },    
            {
                'tax': 'TVP',
                'rate': BC_TVP
            },      
        ],
        'MB':[
            {
                'tax': 'TPS',
                'rate': TPS
            },     
            {
                'tax': 'TVP',
                'rate': MB_TVP
            },     
        ],
        'NB':[
            {
                'tax': 'TVH',
                'rate': NB_TVH
            },   
        ],
        'NL':[
            {
                'tax': 'TVH',
                'rate': NL_TVH
            }, 
        ],
        'NT':[
            {
                'tax': 'TPS',
                'rate': TPS
            },     
        ],
        'NS':[
            {
                'tax': 'TVH',
                'rate': NS_TVH
            },        
        ],
        'NU':[
            {
                'tax': 'TPS',
                'rate': TPS
            },   
        ],
        'ON':[
            {
                'tax': 'TVH',
                'rate': ON_TVH
            }, 
        ],
        'PE':[
            {
                'tax': 'TVH',
                'rate': PE_TVH
            },       
        ],
        'QC':[
            {
                'tax': 'TPS',
                'rate': TPS
            },
            {
                'tax': 'TVQ',
                'rate': TVQ
            },
        ],
        'SK':[
            {
                'tax': 'TPS',
                'rate': TPS
            },   
            {
                'tax': 'TVP',
                'rate': SK_TVP
            },   
        ],
        'YT':[
            {
                'tax': 'TPS',
                'rate': TPS
            },   
        ],
    },
}