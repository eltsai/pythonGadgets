#!/usr/bin/env python3

from Crypto.Util.number import bytes_to_long

flag = bytes_to_long(open("flag").read().encode())



n1 = 19923456590552251975162382016814931637382722375359317208772451871483356576714885405606097241378501075931369906670869061248093649172881861192415328175663097814656963736628313898192077466201058425384752569296996738377762539233037404643814812839894268154220478743035005438051770194437690753198077282440197305242179520050148380897574370600817779326137623367669108915782523407192924244211054831306140325178040945340487553314593944938986145125036773442922867233469484732742374036099352126374556352618891702660032199891902387345141014680832744060658322845566908945809269331920931166181902583367526789454630626729460870647169
n2 = 23652833904119539867170294668574519424764451584703709844692900487740199502027597219325105779509757750797225761350201692963410434498426449300686946983803002021489077408094793455555430544612634765894489927184427882039278621190257263451767512691221747983840404059919424585305403183478687231730821351928952948387786999318351680488492230221474263072462047902669589861650172415714744833823410983928596263345045594725340746629428670770352781564040112067286818358284699547765286831757865286706603307438315831970396001029588630072110064604209495792029805266048287992268106514474824700175027996395298427269399103991524141700041
e = 65537
print(pow(flag, e, n1))
print(pow(flag, e, n2))