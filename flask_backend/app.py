from flask import Flask, request, jsonify
import logging
import json
import requests
from flask_cors import CORS
import asyncio

from ReportGeneration import getReportDataFromHumeEVI, getPreliminaryReport
from RealTimeIntelligence import get_agent_emotion_guidance_map, get_avg_top3_emotion, get_User_Agent_Emotion_Map

prev_user_emotional_state = "Calmness"
app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.INFO)




d = [{'chat_id': '133048ae-ff83-4afe-b891-74957e288032', 'emotion_features': None, 'id': 'f11ffcef-35e4-4ae0-9e39-9c899652f654', 'message_text': 'you are a hiring manager who is conversing with a sales agent. the sales agent will sell you a hiring solution and you need to raise concerns, objections. ', 'metadata': None, 'role': 'SYSTEM', 'timestamp': 1724512380634, 'type': 'SYSTEM_PROMPT'}, {'chat_id': '133048ae-ff83-4afe-b891-74957e288032', 'emotion_features': '{"Admiration": 0.05926513671875, "Adoration": 0.051513671875, "Aesthetic Appreciation": 0.033233642578125, "Amusement": 0.2646484375, "Anger": 0.0338134765625, "Anxiety": 0.015411376953125, "Awe": 0.053436279296875, "Awkwardness": 0.066162109375, "Boredom": 0.0799560546875, "Calmness": 0.036834716796875, "Concentration": 0.02020263671875, "Confusion": 0.0192413330078125, "Contemplation": 0.01788330078125, "Contempt": 0.032958984375, "Contentment": 0.085205078125, "Craving": 0.0205230712890625, "Desire": 0.0284881591796875, "Determination": 0.05755615234375, "Disappointment": 0.032989501953125, "Disgust": 0.0243988037109375, "Distress": 0.0239105224609375, "Doubt": 0.0150146484375, "Ecstasy": 0.10772705078125, "Embarrassment": 0.0169830322265625, "Empathic Pain": 0.004985809326171875, "Entrancement": 0.03155517578125, "Envy": 0.056060791015625, "Excitement": 0.297119140625, "Fear": 0.007625579833984375, "Guilt": 0.0164794921875, "Horror": 0.004482269287109375, "Interest": 0.159912109375, "Joy": 0.2276611328125, "Love": 0.055328369140625, "Nostalgia": 0.022125244140625, "Pain": 0.005157470703125, "Pride": 0.114990234375, "Realization": 0.04620361328125, "Relief": 0.03265380859375, "Romance": 0.01406097412109375, "Sadness": 0.0119171142578125, "Satisfaction": 0.0865478515625, "Shame": 0.01511383056640625, "Surprise (negative)": 0.01462554931640625, "Surprise (positive)": 0.1558837890625, "Sympathy": 0.0066070556640625, "Tiredness": 0.0232391357421875, "Triumph": 0.11138916015625}', 'id': 'ae85b5f0-d307-494e-9e71-4f0feee6231c', 'message_text': 'Hi there.', 'metadata': '{"segments": [{"content": "Hi there.", "embedding": [0.6298828125, 0.1663818359375, -32.125, 1.2626953125, 0.912109375, 0.63671875, 2.833984375, 0.10406494140625, 0.2919921875, 0.9755859375, 1.34375, 0.7197265625, 0.4111328125, 1.00390625, -0.328125, 0.35546875, -1.369140625, 1.0029296875, 1.302734375, 0.56396484375, 0.53515625, -0.1734619140625, 1.693359375, 0.2359619140625, 2.05859375, -0.312744140625, 0.05474853515625, 1.337890625, 0.9462890625, 0.01383209228515625, 0.6943359375, 1.873046875, -0.92919921875, 0.95263671875, -0.27587890625, 1.5029296875, 0.59375, 1.0244140625, -0.1727294921875, 1.4111328125, -0.298583984375, -0.43994140625, -0.1531982421875, -0.10980224609375, -0.2069091796875, 0.8896484375, 1.2685546875, 1.677734375, 0.8125, -0.338134765625, -0.3193359375, 0.428466796875, 0.810546875, 0.54833984375, 1.6689453125, 0.64697265625, 0.74365234375, 1.486328125, 1.0009765625, -1.6767578125, 0.72314453125, 2.123046875, 2.138671875, 0.434326171875, -0.122802734375, 1.912109375, -4.25390625, 0.35498046875, 0.275390625, 0.767578125, 0.255126953125, 0.46337890625, 1.2060546875, -1.5087890625, 1.0732421875, 0.85693359375, 1.01953125, 0.0139923095703125, 1.349609375, 1.0537109375, 1.5263671875, -0.494140625, 0.587890625, 0.814453125, -0.93994140625, -0.0631103515625, 1.318359375, 1.126953125, 0.61962890625, 1.5048828125, 0.35693359375, 1.1513671875, 1.4716796875, 0.8046875, 0.140380859375, 1.7978515625, 0.701171875, -15.265625, 1.2109375, 0.304443359375, 0.498046875, 1.564453125, 0.95703125, -0.2342529296875, 0.90380859375, 3.416015625, 0.76171875, 0.71826171875, 1.21875, 1.3994140625, -0.56494140625, -1.796875, 1.369140625, 0.441650390625, 1.8857421875, -0.421630859375, 0.166015625, 1.552734375, -1.2119140625, 2.521484375, 0.5859375, 0.2099609375, -0.01258087158203125, -0.669921875, -0.031402587890625, -0.2210693359375, 2.833984375, 1.388671875, 0.5400390625, 0.79443359375, 3.001953125, 0.76904296875, 0.210205078125, 0.403564453125, 0.39111328125, 2.037109375, -0.10052490234375, 1.5166015625, 1.4208984375, 1.953125, 1.126953125, 0.31103515625, 0.34033203125, 1.6552734375, -0.87060546875, -0.1993408203125, 1.4375, 1.0390625, -0.5146484375, -0.459228515625, 0.1455078125, 1.2314453125, -1.1083984375, 0.56591796875, 1.3125, 0.425537109375, 0.2030029296875, 2.412109375, 0.292724609375, 0.90625, -0.1505126953125, 0.64453125, -0.079345703125, 0.006801605224609375, -0.042236328125, -0.5947265625, 2.005859375, 0.5908203125, 0.357666015625, 1.27734375, 1.216796875, 1.0400390625, 0.1334228515625, 1.0439453125, -0.3681640625, 0.197265625, 0.7783203125, 0.60205078125, 0.97216796875, 0.2242431640625, 1.2666015625, 0.09490966796875, 1.33203125, 0.7314453125, 1.3212890625, 0.390869140625, 1.0966796875, 0.98681640625, -1.5380859375, 0.0213775634765625, 0.6630859375, 0.244140625, 0.564453125, 1.8046875, 0.8603515625, 2.58203125, 0.73291015625, 0.86181640625, 0.55224609375, 0.93798828125, 0.045623779296875, 1.66796875, 1.982421875, 1.1572265625, 1.171875, 1.5029296875, 0.019134521484375, 0.5908203125, -1.4638671875, 0.810546875, 0.74169921875, -0.6337890625, -0.62744140625, 1.765625, 0.0237884521484375, -0.40625, 0.44921875, 4.7734375, 1.2509765625, -0.69189453125, 0.67333984375, 0.615234375, -1.5029296875, 1.759765625, 0.80810546875, 0.65185546875, 0.2474365234375, 1.62109375, 0.8720703125, 1.7353515625, 2.0078125, 1.5595703125, 0.68896484375, 1.3720703125, 0.88818359375, 1.005859375, 0.11883544921875, 2.001953125, 0.0650634765625, -0.0738525390625, 0.037567138671875, -1.7490234375, 2.01171875, 3.486328125, 0.405517578125, 1.6298828125, -0.266357421875, 0.87255859375, -0.1285400390625, 0.91455078125, 0.82470703125, 0.69140625, 0.036895751953125, 1.234375, 1.052734375, -0.16455078125, 1.0791015625, 0.61669921875, 1.3427734375, 1.1982421875, 0.56494140625, 1.33984375, 2.244140625, 0.490478515625, 0.91162109375, 0.578125, -0.6904296875, 0.2685546875, -0.703125, 0.81396484375, 0.58056640625, 1.6044921875, 0.8662109375, 2.23046875, -0.5517578125, 1.7666015625, 1.33203125, 1.2333984375, 0.681640625, 0.94677734375, 1.052734375, -1.0859375, 1.8115234375, -0.387939453125, 1.0595703125, 0.2998046875, 1.556640625, 1.6708984375, 1.3359375, 2.794921875, 2.02734375, -0.49169921875, 0.740234375, 0.02374267578125, 1.421875, -0.0074462890625, 0.05072021484375, -0.9658203125, 0.263427734375, 1.1748046875, 1.19921875, 1.96875, -0.08233642578125, 1.2333984375, -0.324462890625, 0.67333984375, 0.4033203125, 1.3212890625, 1.3056640625, 0.57470703125, 0.044525146484375, 0.9638671875, 0.91748046875, 0.11590576171875, 1.3125, 0.11419677734375, 2.220703125, 1.248046875, 1.583984375, 0.5947265625, 1.7509765625, -0.250732421875, -0.01081085205078125, -0.25439453125, -0.1834716796875, 0.90966796875, 0.62255859375, 0.2822265625, 0.7861328125, 1.162109375, 1.1796875, -0.279052734375, -0.25048828125, 1.908203125, 1.314453125, 2.171875, 0.26123046875, 1.4033203125, 0.038330078125, 1.2685546875, 1.1044921875, 0.9541015625, 0.869140625, -1.9072265625, 1.1494140625, 0.403076171875, 1.1328125, 0.9619140625, 0.72265625, 2.240234375, 0.059295654296875, 0.64111328125, 0.42236328125, 0.81396484375, 0.314697265625, -0.314697265625, 0.0115509033203125, 0.1513671875, 0.10833740234375, -0.309326171875, 1.130859375, -0.8427734375, 1.3916015625, 0.054229736328125, 1.177734375, 0.96923828125, 1.814453125, 1.150390625, 0.61083984375, 1.2509765625, -1.26171875, 0.3740234375, 0.83740234375, 0.226318359375, 0.004253387451171875, 0.87109375, 1.646484375, 1.103515625, 0.4365234375, 1.8056640625, 0.450927734375, 1.2705078125, 0.09405517578125, -0.8974609375, 1.796875, 1.4267578125, -0.07769775390625, 0.6181640625, 2.056640625, 0.677734375, -0.35693359375, 0.1976318359375, 0.2122802734375, 0.818359375, -1.470703125, 0.95263671875, 0.84619140625, -0.3935546875, 4.046875, 2.515625, 1.2294921875, 0.84033203125, 0.230224609375, 1.0478515625, -1.9853515625, 0.82958984375, 0.412353515625, 0.521484375, 0.313232421875, -0.783203125, 0.716796875, 0.9912109375, -0.1571044921875, 0.95751953125, 1.6865234375, 0.29296875, 0.6806640625, 0.54736328125, 0.428955078125, 0.98681640625, -0.36328125, 1.0029296875, -0.1429443359375, 0.444091796875, 0.1920166015625, 1.818359375, 1.1240234375, -0.48828125, -0.329345703125, 0.78515625, -0.0799560546875, 0.72900390625, -1.9296875, 1.3544921875, -3.857421875, 2.529296875, 1.36328125, 0.1370849609375, 0.77490234375, 0.77978515625, -0.35498046875, 1.1484375, -0.329345703125, 2.0, -0.2325439453125, 0.62548828125, 0.374755859375, 0.3056640625, 0.83349609375, 1.03515625, 0.58544921875, 0.60986328125, 14.2734375, -1.986328125, -0.35888671875, 1.2333984375, 0.0914306640625, -0.66943359375, -0.053253173828125, 0.39892578125, 0.1614990234375, 0.1414794921875, 0.26171875, 1.166015625, -1.3662109375, 0.84033203125, 1.177734375, 0.34814453125, 0.2685546875, 0.10931396484375, 0.221923828125, -0.03302001953125, 0.63525390625, -0.00939178466796875, -1.923828125, 0.2269287109375, 0.5625, 1.306640625, 1.154296875, 1.201171875, 0.99267578125, 1.6708984375, -0.029632568359375, 1.455078125, 0.810546875, 1.544921875, 1.240234375, -0.74169921875, 1.8251953125, 1.1103515625, 1.9208984375, -0.494384765625, 0.77880859375, 1.0576171875, 0.94775390625, 3.36328125, 0.030364990234375, 0.873046875, 0.55029296875, 1.23828125, 1.9814453125, 1.4677734375, 0.09808349609375, 1.1005859375, -0.004016876220703125, 2.05859375, 0.355224609375, -0.52197265625, 1.21484375, 0.452392578125, 0.66357421875, 0.119384765625, 1.08203125, -0.931640625, -0.281982421875, 1.4443359375, 2.03125, 3.1796875, 1.6572265625, 1.0693359375, -0.53076171875, 0.748046875, 1.36328125, 0.1573486328125, 0.236083984375, 0.6259765625, -0.11962890625, 0.76171875, -0.5283203125, -0.358154296875, 1.3017578125, 0.95751953125, 0.60302734375, 1.361328125, 1.0556640625, 0.2230224609375, 0.92626953125, 0.6748046875, 5.84375, 1.1025390625, -0.51416015625, -0.395263671875, 0.70947265625, 0.239990234375, -0.464111328125, 1.935546875, 0.544921875, 0.07159423828125, 0.1756591796875, 0.86962890625, -0.5576171875, 0.2568359375, 0.2423095703125, 2.55078125, 0.9599609375, 0.497802734375, 0.12359619140625, 0.0811767578125, 0.6748046875, -0.3427734375, 1.2880859375, 0.2548828125, 1.9931640625, 2.79296875, -0.309814453125, -0.1707763671875, -0.343505859375, 0.4853515625, 0.833984375, 1.876953125, 0.095458984375, 0.65966796875, 0.005229949951171875, -0.81787109375, 1.7509765625, 0.654296875, 0.1759033203125, 0.266357421875, -0.481689453125, -0.253662109375, 0.74072265625, 0.6513671875, 0.73876953125, 0.48193359375, 0.84033203125, -0.43115234375, -0.0576171875, -0.455078125, 0.75, 0.673828125, 0.21044921875, -0.271240234375, -0.53759765625, 0.9658203125, 0.8515625, -3.30078125, -0.238525390625, 0.78515625, 0.259765625, -0.1314697265625, -0.0290374755859375, -0.83154296875, 0.2200927734375, 0.9423828125, 0.64306640625, -0.53515625, 0.1602783203125, -0.348388671875, -0.0306854248046875, -0.6884765625, 0.8974609375, 0.69482421875, 0.8125, -0.2393798828125, 1.1953125, 0.63623046875, 1.3173828125, 0.87939453125, 0.7001953125, 1.06640625, 1.3828125, 0.52197265625, 0.97607421875, 0.74609375, 1.5361328125, 0.515625, -0.383056640625, 2.33203125, 0.35107421875, -0.62939453125, 0.329345703125, 0.767578125, -0.68359375, -0.251708984375, 1.5615234375, 1.3505859375, 0.09814453125, -0.187744140625, 1.4716796875, -0.79443359375, 0.5478515625, 0.11151123046875, 0.0302581787109375, 0.58203125, -0.47900390625, 0.18310546875, 0.0294342041015625, 0.1766357421875, 0.0589599609375, -0.56494140625, 2.02734375, 2.4375, -0.72314453125, 2.1171875, 0.494873046875, -0.0948486328125, 0.25439453125, 1.6865234375, 1.517578125, 0.40087890625, 0.41357421875, 1.0703125, -0.8037109375, 0.5107421875, 0.2220458984375, -0.28759765625, 0.395263671875, 0.72998046875, 0.68896484375, 1.486328125, 0.043609619140625, 0.394775390625, 1.234375, 1.1279296875, -5.453125, 0.7587890625, 0.3232421875, 1.03125, 1.2001953125, 0.126953125, 0.256103515625, 1.552734375, 1.576171875, -0.0849609375, 0.469970703125, 1.900390625, 5.203125, 1.6259765625, 0.9443359375, -0.161376953125, 0.4833984375, 0.82373046875, 1.0244140625, 0.2232666015625, 0.3076171875, -1.123046875, 0.541015625, 0.9228515625, 0.458251953125, 1.9453125, 0.64599609375, 1.2900390625, 1.0654296875, 0.56884765625, 2.296875, 0.2344970703125, 1.8056640625, -0.479248046875, -0.8369140625, 0.904296875, 1.53125, 0.91796875, 1.05078125, 0.337646484375, -0.44873046875, 2.12109375, 1.2880859375, -0.30810546875, -9.1484375, 0.4404296875, 0.89501953125, -0.5380859375, 0.95947265625, 0.76513671875, 0.84814453125, 1.5625, -0.11907958984375, 0.75537109375, 1.0087890625, -0.0914306640625, 1.611328125, 0.076171875, 0.51953125, 0.828125, 2.41015625, 0.66015625, 3.162109375, 0.1336669921875, 0.460205078125, 0.7900390625, 1.9248046875, 1.87109375, 0.8447265625, -1.376953125, -0.130615234375, 0.369873046875, 0.2493896484375, 0.7470703125, 1.82421875, 1.408203125, 0.6123046875, 1.0126953125, 1.095703125, 0.477783203125, -0.28662109375, 0.49267578125, 0.80517578125, 1.927734375, 0.90869140625, 0.1622314453125, 2.56640625, 1.689453125, -0.2249755859375, 0.982421875, 0.37744140625, -1.125, 1.6328125, 0.381591796875], "scores": [0.05926513671875, 0.051513671875, 0.033233642578125, 0.2646484375, 0.0338134765625, 0.015411376953125, 0.053436279296875, 0.066162109375, 0.0799560546875, 0.036834716796875, 0.02020263671875, 0.01788330078125, 0.0192413330078125, 0.032958984375, 0.085205078125, 0.0205230712890625, 0.05755615234375, 0.032989501953125, 0.0243988037109375, 0.0239105224609375, 0.0150146484375, 0.10772705078125, 0.0169830322265625, 0.004985809326171875, 0.03155517578125, 0.056060791015625, 0.297119140625, 0.007625579833984375, 0.0164794921875, 0.004482269287109375, 0.159912109375, 0.2276611328125, 0.055328369140625, 0.022125244140625, 0.005157470703125, 0.114990234375, 0.04620361328125, 0.03265380859375, 0.01406097412109375, 0.0119171142578125, 0.0865478515625, 0.0284881591796875, 0.01511383056640625, 0.01462554931640625, 0.1558837890625, 0.0066070556640625, 0.0232391357421875, 0.11138916015625], "stoks": [473, 497, 509, 132, 132, 132, 132, 7, 148, 7, 72, 367, 397, 236, 236, 236, 448, 236], "time": {"begin_ms": 640, "end_ms": 1380}}]}', 'role': 'USER', 'timestamp': 1724512385388, 'type': 'USER_MESSAGE'}, {'chat_id': '133048ae-ff83-4afe-b891-74957e288032', 'emotion_features': '{"Admiration": 0.044097900390625, "Adoration": 0.026611328125, "Aesthetic Appreciation": 0.0303802490234375, "Amusement": 0.11859130859375, "Anger": 0.06097412109375, "Anxiety": 0.03582763671875, "Awe": 0.0364990234375, "Awkwardness": 0.055938720703125, "Boredom": 0.043212890625, "Calmness": 0.0836181640625, "Concentration": 0.060760498046875, "Confusion": 0.059112548828125, "Contemplation": 0.0323486328125, "Contempt": 0.036285400390625, "Contentment": 0.06866455078125, "Craving": 0.0121002197265625, "Desire": 0.01433563232421875, "Determination": 0.10394287109375, "Disappointment": 0.050811767578125, "Disgust": 0.0260009765625, "Distress": 0.051544189453125, "Doubt": 0.0416259765625, "Ecstasy": 0.0271759033203125, "Embarrassment": 0.0216217041015625, "Empathic Pain": 0.0153045654296875, "Entrancement": 0.015899658203125, "Envy": 0.015960693359375, "Excitement": 0.135009765625, "Fear": 0.02685546875, "Guilt": 0.015716552734375, "Horror": 0.01554107666015625, "Interest": 0.1297607421875, "Joy": 0.07684326171875, "Love": 0.0239105224609375, "Nostalgia": 0.0224151611328125, "Pain": 0.0197601318359375, "Pride": 0.0548095703125, "Realization": 0.073974609375, "Relief": 0.04327392578125, "Romance": 0.0131683349609375, "Sadness": 0.0256195068359375, "Satisfaction": 0.07989501953125, "Shame": 0.01495361328125, "Surprise (negative)": 0.04803466796875, "Surprise (positive)": 0.08270263671875, "Sympathy": 0.0211181640625, "Tiredness": 0.02044677734375, "Triumph": 0.04248046875}', 'id': '9fb44e5c-5088-4e54-b927-9f2ae8c375ca', 'message_text': 'Hey!', 'metadata': None, 'role': 'AGENT', 'timestamp': 1724512385390, 'type': 'AGENT_MESSAGE'}, {'chat_id': '133048ae-ff83-4afe-b891-74957e288032', 'emotion_features': '{"Admiration": 0.057586669921875, "Adoration": 0.031982421875, "Aesthetic Appreciation": 0.04681396484375, "Amusement": 0.1771240234375, "Anger": 0.03326416015625, "Anxiety": 0.035064697265625, "Awe": 0.05572509765625, "Awkwardness": 0.0830078125, "Boredom": 0.037109375, "Calmness": 0.0704345703125, "Concentration": 0.042327880859375, "Confusion": 0.05645751953125, "Contemplation": 0.0154876708984375, "Contempt": 0.019989013671875, "Contentment": 0.0982666015625, "Craving": 0.007755279541015625, "Desire": 0.0074615478515625, "Determination": 0.055206298828125, "Disappointment": 0.0212860107421875, "Disgust": 0.01560211181640625, "Distress": 0.0289764404296875, "Doubt": 0.025177001953125, "Ecstasy": 0.054901123046875, "Embarrassment": 0.0204925537109375, "Empathic Pain": 0.005344390869140625, "Entrancement": 0.0164031982421875, "Envy": 0.0179901123046875, "Excitement": 0.2454833984375, "Fear": 0.02508544921875, "Guilt": 0.011688232421875, "Horror": 0.014617919921875, "Interest": 0.2264404296875, "Joy": 0.166259765625, "Love": 0.030914306640625, "Nostalgia": 0.01016998291015625, "Pain": 0.0087432861328125, "Pride": 0.040618896484375, "Realization": 0.0390625, "Relief": 0.04327392578125, "Romance": 0.00981903076171875, "Sadness": 0.0119171142578125, "Satisfaction": 0.08660888671875, "Shame": 0.0083160400390625, "Surprise (negative)": 0.036895751953125, "Surprise (positive)": 0.1798095703125, "Sympathy": 0.00974273681640625, "Tiredness": 0.0106964111328125, "Triumph": 0.04010009765625}', 'id': 'd0dd122f-e109-45df-8e81-89f9c9edc7ef', 'message_text': 'Hello there!', 'metadata': None, 'role': 'AGENT', 'timestamp': 1724512386885, 'type': 'AGENT_MESSAGE'}, {'chat_id': '133048ae-ff83-4afe-b891-74957e288032', 'emotion_features': '{"Admiration": 0.1041259765625, "Adoration": 0.06292724609375, "Aesthetic Appreciation": 0.03955078125, "Amusement": 0.1268310546875, "Anger": 0.03167724609375, "Anxiety": 0.03125, "Awe": 0.04052734375, "Awkwardness": 0.048309326171875, "Boredom": 0.0294189453125, "Calmness": 0.08770751953125, "Concentration": 0.0191650390625, "Confusion": 0.027435302734375, "Contemplation": 0.0139007568359375, "Contempt": 0.015777587890625, "Contentment": 0.129638671875, "Craving": 0.007122039794921875, "Desire": 0.011871337890625, "Determination": 0.0469970703125, "Disappointment": 0.0206451416015625, "Disgust": 0.01262664794921875, "Distress": 0.0294189453125, "Doubt": 0.0200653076171875, "Ecstasy": 0.04876708984375, "Embarrassment": 0.009674072265625, "Empathic Pain": 0.00536346435546875, "Entrancement": 0.0197601318359375, "Envy": 0.01560211181640625, "Excitement": 0.2371826171875, "Fear": 0.0193023681640625, "Guilt": 0.0106964111328125, "Horror": 0.00878143310546875, "Interest": 0.1424560546875, "Joy": 0.2171630859375, "Love": 0.052337646484375, "Nostalgia": 0.0117340087890625, "Pain": 0.016845703125, "Pride": 0.0640869140625, "Realization": 0.03277587890625, "Relief": 0.0704345703125, "Romance": 0.021575927734375, "Sadness": 0.0185089111328125, "Satisfaction": 0.1541748046875, "Shame": 0.00734710693359375, "Surprise (negative)": 0.015838623046875, "Surprise (positive)": 0.092041015625, "Sympathy": 0.01111602783203125, "Tiredness": 0.0171051025390625, "Triumph": 0.0455322265625}', 'id': 'ea069a2d-ff3d-4826-9c9d-de2073686a3b', 'message_text': "It's great to meet you.", 'metadata': None, 'role': 'AGENT', 'timestamp': 1724512387081, 'type': 'AGENT_MESSAGE'}, {'chat_id': '133048ae-ff83-4afe-b891-74957e288032', 'emotion_features': '{"Admiration": 0.12200927734375, "Adoration": 0.0517578125, "Aesthetic Appreciation": 0.038818359375, "Amusement": 0.08880615234375, "Anger": 0.0265045166015625, "Anxiety": 0.01085662841796875, "Awe": 0.0323486328125, "Awkwardness": 0.01490020751953125, "Boredom": 0.00766754150390625, "Calmness": 0.044677734375, "Concentration": 0.10052490234375, "Confusion": 0.01085662841796875, "Contemplation": 0.027801513671875, "Contempt": 0.0299224853515625, "Contentment": 0.130615234375, "Craving": 0.0125732421875, "Desire": 0.0036792755126953125, "Determination": 0.22509765625, "Disappointment": 0.0161590576171875, "Disgust": 0.00861358642578125, "Distress": 0.007518768310546875, "Doubt": 0.0102081298828125, "Ecstasy": 0.042633056640625, "Embarrassment": 0.003749847412109375, "Empathic Pain": 0.0011157989501953125, "Entrancement": 0.0162811279296875, "Envy": 0.0092315673828125, "Excitement": 0.595703125, "Fear": 0.0018749237060546875, "Guilt": 0.0017681121826171875, "Horror": 0.0008358955383300781, "Interest": 0.477294921875, "Joy": 0.277099609375, "Love": 0.0207672119140625, "Nostalgia": 0.006984710693359375, "Pain": 0.0008358955383300781, "Pride": 0.1668701171875, "Realization": 0.021209716796875, "Relief": 0.033477783203125, "Romance": 0.00634002685546875, "Sadness": 0.002216339111328125, "Satisfaction": 0.2342529296875, "Shame": 0.0014553070068359375, "Surprise (negative)": 0.004608154296875, "Surprise (positive)": 0.0869140625, "Sympathy": 0.005619049072265625, "Tiredness": 0.0026111602783203125, "Triumph": 0.06964111328125}', 'id': '2aef64a2-dfaa-4fc0-a3b3-4d324929a78c', 'message_text': "I'm excited to chat with you today about our innovative hiring solution.", 'metadata': None, 'role': 'AGENT', 'timestamp': 1724512387934, 'type': 'AGENT_MESSAGE'}, {'chat_id': '133048ae-ff83-4afe-b891-74957e288032', 'emotion_features': '{"Admiration": 0.192138671875, "Adoration": 0.034698486328125, "Aesthetic Appreciation": 0.038818359375, "Amusement": 0.135498046875, "Anger": 0.038909912109375, "Anxiety": 0.010406494140625, "Awe": 0.0229339599609375, "Awkwardness": 0.0154876708984375, "Boredom": 0.0034027099609375, "Calmness": 0.12420654296875, "Concentration": 0.34423828125, "Confusion": 0.0038089752197265625, "Contemplation": 0.0701904296875, "Contempt": 0.058990478515625, "Contentment": 0.10931396484375, "Craving": 0.0125732421875, "Desire": 0.0038089752197265625, "Determination": 0.64599609375, "Disappointment": 0.034088134765625, "Disgust": 0.01666259765625, "Distress": 0.01560211181640625, "Doubt": 0.00690460205078125, "Ecstasy": 0.015960693359375, "Embarrassment": 0.0035114288330078125, "Empathic Pain": 0.00469970703125, "Entrancement": 0.01078033447265625, "Envy": 0.0189056396484375, "Excitement": 0.30810546875, "Fear": 0.0024814605712890625, "Guilt": 0.0013408660888671875, "Horror": 0.0014667510986328125, "Interest": 0.373046875, "Joy": 0.0975341796875, "Love": 0.01332855224609375, "Nostalgia": 0.027374267578125, "Pain": 0.0007495880126953125, "Pride": 0.474365234375, "Realization": 0.06671142578125, "Relief": 0.021484375, "Romance": 0.003765106201171875, "Sadness": 0.002132415771484375, "Satisfaction": 0.342529296875, "Shame": 0.001789093017578125, "Surprise (negative)": 0.00536346435546875, "Surprise (positive)": 0.031494140625, "Sympathy": 0.03436279296875, "Tiredness": 0.0018243789672851562, "Triumph": 0.1939697265625}', 'id': 'cee0c87a-daf1-478a-8779-4bd96b9485ee', 'message_text': "As a hiring manager, I'm sure you're always on the lookout for ways to streamline your recruitment process and find the best talent.", 'metadata': None, 'role': 'AGENT', 'timestamp': 1724512388370, 'type': 'AGENT_MESSAGE'}]




