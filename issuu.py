import os
import hashlib
import urllib
import urllib2
import requests
import json
import sys
import upload
import ast


from werkzeug import secure_filename
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, _app_ctx_stack, make_response, send_from_directory

version = '0.7.148'

app = Flask(__name__)

issuu_key = os.environ.get('ISSUU_KEY')
issuu_secret = os.environ.get('ISSUU_SECRET')

access = 'public'
documentSortBy = 'publishDate'
documentStates = 'A'
format = 'json'
orgDocTypes = 'pdf,doc'
pageSize = 100
resultOrder = 'desc'
startIndex = 0


embeds = {
'148': {'documentId': '180212032629-e331e2e7bbbd4f668883fec189011096', 'title': 'California Style', 'description': 'March 2018', 'dataconfigId': '6936490/58303085'},
'147': {'documentId': '180116071625-d1239b93b5144c62bcbade092a7db207', 'title': 'C Weddings', 'description': 'Spring 2018', 'dataconfigId': '6936490/57407179'},
'146': {'documentId': '171119212358-def73d5175e647cbabaaa7ac47726939', 'title': 'California Style', 'description': 'Winter 2017/18', 'dataconfigId': '6936490/55527501'},
'145': {'documentId': '171022191512-f18b8e8783ea458bbf940eddd08779f2', 'title': 'California Style', 'description': 'November 2017', 'dataconfigId': '6936490/54522122'},
'144': {'documentId': '171001194232-a7d1fb5503ba4a5890ea11080783fc68', 'title': 'C for Men', 'description': 'Fall 2017', 'dataconfigId': '6936490/53865923'},
'143': {'documentId': '170910184237-4792283118104bdeaaf4fd90dff01ec9', 'title': 'California Style', 'description': 'October 2017', 'dataconfigId': '6936490/53040534'},
'142': {'documentId': '170814153546-f84bbfd7c905413dadf962207cf3b57b', 'title': 'C Home', 'description': 'Fall 2017', 'dataconfigId': '6936490/52153602'},
'141': {'documentId': '170814153315-45733919cf19401c9e866c1ffc938983', 'title': 'California Style', 'description': 'September 2017', 'dataconfigId': '6936490/52153556'},
'140': {'documentId': '170618212558-e999da217d414de78ed254b5335dcee6', 'title': 'C Weddings', 'description': 'Fall 2017', 'dataconfigId': '6936490/50288421'},
'139': {'documentId': '170522050736-3d77a2423f4a4ae9b6cbfdfdc2220910', 'title': 'California Style', 'description': 'Summer 2017', 'dataconfigId': '6936490/49141440'},
'138': {'documentId': '170416192611-f0fa089ee60c48d0a652604d5a6868ae', 'title': 'California Style', 'description': 'May 2017', 'dataconfigId': '6936490/47380061'},
'137': {'documentId': '170403023921-54f85154be8b4bb6aeabf93d530b19f5', 'title': 'C for Men', 'description': 'Spring 2017', 'dataconfigId': '6936490/46717533'},
'136': {'documentId': '170319175921-2b4f092a2eaf45ed8205cc4383e8116c', 'title': 'California Style', 'description': 'April 2017', 'dataconfigId': '6936490/46050149'},
'135': {'documentId': '170219211122-793250fe402749e7bb7c3d38dcfb3298', 'title': 'C Home', 'description': 'Spring 2017', 'dataconfigId': '6936490/44600236'},
'134': {'documentId': '170219210757-58db00d3ebe84b5cb7f3e12106c980e1', 'title': 'California Style', 'description': 'March 2017', 'dataconfigId': '6936490/44600079'},
'133': {'documentId': '161219014119-e73bec56aa6a4f4fb39803b392dc2a9a', 'title': 'C Weddings', 'description': 'Spring 2017', 'dataconfigId': '6936490/42104256'},
'132': {'documentId': '161120182459-dd13d817856a4ea79aa33c2acfa0a069', 'title': 'California Style', 'description': 'Winter 2016/17', 'dataconfigId': '6936490/40953146'},
'131': {'documentId': '161024054133-5d3670ba5b0c4d2d8034453ae9bf74ee', 'title': 'California Style', 'description': 'November 2016', 'dataconfigId': '6936490/39953618'},
'130': {'documentId': '161003071408-6d409beaef8745da9fe4fdeb756083ae', 'title': 'C for Men', 'description': 'Fall 2016', 'dataconfigId': '6936490/39305838'},
'129': {'documentId': '160919035724-251eebd5dd864781b415a4c63de696d0', 'title': 'California Style', 'description': 'October 2016', 'dataconfigId': '6936490/38911073'},
'128': {'documentId': '160815143423-b1bd9322877c4d4081825356d54d453d', 'title': 'C Home', 'description': 'Fall 2016', 'dataconfigId': '6936490/37905125'},
'127': {'documentId': '160815143216-c18b9ab79eda4388aea2f5628b75a80b', 'title': 'California Style', 'description': 'September 2016', 'dataconfigId': '6936490/37905103'},
'126': {'documentId': '160627144507-e853c9b3dd3142a6a56cfbb4d3756e23', 'title': 'C Weddings', 'description': 'Fall 2016', 'dataconfigId': '6936490/36809004'},
'125': {'documentId': '160530211658-a7a10c26687f4247bfc5e6bdb393fb49', 'title': 'California Style', 'description': 'Summer 2016', 'dataconfigId': '6936490/36083234'},
'124': {'documentId': '160425144950-850d8d839fd54d79a529ab986183e74a', 'title': 'California Style', 'description': 'May 2016', 'dataconfigId': '6936490/35154662'},
'123': {'documentId': '160404142142-123e0b1b14a1411295be9019e847749a', 'title': 'C for Men', 'description': 'Spring 2016', 'dataconfigId': '6936490/34648566'},
'122': {'documentId': '160321043602-9ac9efaa946d49a28b98b85a30823c17', 'title': 'California Style', 'description': 'April 2016', 'dataconfigId': '6936490/34305352'},
'121': {'documentId': '160212235616-d63b475119a7463f9af711f7e6deff47', 'title': 'C Home', 'description': 'Spring 2016', 'dataconfigId': '6936490/33423014'},
'120': {'documentId': '160212234540-241b658cb38d4f2ca391cc309c1d94f7', 'title': 'California Style', 'description': 'March 2016', 'dataconfigId': '6936490/33422955'},
'119': {'documentId': '151221215423-fd267d79d0c44218a224c80d26eb195a', 'title': 'C Weddings', 'description': 'Spring 2016', 'dataconfigId': '6936490/32125429'},
'118': {'documentId': '151124171950-52c2045bc2dc4256bb70e98fd20cfc2e', 'title': 'California Style', 'description': 'Winter 2015/16', 'dataconfigId': '6936490/31563451'},
'117': {'documentId': '151005164511-d85869529cad4433a5caf69ebb5db9df', 'title': 'California Style', 'description': 'November 2015', 'dataconfigId': '6936490/30956711'},
'116': {'documentId': '151005164511-16a4c7a2e7b34a2d92ccec4926237c67', 'title': 'C for Men', 'description': 'Fall 2015', 'dataconfigId': '6936490/30507842'},
'115': {'documentId': '150923064257-28d21bcbe4234551b1181c84a39f9617', 'title': 'C California Style', 'description': 'October 2015', 'dataconfigId': '6936490/30238976'},
'114': {'documentId': '150824071940-10eaa5ec1a8a4a95a891adc4b0897f1d', 'title': 'C Home', 'description': 'Fall 2015', 'dataconfigId': '6936490/14964408'},
'113': {'documentId': '150824071805-243f175dd52a4cd9bce14f5469dc3c60', 'title': 'C California Style', 'description': 'September 2015', 'dataconfigId': '6936490/14964559'},
'112': {'documentId': '150629174131-60f8d55e351b43e2ab0634c60793a024', 'title': 'C Weddings', 'description': 'Fall 2015', 'dataconfigId': '6936490/13844801'},
'111': {'documentId': '150601154552-2a723187665d43c09b5775b97866a9a7', 'title': 'C California Style', 'description': 'Summer 2015', 'dataconfigId': '6936490/13245988'},
'110': {'documentId': '150428160452-cce3a58f5f4c4d089b84e42dfd768a47', 'title': 'C California Style', 'description': 'May 2015', 'dataconfigId': '6936490/12542444'},
'109': {'documentId': '150406155116-a1af5be47ddb4ec5bd0ed420c8b65eb6', 'title': 'C for Men', 'description': 'Spring 2015', 'dataconfigId': '6936490/12194460'},
'108': {'documentId': '150323151233-23c2e2a566904b8cb73f7ee70d391f0c', 'title': 'C California Style', 'description': 'April 2015', 'dataconfigId': '6936490/11991860'},
'107': {'documentId': '150216171751-df96455502474c7d955618ae1953cecc', 'title': 'C Home', 'description': 'Spring 2015', 'dataconfigId': '6936490/11449811'},
'106': {'documentId': '150210043310-80f16062ca7e43648f6b4edddd35d390', 'title': 'C California Style', 'description': 'March 2015', 'dataconfigId': '6936490/11354619'},
'105': {'documentId': '150113031949-0a01b9b540e84a77982f2e9ac9eaba9f', 'title': 'C Weddings', 'description': 'Spring 2015', 'dataconfigId': '6936490/10912353'},
'104': {'documentId': '141118050119-fb1d565ad5a54ebebde12ce2bf729573', 'title': 'C California Style', 'description': 'Winter 2014/15', 'dataconfigId': '6936490/10192855'},
'103': {'documentId': '141020184743-9f2f466749b34e22a11acb5d4ff29ad2', 'title': 'C California Style', 'description': 'November 2014', 'dataconfigId': '6936490/9800041'},
'102': {'documentId': '141006185327-3c1e32c06cee42a9a5e45fc77fe9c7bf', 'title': 'C for Men', 'description': 'Fall 2014', 'dataconfigId': '6936490/9613868'},
'101': {'documentId': '140811165342-c6453539a33c4120a453d8be984e9366', 'title': 'C California Style', 'description': 'October 2014', 'dataconfigId': '6936490/9439387'},
'100': {'documentId': '140811165342-c6453539a33c4120a453d8be984e9366', 'title': 'C California Style', 'description': 'September 2014', 'dataconfigId': '6936490/8904435'},
'99': {'documentId': '140819232801-7f9afae2a7174f5b84294a43842e61f0', 'title': 'C Home', 'description': 'Fall 2014', 'dataconfigId': '6936490/8993184'},
'98': {'documentId': '140703000353-80e9518973374d598f7d0749f9800d3a', 'title': 'C Weddings', 'description': 'Fall 2014', 'dataconfigId': '6936490/8610198'},
'97': {'documentId': '140703000254-8cf2cfa30eed4f78a55ff6c33d82e5f2', 'title': 'C Home', 'description': 'Summer 2014', 'dataconfigId': '6936490/8634014'},
'96': {'documentId': '140703000151-4ec11995193f41a0aebf9cd669dd6d7b', 'title': 'C California Style', 'description': 'Summer 2014', 'dataconfigId': '6936490/8634087'},
'95': {'documentId': '140703000050-3456ada982694ab0928ecd2fca533f57', 'title': 'C California Style', 'description': 'May 2014', 'dataconfigId': '6936490/8634136'},
'94': {'documentId': '140702235955-242d241f524f4740a842d4106ec98022', 'title': 'C for Men', 'description': 'Spring 2014', 'dataconfigId': '6936490/8634149'},
'93': {'documentId': '140702235903-0fa072b7c52b41118d570a79aa42f477', 'title': 'C California Style', 'description': 'April 2014', 'dataconfigId': '6936490/8634159'},
'92': {'documentId': '140702235742-56b6cc80481042adadc582659a255219', 'title': 'C Home', 'description': 'Spring 2014', 'dataconfigId': '6936490/8634177'},
'91': {'documentId': '140702235640-cc97d7371fd141809064868d8753ebb8', 'title': 'C California Style', 'description': 'March 2014', 'dataconfigId': '6936490/8634194'},
'90': {'documentId': '140702235531-7ae58c8ee1e84bbf9d6485cd0f3e2a4c', 'title': 'C Weddings', 'description': 'Spring 2014', 'dataconfigId': '6936490/8634196'},
'89': {'documentId': '140702225753-ee2087e9ac60465babc876065483da86', 'title': 'C California Style', 'description': 'Winter 2013/14', 'dataconfigId': '6936490/8483116'},
'88': {'documentId': '140702225639-a4688fd0f7c442dfa7b952759d8d76d6', 'title': 'C California Style', 'description': 'November 2013', 'dataconfigId': '6936490/8635302'},
'87': {'documentId': '140702225357-f9fc3a14692d46b1993ba4dde6c824de', 'title': 'C for Men', 'description': 'Fall 2013', 'dataconfigId': '6936490/8635310'},
'86': {'documentId': '140702225248-01a652ebba3148deaa99ed1d66c6c713', 'title': 'C California Style', 'description': 'October 2013', 'dataconfigId': '6936490/8635317'},
'85': {'documentId': '140702225136-ed4358af1f714b52858e76fbff574393', 'title': 'C California Style', 'description': 'September 2013', 'dataconfigId': '6936490/8635354'},
'84': {'documentId': '140702224947-e52bb6675a584d2f92033926ed6621cc', 'title': 'C Weddings', 'description': 'Fall 2013', 'dataconfigId': '6936490/8635362'},
'83': {'documentId': '140702224719-f30cc9a95b414b5d83ca89753f7918f1', 'title': 'C California Style', 'description': 'Summer 2013', 'dataconfigId': '6936490/8635368'},
'82': {'documentId': '140702224447-a84a2dd382464daa833d8ad91b427ac3', 'title': 'C California Style', 'description': 'May 2013', 'dataconfigId': '6936490/8635376'},
'81': {'documentId': '140702224351-a64117b506e6454392872e753fe9ca19', 'title': 'C for Men', 'description': 'Spring 2013', 'dataconfigId': '6936490/8635380'},
'80': {'documentId': '140702224218-a44d22940a764f73bec7eff39b5a58b2', 'title': 'C California Style', 'description': 'April 2013', 'dataconfigId': '6936490/8635386'},
'79': {'documentId': '140702224043-90b97d3e54e242f9aa3d75e202610ff0', 'title': 'C California Style', 'description': 'March 2013', 'dataconfigId': '6936490/8635393'},
'78': {'documentId': '140702223835-c9a6de820b6947b0b12cda86bd4ffdee', 'title': 'C Weddings', 'description': 'Spring 2013', 'dataconfigId': '6936490/8635403'},
'77': {'documentId': '140702222648-b097fed003654b18a3a2ad1d51766f9b', 'title': 'C California Style', 'description': 'December 2012', 'dataconfigId': '6936490/8635421'},
'76': {'documentId': '140702222435-3e6eeafa2e6241c6be2c2856abdca4ec', 'title': 'C California Style', 'description': 'November 2012', 'dataconfigId': '6936490/8635432'},
'75': {'documentId': '140702222257-2391de9163a247f296adf4faf04560b2', 'title': 'C for Men', 'description': 'Fall 2012', 'dataconfigId': '6936490/8635441'},
'74': {'documentId': '140702222056-798c60a839b1433e9cfc32fbaa8a79bb', 'title': 'C California Style', 'description': 'October 2012', 'dataconfigId': '6936490/8635446'},
'73': {'documentId': '140702221732-b02b36fb61cd42a59ae8670afdae29a2', 'title': 'C California Style', 'description': 'September 2012', 'dataconfigId': '6936490/8635448'},
'72': {'documentId': '140702221508-d3fb6c77d03a43d791fadb1ed8da1b68', 'title': 'C Weddings', 'description': 'Fall 2012', 'dataconfigId': '6936490/8635455'},
'71': {'documentId': '140702221336-e5fdc04cb56141819346c85dc1de1713', 'title': 'C California Style', 'description': 'Summer 2012', 'dataconfigId': '6936490/8635465'},
'70': {'documentId': '140702221217-4dabbdc3e50548f3ad78c7ca31977b05', 'title': 'C California Style', 'description': 'May 2012', 'dataconfigId': '6936490/8635468'},
'69': {'documentId': '140702221040-f0c5e4571724451b9274f55b6465e666', 'title': 'C for Men', 'description': 'Spring 2012', 'dataconfigId': '6936490/8635475'},
'68': {'documentId': '140702220749-e56d36331b9f436690c2cafd54a15c97', 'title': 'C California Style', 'description': 'April 2012', 'dataconfigId': '6936490/8635480'},
'67': {'documentId': '140702220622-32bac1432132431aa69e1ad150af508a', 'title': 'C California Style', 'description': 'March 2012', 'dataconfigId': '6936490/8635485'},
'66': {'documentId': '140702220359-a8ace0299e6e4510a5d0ece50d07fc1d', 'title': 'C Weddings', 'description': 'Spring 2012', 'dataconfigId': '6936490/8635492'},
'65': {'documentId': '140627175153-23523b5ef8394edd84c81a577fcddc41', 'title': 'C California Style', 'description': 'December 2011', 'dataconfigId': '6936490/8635498'},
'64': {'documentId': '140627175025-e663a75de4064ef8832e86a3f50d14c1', 'title': 'C California Style', 'description': 'November 2011', 'dataconfigId': '6936490/8635506'},
'63': {'documentId': '140627174459-18004f976ac34c7abb1a5eec534f0df2', 'title': 'C for Men', 'description': 'Fall 2011', 'dataconfigId': '6936490/8635514'},
'62': {'documentId': '140627174702-6ef92b44c60648308da2e09aff06276b', 'title': 'C California Style', 'description': 'October 2011', 'dataconfigId': '6936490/8635517'},
'61': {'documentId': '140627174910-9dc705620b7e45999f7061845abb2f2a', 'title': 'C California Style', 'description': 'September 2011', 'dataconfigId': '6936490/8635524'},
'60': {'documentId': '140627175303-b55f5ccc20724932bfd701a4ab8a78e7', 'title': 'C Weddings', 'description': 'Fall 2011', 'dataconfigId': '6936490/8635534'},
'59': {'documentId': '140627172828-9b1849e5fe1e4b76b0a4c0be6ebd7343', 'title': 'C California Style', 'description': 'Summer 2011', 'dataconfigId': ''},
'58': {'documentId': '140627172737-d803da410e7d4904994810d8c115b2c3', 'title': 'C California Style', 'description': 'May 2011', 'dataconfigId': ''},
'57': {'documentId': '140627174331-297352b41a4f4955b6bcf855cc720a6d', 'title': 'C for Men', 'description': 'Spring 2011', 'dataconfigId': '6936490/8659508'},
'56': {'documentId': '140627172603-2cca041b261648d2a02ef60ca49a59c5', 'title': 'C California Style', 'description': 'April 2011', 'dataconfigId': ''},
'55': {'documentId': '140627172452-cb8f3d7005e049c6804914d9dc786719', 'title': 'C California Style', 'description': 'March 2011', 'dataconfigId': ''},
'54': {'documentId': '140627172413-b7e3c0537ceb4fe690533f2a2c32de8e', 'title': 'C Weddings', 'description': 'Spring 2011', 'dataconfigId': ''},
'53': {'documentId': '140627051811-2ff75b1d851746299f5e36ec2f8e8c66', 'title': 'C California Style', 'description': 'December 2010', 'dataconfigId': '6936490/8659404'},
'52': {'documentId': '140627171411-0812b1ccec9b4b198ae8228c6a5783e7', 'title': 'C California Style', 'description': 'November 2010', 'dataconfigId': '6936490/8659474'},
'51': {'documentId': '140627171051-d3d2277dfe1e458d80de4480871e8ad9', 'title': 'C for Men', 'description': 'Fall 2010', 'dataconfigId': '6936490/8659426'},
'50': {'documentId': '140627171218-0bfa8349bae048f39f1b2d3f9c94b425', 'title': 'C California Style', 'description': 'October 2010', 'dataconfigId': '6936490/8659485'},
'49': {'documentId': '140627170928-d7a02ea47335403795a819df28bf6d0a', 'title': 'C California Style', 'description': 'September 2010', 'dataconfigId': '6936490/8659492'},
'48': {'documentId': '140627170708-c18ef59a1e574d2ea2994d00ada9404e', 'title': 'C California Style', 'description': 'August 2010', 'dataconfigId': '6936490/8659314'},
'47': {'documentId': '140627170554-168c5203f73e4db7b109b2be65733e0a', 'title': 'C California Style', 'description': 'Summer 2010', 'dataconfigId': '6936490/8659502'},
'46': {'documentId': '140627170417-095ba64176f24eaea3071792418671d0', 'title': 'C California Style', 'description': 'May 2010', 'dataconfigId': '6936490/8659459'},
'45': {'documentId': '140627051232-29b325ff13c9409c878478b2ab99f179', 'title': 'C California Style', 'description': 'April 2010', 'dataconfigId': ''},
'44': {'documentId': '140627051149-a82b0972df5c4070b8761651354e43b4', 'title': 'C California Style', 'description': 'March 2010', 'dataconfigId': ''},
'43': {'documentId': '140627170220-cf8010bdc39e4e8683562761a7b735a3', 'title': 'C Weddings', 'description': 'Spring 2010', 'dataconfigId': '6936490/8659446'},
'42': {'documentId': '140627042724-c1caae6980e54c89877732f7579b206d', 'title': 'C California Style', 'description': 'Winter 2009', 'dataconfigId': ''},
'41': {'documentId': '140627042642-a61bb75d39d64674961d0a01a4c8b747', 'title': 'C California Style', 'description': 'November 2009', 'dataconfigId': ''},
'40': {'documentId': '140627042600-7b635de42da74a4c8b58fa85979c02b8', 'title': 'C California Style', 'description': 'October 2009', 'dataconfigId': ''},
'39': {'documentId': '140627042526-23c29d472b4d4ddc980f68c92f63a754', 'title': 'C California Style', 'description': 'September 2009', 'dataconfigId': ''},
'38': {'documentId': '140627042449-a41b5e1d876a430998f36ed0ac84501b', 'title': 'C California Style', 'description': 'Summer 2009', 'dataconfigId': ''},
'37': {'documentId': '140627042336-5e190f3713ab457f9a03c2c6c67cf824', 'title': 'C California Style', 'description': 'April/May 2009', 'dataconfigId': ''},
'36': {'documentId': '140627042308-6dd63118449640f983dc26be846f1402', 'title': 'C California Style', 'description': 'March 2009', 'dataconfigId': ''},
'35': {'documentId': '140627042236-19398900c0d6449b98be51688c83dc4a', 'title': 'C California Style', 'description': 'January/February 2009', 'dataconfigId': ''},
'34': {'documentId': '140627041806-f85db3c9ccc147e2950e50f8b42e4b06', 'title': 'C California Style', 'description': 'December 2008', 'dataconfigId': ''},
'33': {'documentId': '140627041722-12cd20d6d8fd447ab6f222288aaa5cb6', 'title': 'C California Style', 'description': 'November 2008', 'dataconfigId': ''},
'32': {'documentId': '140627041649-562a705c66f24e1a9513899a01b5cf4b', 'title': 'C California Style', 'description': 'October 2008', 'dataconfigId': ''},
'31': {'documentId': '140627041450-471835451a87484594a813f34aa819cb', 'title': 'C California Style', 'description': 'September 2008', 'dataconfigId': ''},
'30': {'documentId': '140627041411-7bb1333e19704f49bd6ebe0cec59a71b', 'title': 'C California Style', 'description': 'August 2008', 'dataconfigId': ''},
'29': {'documentId': '140627041335-a2847cea3c8949218d94f76fc4779a10', 'title': 'C California Style', 'description': 'June/July 2008', 'dataconfigId': ''},
'28': {'documentId': '140627041305-2bd522a2ff0048d09820a20cb0ca59dc', 'title': 'C California Style', 'description': 'May 2008', 'dataconfigId': ''},
'27': {'documentId': '140627041228-3027c38115cd47ee99f370c0182d1d24', 'title': 'C California Style', 'description': 'April 2008', 'dataconfigId': ''},
'26': {'documentId': '140627041155-a3bb0e7f6b5249e08e5da004a09228c5', 'title': 'C California Style', 'description': 'March 2008', 'dataconfigId': ''},
'25': {'documentId': '140627041125-75f4db4f7042422eaeef12bb13013aa4', 'title': 'C California Style', 'description': 'January/February 2008', 'dataconfigId': ''},
'24': {'documentId': '140627035948-b2861fde2db84a318ddf3b17202477a0', 'title': 'C California Style', 'description': 'December 2007', 'dataconfigId': ''},
'23': {'documentId': '140627035800-26d51492f1774af2bcc2ee0e14781799', 'title': 'C California Style', 'description': 'November 2007', 'dataconfigId': ''},
'22': {'documentId': '140627035727-d9301df3c90e4054a8dd4a61da094e79', 'title': 'C California Style', 'description': 'October 2007', 'dataconfigId': ''},
'21': {'documentId': '140627035642-12097243c62f4f26822477bafbd102ad', 'title': 'C California Style', 'description': 'September 2007', 'dataconfigId': ''},
'20': {'documentId': '140627035418-533dbef565fa4f92ae4226fe798a0d5c', 'title': 'C California Style', 'description': 'August 2007', 'dataconfigId': ''},
'19': {'documentId': '140627035342-aacfc26a667a4f79832e2e42883fabc2', 'title': 'C California Style', 'description': 'June/July 2007', 'dataconfigId': ''},
'18': {'documentId': '140627035258-8c7e5220f2c241dbbe23d705c7108496', 'title': 'C California Style', 'description': 'May 2007', 'dataconfigId': ''},
'17': {'documentId': '140627035224-4c778a5e48b7405ca3faeb8296e266f1', 'title': 'C California Style', 'description': 'April 2007', 'dataconfigId': ''},
'16': {'documentId': '140627035143-9eca4338eb7f4fa485c3ea8a080f3845', 'title': 'C California Style', 'description': 'March 2007', 'dataconfigId': ''},
'15': {'documentId': '140627035102-e83196f0b8374db7841c0e1049f27638', 'title': 'C California Style', 'description': 'January/February 2007', 'dataconfigId': ''},
'14': {'documentId': '140627031851-bd24a7f95edf40a7a71b635e06a0a390', 'title': 'C California Style', 'description': 'December 2006', 'dataconfigId': ''},
'13': {'documentId': '140627031812-48017477057a4b3581275e78f6dca26c', 'title': 'C California Style', 'description': 'November 2006', 'dataconfigId': ''},
'12': {'documentId': '140627031732-ad435fe70b854f8c9043a68f841ff874', 'title': 'C California Style', 'description': 'October 2006', 'dataconfigId': ''},
'11': {'documentId': '140627031645-93236b1a162a4f6e95d086e927c5abcd', 'title': 'C California Style', 'description': 'September 2006', 'dataconfigId': ''},
'10': {'documentId': '140627031550-aed35b470c474063af2a6ca73bb2bfa3', 'title': 'C California Style', 'description': 'August 2006', 'dataconfigId': '6936490/8660589'},
'9': {'documentId': '140627031432-e82249d93984483fb39d7e622338241b', 'title': 'C California Style', 'description': 'June/July 2006', 'dataconfigId': ''},
'8': {'documentId': '140627034316-a1d552a5c4d542508aeb5ae9b4acd722', 'title': 'C California Style', 'description': 'May 2006', 'dataconfigId': ''},
'7': {'documentId': '140625185434-4a7de769ac014644a82c5e2796cc115a', 'title': 'C California Style', 'description': 'April 2006', 'dataconfigId': ''},
'6': {'documentId': '140627031326-85a2fdcf1b1f4419a287059db9685270', 'title': 'C California Style', 'description': 'March 2006', 'dataconfigId': ''},
'5': {'documentId': '140625185051-978d035e2b964706b92985bd54bfa01d', 'title': 'C California Style', 'description': 'January/February 2006', 'dataconfigId': ''},
'4': {'documentId': '140625184836-790d72da166c477591d6c42098245e31', 'title': 'C California Style', 'description': 'December 2005', 'dataconfigId': ''},
'3': {'documentId': '140625184647-8d0cf610515140589bca9d41c2e9cb3d', 'title': 'C California Style', 'description': 'November 2005', 'dataconfigId': ''},
'2': {'documentId': '140625184224-68b603889dbb4e6d96fbf9fa5104e319', 'title': 'C California Style', 'description': 'October 2005', 'dataconfigId': ''},
'1': {'documentId': '140625182723-1de1742c84d241bdaa2cb46cb264ae16', 'title': 'C California Style', 'description': 'September 2005', 'dataconfigId': ''}
}



