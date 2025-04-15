import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/swati/Motion_Planning/MP_for_AV/src/MP_for_AV/install/vd_config'
