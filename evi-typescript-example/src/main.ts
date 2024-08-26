import {
  Hume,
  HumeClient,
  convertBlobToBase64,
  convertBase64ToBlob,
  ensureSingleValidAudioTrack,
  getAudioStream,
  getBrowserSupportedMimeType,
  MimeType,
} from 'hume';

import './styles.css';
import OpenAI from "openai";



// code for realtime ui


// Example: Updating the suggestions tab with new data
function updateSuggestionsTab(emotion: string, talkingPoints: string[], emotionalCues: string[]) {
  // Update the emotional state
  const currentEmotionElement = document.getElementById('currentEmotion');
  if (currentEmotionElement) {
    currentEmotionElement.textContent = emotion;
  }

  // Update the talking points
  const talkingPointsListElement = document.getElementById('talkingPointsList');
  if (talkingPointsListElement) {
    talkingPointsListElement.innerHTML = ''; // Clear existing points
    talkingPoints.forEach(point => {
      const listItem = document.createElement('li');
      listItem.textContent = point;
      talkingPointsListElement.appendChild(listItem);
    });
  }

  // Update the emotional cues
  const emotionalCuesListElement = document.getElementById('emotionalCuesList');
  if (emotionalCuesListElement) {
    emotionalCuesListElement.innerHTML = ''; // Clear existing cues
    emotionalCues.forEach(cue => {
      const listItem = document.createElement('li');
      listItem.textContent = cue;
      emotionalCuesListElement.appendChild(listItem);
    });
  }
}

// Example of how to use this function







// till here