@app.route('/', methods=['GET'])
def get_root():
    return jsonify({'message': 'hello'}), 200

@app.route('/guidance', methods=['GET'])
def get_guidance():
    message = "Great going!!"
    emotion_to_show = "Calmness"
    try:
        current_emotion = request.args.get("emotion")
        if current_emotion == prev_user_emotional_state:
            return jsonify({'guidance': message,'emotion_to_show':emotion_to_show}), 200
        else:
            prev_user_emotional_state = current_emotion
            emotion_to_show = get_User_Agent_Emotion_Map[str(current_emotion)]
            Guidance = get_agent_emotion_guidance_map[str(emotion_to_show)]
            return jsonify({"guidance":Guidance,"emotion_to_show":emotion_to_show})
    except Exception as e:
        app.logger.error('Error processing request: %s', str(e))
        return jsonify({'error':str(e)}), 400
    



@app.route('/analyzechat', methods=['GET'])
async def get_chat_report():
    try:
        # get chat id
        chatId = request.args.get('chatId')
        
        # call hume
        chatData = get_chat_data(chatId)
        app.logger.info(d == chatData[0].json["data"]["events_page"])
        app.logger.info(type(chatData[0].json["data"]["events_page"]))


        # process all chat data here
        
        interruptions, confidence_score, Talk_Listen_Ratio, objections, qualifications = await getPreliminaryReport(chatData=chatData[0].json)
        
        
        # prepare the report data as a dictionary
        ReportData = {
            #"emotions_user": emotions_user,  
            #"emotions_agent": emotions_agent,  
            "interruptions": "No interruptions detected!",
            "confidence": confidence_score,
            "Talk Listen Ratio": Talk_Listen_Ratio,
            "objections": objections,
            "qualifications": qualifications
        }
    
        return (ReportData),200
        # return processed data for report
        #return jsonify({"message":"dummy"}), 200
    except Exception as e:
        app.logger.error('Error processing request from flask call: %s', str(e))
        return jsonify({'error here 2': str(e)}), 400