# test of issuu request
@app.route('/', methods=['GET'])
@app.route('/issuu', methods=['GET'])
def on_issuu_get():
    issues = get_issuu()
    result = set_flag(issues)
    return render_template('issuu.tpl', result = result, version = version)

@app.route('/new', methods=['GET'])
def give_issuu():
    return render_template('new.tpl', version = version)

@app.route('/digital', methods=['GET'])
def go_stats():
    return render_template('digital.tpl', version = version)

@app.route('/<name>', methods=['GET'])
def find_issuu(name):
    if name in embeds:
        result = embeds[name]
        print result
        return render_template('doc.tpl', result = result, version = version)
    else:
        return redirect(url_for('on_issuu_get'))

@app.route('/embed', methods=['POST'])
def post_embed():
    action = 'issuu.document_embed.add'
    issuu_url = 'http://api.issuu.com/1_0'
    documentId = '140702225753-ee2087e9ac60465babc876065483da86'
    readerStartPage = 0
    width = 400
    height = 300
    sig_query = issuu_secret + 'access' + access + 'action' + action + 'apiKey' + issuu_key + 'commentsAllowed' + commentsAllowed + 'description' + description + 'name' + name + 'publishDate' + publishDate + 'title' + title
    signature = hashlib.md5(sig_query).hexdigest()
    post_data = {'signature':signature, 'access':access, 'action':action, 'apiKey':issuu_key, 'commentsAllowed':commentsAllowed, 'description':description, 'name':name, 'publishDate':publishDate, 'title':title}
    r = requests.post(issuu_url, data=post_data, files={'file':f})
    message = str(r.text)
    print r.headers
    print r.text
    print r.status_code
    print message
    upload.delete_file(file)
    return render_template('ok.tpl', message = message, version = version)