(async () => {
  const startBtn = document.querySelector<HTMLButtonElement>('button#start-btn');
  const stopBtn = document.querySelector<HTMLButtonElement>('button#stop-btn');
  const chat = document.querySelector<HTMLDivElement>('div#chat');

  startBtn?.addEventListener('click', connect);
  stopBtn?.addEventListener('click', disconnect);

  /**
   * the Hume Client, includes methods for connecting to EVI and managing the Web Socket connection
   */
  let client: HumeClient | null = null;

  /**
   * the WebSocket instance
   */
  let socket: Hume.empathicVoice.chat.ChatSocket | null = null;

  /**
   * flag which denotes the intended state of the WebSocket
   */
  let connected = false;

  /**
   * the recorder responsible for recording the audio stream to be prepared as the audio input
   */
  let recorder: MediaRecorder | null = null;

  /**
   * the stream of audio captured from the user's microphone
   */
  let audioStream: MediaStream | null = null;

  /**
   * the current audio element to be played
   */
  let currentAudio: HTMLAudioElement | null = null;

  /**
   * flag which denotes whether audio is currently playing or not
   */
  let isPlaying = false;

  /**
   * flag which denotes whether to utilize chat resumability (preserve context from one chat to the next)
   */
  let resumeChats = true;

  /**
   * The ChatGroup ID used to resume the chat if disconnected unexpectedly
   */
  let chatGroupId: string | undefined;
  let chatId: string | undefined;




  // report code

  interface ReportSection {
    title: string;
    content: string;
  }
  
  interface ReportData {
    sections: ReportSection[];
  }
  
  // Function to fetch report data
  const fetchReportData = async (reportId: string): Promise<ReportData> => {
    try {
      const response = await fetch(`/api/reports/${reportId}`);
      if (!response.ok) throw new Error('Failed to fetch report data');
      return response.json();
    } catch (error) {
      console.error('Error fetching report data:', error);
      throw error;
    }
  };


  // create dummy report data
  // Dummy data for testing
const dummyReportData: ReportData = {
  sections: [
    { title: 'Introduction', content: 'This is the introduction section of the report.' },
    { title: 'Summary', content: 'This section provides a summary of the findings.' },
    { title: 'Details', content: 'Here are the detailed observations and analysis.' },
    { title: 'Conclusion', content: 'This section includes the final conclusions and recommendations.' },
    { title: 'Appendices', content: 'Additional data and information can be found in the appendices.' },
  ],
};



  
  // Function to render the report
  const renderReport = (data: ReportData): void => {
    const container = document.getElementById('report-content');
    if (!container) return;
  
    container.innerHTML = ''; // Clear existing content
  
    data.sections.forEach((section) => {
      const sectionElement = document.createElement('div');
      sectionElement.className = 'report-section';
      sectionElement.innerHTML = `
        <h2>${section.title}</h2>
        <p>${section.content}</p>
      `;
      container.appendChild(sectionElement);
    });
  };

  


  // Function to handle report closing
const closeReportButton = document.getElementById('close-report-btn');
if (closeReportButton) {
  closeReportButton.addEventListener('click', () => {
    const reportContainer = document.getElementById('report-container');
    if (reportContainer) {
      reportContainer.style.display = 'none'; // Hide the report
    }
  });
}
  // till here





  //
  // Call the function
  const callLocalhost = async () => {
    try {
        const res = await fetch('http://localhost:8080/analyze?chatId="ddd"', {
            method: 'GET', // or 'GET' if you're making a GET request
            headers: {
                'Content-Type': 'application/json',
            },
          
        });
        console.log('Result:',res)
        const result = await res.json();
        console.log('Result:', result);
    } catch (error) {
        console.error('Error during API call:', error);
    }
};
await callLocalhost();






  //
  /**
   * audio playback queue
   */
  const audioQueue: Blob[] = [];


  /**
   * open ai messag object
   */

  
  const openAImessages  = [{"role": "system", "content": "You are helping sales agents with realtime advice and coaching during a call. You will be given an emotion and the converation till now and you need to send suggestions to the salesperson on how to tailor his tone, approach and pitch"},
  ];

  /**
   * mime type supported by the browser the application is running in
   */
  const mimeType: MimeType = (() => {
    const result = getBrowserSupportedMimeType();
    return result.success ? result.mimeType : MimeType.WEBM;
  })();

  /**
   * instantiates interface config and client, sets up Web Socket handlers, and establishes secure Web Socket connection
   */
  async function connect(): Promise<void> {
    // instantiate the HumeClient with credentials to make authenticated requests
    if (!client) {
      client = new HumeClient({
        apiKey: import.meta.env.VITE_HUME_API_KEY || '',
        secretKey: import.meta.env.VITE_HUME_SECRET_KEY || '',
      });

  
    }

    // instantiates WebSocket and establishes an authenticated connection
    socket = await client.empathicVoice.chat.connect({
      configId: import.meta.env.VITE_HUME_CONFIG_ID || null,
      resumedChatGroupId: chatGroupId,
    });

    socket.on('open', handleWebSocketOpenEvent);
    socket.on('message', handleWebSocketMessageEvent);
    socket.on('error', handleWebSocketErrorEvent);
    socket.on('close', handleWebSocketCloseEvent);

    // update ui state
    toggleBtnStates();
  }

  /**
   * stops audio capture and playback, and closes the Web Socket connection
   */
  async function disconnect(): Promise<void> {
    // update ui state
    toggleBtnStates();

    // stop audio playback
    stopAudio();

    // stop audio capture
    recorder?.stop();
    recorder = null;
    audioStream = null;

    // set connected state to false to prevent automatic reconnect
    connected = false;

    // IF resumeChats flag is false, reset chatGroupId so a new conversation is started when reconnecting
    if (!resumeChats) {
      chatGroupId = undefined;
    }

    // closed the Web Socket connection
    socket?.close();

    // code for report data -------------------------------------------------------------------------------------


    const reportId = '123'; // Replace with actual report ID or logic to determine ID
  try {
    //const reportData = await fetchReportData(reportId);
    //renderReport(reportData);
    renderReport(dummyReportData);
    
    const reportContainer = document.getElementById('report-container');
    if (reportContainer) {
      reportContainer.style.display = 'block'; // Show the report
    }
  } catch (error) {
    console.error('Error handling stop call:', error);
  }








  }



  async function getDataWithParams(chatId:string) {
    // Define your base URL and parameters
    const baseUrl = 'http://localhost:8080/analyze';
    const params = new URLSearchParams({
        
        chatId: chatId,
    }).toString();

    // Construct the full URL with query parameters
    const url = `${baseUrl}?${params}`;
    
    try {
        // Send GET request
        const response = await fetch(url, {
            method: 'GET', // Method is GET by default, but it's good practice to include it
            
        });

        // Check if response is ok
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        // Parse JSON response
        const data = await response.json();

        // Handle the data
        console.log('Response data:', data);
    } catch (error) {
        console.error('Error fetching data:', error);
    }
}




  /**
   * captures and records audio stream, and sends audio stream through the socket
   *
   * API Reference:
   * - `audio_input`: https://dev.hume.ai/reference/empathic-voice-interface-evi/chat/chat#send.Audio%20Input.type
   */
  async function captureAudio(): Promise<void> {
    audioStream = await getAudioStream();
    // ensure there is only one audio track in the stream
    ensureSingleValidAudioTrack(audioStream);

    // instantiate the media recorder
    recorder = new MediaRecorder(audioStream, { mimeType });

    // callback for when recorded chunk is available to be processed
    recorder.ondataavailable = async ({ data }) => {
      // IF size of data is smaller than 1 byte then do nothing
      if (data.size < 1) return;

      // base64 encode audio data
      const encodedAudioData = await convertBlobToBase64(data);

      // define the audio_input message JSON
      const audioInput: Omit<Hume.empathicVoice.AudioInput, 'type'> = {
        data: encodedAudioData,
      };

      // send audio_input message
      socket?.sendAudioInput(audioInput);
    };

    // capture audio input at a rate of 100ms (recommended)
    const timeSlice = 100;
    recorder.start(timeSlice);
  }

  /**
   * play the audio within the playback queue, converting each Blob into playable HTMLAudioElements
   */
  function playAudio(): void {
    // IF there is nothing in the audioQueue OR audio is currently playing then do nothing
    if (!audioQueue.length || isPlaying) return;

    // update isPlaying state
    isPlaying = true;

    // pull next audio output from the queue
    const audioBlob = audioQueue.shift();

    // IF audioBlob is unexpectedly undefined then do nothing
    if (!audioBlob) return;

    // converts Blob to AudioElement for playback
    const audioUrl = URL.createObjectURL(audioBlob);
    currentAudio = new Audio(audioUrl);

    // play audio
    currentAudio.play();

    // callback for when audio finishes playing
    currentAudio.onended = () => {
      // update isPlaying state
      isPlaying = false;

      // attempt to pull next audio output from queue
      if (audioQueue.length) playAudio();
    };
  }

  /**
   * stops audio playback, clears audio playback queue, and updates audio playback state
   */
  function stopAudio(): void {
    // stop the audio playback
    currentAudio?.pause();
    currentAudio = null;

    // update audio playback state
    isPlaying = false;

    // clear the audioQueue
    audioQueue.length = 0;
  }

  /**
   * callback function to handle a WebSocket opened event
   */
  async function handleWebSocketOpenEvent(): Promise<void> {
    /* place logic here which you would like invoked when the socket opens */
    console.log('Web socket connection opened');

    // ensures socket will reconnect if disconnected unintentionally
    connected = true;

    await captureAudio();
  }

  /**
   * callback function to handle a WebSocket message event
   *
   * API Reference:
   * - `user_message`: https://dev.hume.ai/reference/empathic-voice-interface-evi/chat/chat#receive.User%20Message.type
   * - `assistant_message`: https://dev.hume.ai/reference/empathic-voice-interface-evi/chat/chat#receive.Assistant%20Message.type
   * - `audio_output`: https://dev.hume.ai/reference/empathic-voice-interface-evi/chat/chat#receive.Audio%20Output.type
   * - `user_interruption`: https://dev.hume.ai/reference/empathic-voice-interface-evi/chat/chat#receive.User%20Interruption.type
   */
  async function handleWebSocketMessageEvent(
    message: Hume.empathicVoice.SubscribeEvent
  ): Promise<void> {




    /* place logic here which you would like to invoke when receiving a message through the socket */

    // handle messages received through the WebSocket (messages are distinguished by their "type" field.)
    switch (message.type) {
      // save chat_group_id to resume chat if disconnected
      case 'chat_metadata':
        chatGroupId = message.chatGroupId;
        chatId = message.chatId;
        break;

      // append user and assistant messages to UI for chat visibility
      case 'user_message':
        //openAImessages.push({role:"user",content:message.message.toString()});
        //break;

      case 'assistant_message':
        const { role, content } = message.message;
        const topThreeEmotions = extractTopThreeEmotions(message);
        appendMessage(role, content ?? '', topThreeEmotions);
        

        // append open ai message
        openAImessages.push({role:"assistant",content:message.message.toString()});
        
        const suggestions = await fetchSuggestions();
        updateSuggestionsList(suggestions);
        updateSuggestionsTab('Happy', [message.message.content?message.message.content:""], ['Show enthusiasm', 'Offer a compliment']);

        
        
        break;

      // add received audio to the playback queue, and play next audio output
      case 'audio_output':
        // convert base64 encoded audio to a Blob
        const audioOutput = message.data;
        const blob = convertBase64ToBlob(audioOutput, mimeType);

        // add audio Blob to audioQueue
        audioQueue.push(blob);

        // play the next audio output
        if (audioQueue.length >= 1) playAudio();
        break;

      // stop audio playback, clear audio playback queue, and update audio playback state on interrupt
      case 'user_interruption':
        stopAudio();
        break;
    }



    // fetch open ai response here
    /*
    const completion = await openai.chat.completions.create({
      messages:[],//openAImessages,
      model: "gpt-4o-mini",
    });
    */




    



    
    // added
    /*
    setInterval(async () => {
      const suggestions = await fetchSuggestions(message.message, extractTopThreeEmotions(message));
      updateSuggestionsList(suggestions);
    }, 5000); // Refresh suggestions every 5 seconds
    */
  }

  /**
   * callback function to handle a WebSocket error event
   */
  function handleWebSocketErrorEvent(error: Error): void {
    /* place logic here which you would like invoked when receiving an error through the socket */
    console.error(error);
  }

  /**
   * callback function to handle a WebSocket closed event
   */
  async function handleWebSocketCloseEvent(): Promise<void> {
    /* place logic here which you would like invoked when the socket closes */

    // reconnect to the socket if disconnect was unintentional
    if (connected) await connect();

    console.log('Web socket connection closed');
  }

  /**
   * adds message to Chat in the webpage's UI
   *
   * @param role the speaker associated with the audio transcription
   * @param content transcript of the audio
   * @param topThreeEmotions the top three emotion prediction scores for the message
   */
  function appendMessage(
    role: Hume.empathicVoice.Role,
    content: string,
    topThreeEmotions: { emotion: string; score: any }[]
  ): void {
    // generate chat card component with message content and emotion scores
    const chatCard = new ChatCard({
      role,
      timestamp: new Date().toLocaleTimeString(),
      content,
      scores: topThreeEmotions,
    });

    // append chat card to the UI
    chat?.appendChild(chatCard.render());

    // scroll to the bottom to view most recently added message
    if (chat) chat.scrollTop = chat.scrollHeight;
  }

  /**
   * toggles `start` and `stop` buttons' disabled states
   */
  function toggleBtnStates(): void {
    if (startBtn) startBtn.disabled = !startBtn.disabled;
    if (stopBtn) stopBtn.disabled = !stopBtn.disabled;
  }

  /**
   * takes a received `user_message` or `assistant_message` and extracts the top 3 emotions from the
   * predicted expression measurement scores.
   */
  function extractTopThreeEmotions(
    message: Hume.empathicVoice.UserMessage | Hume.empathicVoice.AssistantMessage
  ): { emotion: string; score: string }[] {
    // extract emotion scores from the message
    const scores = message.models.prosody?.scores;

    // convert the emotions object into an array of key-value pairs
    const scoresArray = Object.entries(scores || {});

    // sort the array by the values in descending order
    scoresArray.sort((a, b) => b[1] - a[1]);

    // extract the top three emotions and convert them back to an object
    const topThreeEmotions = scoresArray.slice(0, 3).map(([emotion, score]) => ({
      emotion,
      score: (Math.round(Number(score) * 100) / 100).toFixed(2),
    }));

    return topThreeEmotions;
  }
})();