"""
@app.route('/analyzechat', methods=['GET'])
def get_chat_report():
    try:
        # get chat id
        chatId = request.args.get('chatId')
        #print("chatId.  = " + str(chatId))
        #logging.info(f"chatId: {chatId}")

        # call hume
        chatData = get_chat_data(chatId)
        #logging.info(f"chatData final: {chatData}")
        # process data here
        #print(chatData)


        #process all chat data here

        emotions_agent, emotions_user, interruptions, confidence_score, Talk_Listen_Ratio, objections, qualifications = getPreliminaryReport(chatData=chatData)
        app.logger("confidence score \n\n\n")
        app.logger(str(confidence_score))
        #reportData = jsonify(getReportDataFromHumeEVI(chatData))
        ReportData = {
            "emotions_user":emotions_agent,
            "emotions_agent":emotions_user,
            "interruptions":interruptions,
            "confidence":confidence_score,
            "Talk Listen Ratio": Talk_Listen_Ratio,
            "objections":objections,
            "qualifications":qualifications

        }
        # then return processed data for report
        return jsonify({"message":"hello"}), 200
    except Exception as e:
        app.logger.error('Error processing request from flask call: %s', str(e))
        return jsonify({'error processing request from flask call':str(e)}), 400
"""



@app.route('/analyze', methods=['GET'])
def get_account_report():
    try:
        # get chat id
        chatId = request.args.get('chatId')
        print("chatId.  = " + str(chatId))
        logging.info(f"chatId: {chatId}")

        # call hume
        chatData = get_all_chats(chatId)
        logging.info(f"chatData final: {chatData}")
        # process data here


        print(chatData)
        return jsonify(str(chatData)), 200
    except Exception as e:
        app.logger.error('Error processing request: %s', str(e))
        return jsonify({'error':str(e)}), 400
    