@app.route('/upload', methods=['POST'])
def upload_issuu():
    action = 'issuu.document.upload'
    issuu_url = 'http://upload.issuu.com/1_0'
    btn = request.form['btn']
    if btn == 'Cancel':
        return redirect(url_for('on_issuu_get'))
    name = request.form['name']
    print name
    title = request.form['title']
    description = request.form['description']
    publishDate = request.form['publishDate']
    access = request.form['access']
    file = request.files['file']
    commentsAllowed = 'false'
    f = upload.upload_file(file)
    sig_query = issuu_secret + 'access' + access + 'action' + action + 'apiKey' + issuu_key + 'commentsAllowed' + commentsAllowed + 'description' + description + 'name' + name + 'publishDate' + publishDate + 'title' + title
    signature = hashlib.md5(sig_query).hexdigest()
    post_data = {'signature':signature, 'access':access, 'action':action, 'apiKey':issuu_key, 'commentsAllowed':commentsAllowed, 'description':description, 'name':name, 'publishDate':publishDate, 'title':title}
    r = requests.post(issuu_url, data=post_data, files={'file':f})
    message = str(r.text)
    print r.headers
    print r.text
    print r.status_code
    print message
    upload.delete_file(file)
    return render_template('ok.tpl', message = message, version = version)