/**
 * The code below does not pertain to the EVI implementation, and only serves to style the UI.
 */

interface Score {
  emotion: string;
  score: string;
}

interface ChatMessage {
  role: Hume.empathicVoice.Role;
  timestamp: string;
  content: string;
  scores: Score[];
}

class ChatCard {
  private message: ChatMessage;

  constructor(message: ChatMessage) {
    this.message = message;
  }

  private createScoreItem(score: Score): HTMLElement {
    const scoreItem = document.createElement('div');
    scoreItem.className = 'score-item';
    scoreItem.innerHTML = `${score.emotion}: <strong>${score.score}</strong>`;
    return scoreItem;
  }

  public render(): HTMLElement {
    const card = document.createElement('div');
    card.className = `chat-card ${this.message.role}`;

    const role = document.createElement('div');
    role.className = 'role';
    role.textContent =
      this.message.role.charAt(0).toUpperCase() + this.message.role.slice(1);

    const timestamp = document.createElement('div');
    timestamp.className = 'timestamp';
    timestamp.innerHTML = `<strong>${this.message.timestamp}</strong>`;

    const content = document.createElement('div');
    content.className = 'content';
    content.textContent = this.message.content;

    const scores = document.createElement('div');
    scores.className = 'scores';
    this.message.scores.forEach((score) => {
      scores.appendChild(this.createScoreItem(score));
    });

    card.appendChild(role);
    card.appendChild(timestamp);
    card.appendChild(content);
    card.appendChild(scores);

    return card;
  }
}



