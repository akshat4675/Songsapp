"use client";
import React, { useState } from 'react';
import axios from 'axios';

const ActionProvider = ({ createChatBotMessage, setState, children }) => {
  const [loading, setLoading] = useState(false);

  const handleHello = () => {
    const botMessage = createChatBotMessage('Hello. Nice to meet you.');
    setState((prev) => ({
      ...prev,
      messages: [...prev.messages, botMessage],
    }));
  };

  const handleChatbotQuery = async (query) => {
    setLoading(true);
    try {
      const response = await axios.post('http://localhost:8000/chatbot', { query });
      const botMessage = createChatBotMessage(response.data.response);
      setState((prev) => ({
        ...prev,
        messages: [...prev.messages, botMessage],
      }));
    } catch (error) {
      const errorMessage = createChatBotMessage('Sorry, there was an error with the request.');
      setState((prev) => ({
        ...prev,
        messages: [...prev.messages, errorMessage],
      }));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      {React.Children.map(children, (child) => {
        return React.cloneElement(child, {
          actions: {
            handleHello,
            handleChatbotQuery,  // Adding the new action for chatbot queries
          },
          loading,
        });
      })}
    </div>
  );
};

export default ActionProvider;