def get_chat_data(chatId):
# URL of the API you want to send a GET request to
    api_url = 'https://api.hume.ai/v0/evi/chats/' + str(chatId) 
    
    # add multiple page handler
    params = {
        'page_number': 0,  # Example parameter, replace with your actual parameters
        'page_size': 100           # Another example parameter
    }
    headers = {
        "X-Hume-Api-Key":"QAmS4Qs8QGG4fbyWRG8L8xIvbZDRL6CXRuF0lE2AdQ1jtfqQ"
    }
    

    try:
        # Send the GET request
        response = requests.get(api_url, params=params, headers=headers)
        #logging.info(f"response from inner func: {response}")

        # Check if the request was successful
        if response.status_code == 200:
            # Get the JSON response data
            data = response.json()
            app.logger.info(type(data))
            #logging.info(f"response from inner func 2 after .json call: {data}")
            return jsonify({'data': data}), 200
        else:
            # Handle errors
            return jsonify({'status': 'error', 'message': 'Failed to fetch data'}), response.status_code
    
    except requests.exceptions.RequestException as e:
        # Handle network errors
        return jsonify({'status': 'error', 'message': str(e)}), 500


def get_all_chats(chatId):
    # URL of the API you want to send a GET request to
    api_url = 'https://api.hume.ai/v0/evi/chats' 
    
    # add multiple page handler
    params = {
        'page_number': 0,  # Example parameter, replace with your actual parameters
        'page_size': 100           # Another example parameter
    }
    headers = {
        "X-Hume-Api-Key":"QAmS4Qs8QGG4fbyWRG8L8xIvbZDRL6CXRuF0lE2AdQ1jtfqQ"
    }
    

    try:
        # Send the GET request
        response = requests.get(api_url, params=params, headers=headers)
        logging.info(f"response from inner func: {response}")

        # Check if the request was successful
        if response.status_code == 200:
            # Get the JSON response data
            data = response.json()
            logging.info(f"response from inner func 2 after .json call: {data}")
            return jsonify({'status': 'success', 'data': data}), 200
        else:
            # Handle errors
            return jsonify({'status': 'error', 'message': 'Failed to fetch data'}), response.status_code
    
    except requests.exceptions.RequestException as e:
        # Handle network errors
        return jsonify({'status': 'error', 'message': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080,debug=True)
    