def get_issuu():
    issuu_url = 'http://api.issuu.com/1_0?'
    action = 'issuu.documents.list'
    responseParams='name,documentId,title,description,publishDate'
    i = []
    result = []
    sig_query = issuu_secret + 'action' + action + 'apiKey' + issuu_key + 'documentSortBy' + documentSortBy + 'documentStates' + documentStates + 'format' + format + 'orgDocTypes' + orgDocTypes + 'pageSize' + str(pageSize) + 'responseParams' + responseParams + 'resultOrder' + resultOrder + 'startIndex' + str(startIndex)
    req_query = 'action' + '=' + action + '&' + 'apiKey' + '=' + issuu_key + '&' + 'documentSortBy' + '=' + documentSortBy + '&' + 'documentStates' + '=' + documentStates + '&' + 'format' + '=' + format + '&' + 'orgDocTypes' + '=' + orgDocTypes + '&' + 'pageSize' + '=' + str(pageSize) + '&' + 'responseParams' + '=' + responseParams + '&' + 'resultOrder' + '=' + resultOrder + '&' + 'startIndex' + '=' + str(startIndex)
    signature = hashlib.md5(sig_query).hexdigest()
    query = issuu_url + req_query + '&' + 'signature' + '=' + signature
    response = urllib2.urlopen(query)
    response = json.loads(response.read())
    i = response['rsp']['_content']['result']['_content']
    for doc in i:
        if not 'description' in list(doc['document']):
            doc['document']['description'] = doc['document']['title']
        if not doc['document']['description'][0] == '*':
            result.append({'description': doc['document']['description'], 'documentId': doc['document']['documentId'], 'name': doc['document']['name'], 'title': doc['document']['title']})
    print result
    return result

