import React from 'react';

const MessageParser = ({ children, actions }) => {
  const parse = (message) => {
    if (message.includes('hello')) {
      actions.handleHello();
    } else if (message.includes('recommend')) {
      actions.handleChatbotQuery(message);  // Trigger chatbot query for recommendation
    } else {
      actions.handleChatbotQuery(message);  // Handle other queries using the same method
    }
  };

  return (
    <div>
      {React.Children.map(children, (child) => {
        return React.cloneElement(child, {
          parse: parse,
          actions,
        });
      })}
    </div>
  );
};

export default MessageParser;
