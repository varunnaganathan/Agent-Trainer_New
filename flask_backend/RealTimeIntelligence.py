import os

All_emotions = {'Admiration': 0, 'Adoration': 0, 'Aesthetic Appreciation': 0, 'Amusement': 0, 'Anger': 0, 'Anxiety': 0, 'Awe': 0, 'Awkwardness': 0, 'Boredom': 0, 'Calmness': 0, 'Concentration': 0, 'Confusion': 0, 'Contemplation': 0, 'Contempt': 0, 'Contentment': 0, 'Craving': 0, 'Desire': 0, 'Determination': 0, 'Disappointment': 0, 'Disgust': 0, 'Distress': 0, 'Doubt': 0, 'Ecstasy': 0, 'Embarrassment': 0, 'Empathic Pain': 0, 'Entrancement': 0, 'Envy': 0, 'Excitement': 0, 'Fear': 0, 'Guilt': 0, 'Horror': 0, 'Interest': 0, 'Joy': 0, 'Love': 0, 'Nostalgia': 0, 'Pain': 0, 'Pride': 0, 'Realization': 0, 'Relief': 0, 'Romance': 0, 'Sadness': 0, 'Satisfaction': 0, 'Shame': 0, 'Surprise (negative)': 0, 'Surprise (positive)': 0, 'Sympathy': 0, 'Tiredness': 0, 'Triumph': 0}
Confidence_emotions = ["Calmness","Concentration","Determination","Interest","Triumph"]
Negative_emotions = ["Anger","Anxiety","Boredom","confusion","Contemplation","Contempt","Disappointment","Disgust","Distress","Doubt","Fear","Pain","Surprise (negative)","Tiredness"]
Positive_emotions = set(All_emotions.keys()).difference(set(Negative_emotions))


# find avg emotion for last 3 segments
def get_avg_top3_emotion(segments, topk = 3):
    Emotions = All_emotions.copy()
    for segment in segments:
        Emotions  = {key: Emotions[key] + segment[key] for key in Emotions}
    Emotions = dict(sorted(Emotions.items(), key=lambda item: item[1],reverse=True))
    return dict(list(Emotions.items())[:3])

def get_User_Agent_Emotion_Map():

    return {
    'Admiration': 'Contentment',
    'Adoration': 'Joy',
    'Aesthetic Appreciation': 'Contentment',
    'Amusement': 'Amusement',
    'Anger': 'Calmness',
    'Anxiety': 'Calmness',
    'Awe': 'Awe',
    'Awkwardness': 'Calmness',
    'Boredom': 'Interest',
    'Calmness': 'Calmness',
    'Concentration': 'Interest',
    'Confusion': 'Concentration',
    'Contemplation': 'Contemplation',
    'Contempt': 'Calmness',
    'Contentment': 'Contentment',
    'Craving': 'Excitement',
    'Desire': 'Determination',
    'Determination': 'Determination',
    'Disappointment': 'Sympathy',
    'Disgust': 'Calmness',
    'Distress': 'Sympathy',
    'Doubt': 'Calmness',
    'Ecstasy': 'Excitement',
    'Embarrassment': 'Calmness',
    'Empathic Pain': 'Sympathy',
    'Entrancement': 'Interest',
    'Envy': 'Contentment',
    'Excitement': 'Excitement',
    'Fear': 'Calmness',
    'Guilt': 'Sympathy',
    'Horror': 'Calmness',
    'Interest': 'Interest',
    'Joy': 'Joy',
    'Love': 'Contentment',
    'Nostalgia': 'Contentment',
    'Pain': 'Sympathy',
    'Pride': 'Admiration',
    'Realization': 'Interest',
    'Relief': 'Contentment',
    'Romance': 'Contentment',
    'Sadness': 'Sympathy',
    'Satisfaction': 'Contentment',
    'Shame': 'Calmness',
    'Surprise (negative)': 'Calmness',
    'Surprise (positive)': 'Excitement',
    'Sympathy': 'Sympathy',
    'Tiredness': 'Calmness',
    'Triumph': 'Admiration'
    }

# replace this with intelligence based insights
def get_agent_emotion_guidance_map():
    return  {
    'Admiration': "Acknowledge the customer's achievement or point of pride. Highlight how your product can further support or enhance their success.",
    'Amusement': 'Keep the tone light and positive. Use humor where appropriate to build rapport.',
    'Calmness': 'Steer the conversation calmly. Focus on providing logical solutions and reassurance.',
    'Contentment': "Reinforce the positive feelings by acknowledging the customer's satisfaction. Explore opportunities to deepen their engagement with your product.",
    'Concentration': 'Encourage the customer to focus on the benefits and specifics of your offering. Provide detailed information or data to support your points.',
    'Contemplation': 'Invite the customer to think more deeply about their needs and how your product aligns with them. Ask open-ended questions to stimulate further reflection.',
    'Determination': "Recognize the customer's resolve. Align your pitch with their goals, showing how your product can help them achieve their objectives.",
    'Excitement': "Build on the customer's energy. Highlight key benefits and success stories to keep the momentum going.",
    'Sympathy': "Show understanding and care. Offer solutions that are empathetic to the customer's situation.",
    'Interest': "Dig deeper into the current topic. Ask questions to uncover more about the customer's needs and tailor your pitch accordingly.",
    'Joy': 'Celebrate the positive moment with the customer. Reinforce how your product contributes to their happiness or success.',
    'Awe': 'Emphasize the impressive aspects of your product. Inspire the customer by showing how it can achieve extraordinary results.',
    'Contempt': 'Address any negative feelings with understanding. Gently steer the conversation back to positive aspects or offer alternatives.',
    'Embarrassment': 'Be supportive and non-judgmental. Provide reassurance and steer the conversation to a more comfortable topic.',
    'Relief': "Confirm that the customer's concerns have been addressed. Provide assurance and reinforce the solution offered.",
    'Surprise (negative)': 'Calmly address any unexpected concerns. Offer clarity and reassurance to mitigate any doubts.',
    'Surprise (positive)': 'Encourage the positive reaction. Build on it by highlighting further benefits or advantages of your product.',
    'Tiredness': 'Keep the conversation focused and efficient. Provide clear, concise information, and avoid overwhelming the customer with details.',
    'Triumph': "Celebrate the customer's success. Show how your product can continue to support their winning strategy."
    }