// newly added funcs

async function fetchSuggestions(): Promise<string[]> {
    

  try {
      const res = await fetch('http://localhost:8080/guidance?emotion=Calmness"', {
          method: 'GET', // or 'GET' if you're making a GET request
          headers: {
              'Content-Type': 'application/json',
          },
        
      });
      console.log('Result:',res)
      const result = await res.json();
      console.log('Result:', result);
      return [res.toString()];
  } catch (error) {
      console.error('Error during API call:', error);
  }
  return ["failed request suggestion"]
  


  /*
  const openai = new OpenAI({
     dangerouslyAllowBrowser:true,
  });
  
    const response = await openai.chat.completions.create({
      messages: [{"role": "system", "content": "You are helping sales agents with realtime advice and coaching during a call. You will be given an emotion and the converation till now and you need to send suggestions to the salesperson on how to tailor his tone, approach and pitch"},
          {"role": "user", "content": "Who won the world series in 2020?"},
          {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
          {"role": "user", "content": "Where was it played?"}],
      model: "gpt-4o-mini",
    });
  
    console.log(response.choices[0]);
  
  */


    /*
    const response = await fetch('https://your-api-endpoint.com/suggestions', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });
    */
   

}


function updateSuggestionsList(suggestions: string[]): void {
  const suggestionsList = document.querySelector<HTMLUListElement>('#suggestions-list');
  if (suggestionsList) {
    suggestionsList.innerHTML = ''; // Clear existing suggestions
    suggestions.forEach((suggestion) => {
      const listItem = document.createElement('li');
      listItem.textContent = suggestion;
      suggestionsList.appendChild(listItem);
    });
  }
}

