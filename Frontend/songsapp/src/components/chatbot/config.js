import { createChatBotMessage } from 'react-chatbot-kit';

const config = {
  initialMessages: [
    createChatBotMessage("Hello! How can I assist you today? You can ask for song recommendations by song ID."),
  ],
};

export default config;