def get_embed(documentId):
    issuu_url = 'http://api.issuu.com/1_0?'
    action = 'issuu.document_embeds.list'
    responseParams = 'dataConfigId,documentId'
    embedSortBy = 'documentId'
    i = []
    result = []
    sig_query = issuu_secret + 'action' + action + 'apiKey' + issuu_key + 'documentId' + documentId + 'embedSortBy' + embedSortBy + 'format' + format + 'pageSize' + str(pageSize) + 'responseParams' + responseParams + 'resultOrder' + resultOrder + 'startIndex' + str(startIndex)
    req_query = 'action' + '=' + action + '&' + 'apiKey' + '=' + issuu_key + '&' + 'documentId' + '=' + documentId + '&' + 'embedSortBy' + '=' + embedSortBy + '&'  + 'format' + '=' + format + '&' +  'pageSize' + '=' + str(pageSize) + '&' + 'responseParams' + '=' + responseParams + '&' + 'resultOrder' + '=' + resultOrder + '&' + 'startIndex' + '=' + str(startIndex)
    signature = hashlib.md5(sig_query).hexdigest()
    query = issuu_url + req_query + '&' + 'signature' + '=' + signature
    response = urllib2.urlopen(query)
    response = json.loads(response.read())
    result = response['rsp']['_content']['result']['_content'][0]['documentEmbed']['dataConfigId']
    return result

def set_flag(issues):
    result = []
    for i in issues:
        if i['name'] in embeds:
            i['dataconfigId'] = embeds[(i['name'])]['dataconfigId']
            result.append(i)
    return result

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 17939))
    app.run(host='0.0.0.0', port=port, debug=True)
