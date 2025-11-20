'use client';

import { useState, useEffect, useRef } from 'react';
import { Card } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { Loading } from '@/components/ui/Loading';
import { api, getErrorMessage } from '@/lib/api';
import type { ChatConversation, ChatMessage, MetaAdAccount } from '@/lib/types';
import toast from 'react-hot-toast';

export default function ChatPage() {
  const [accounts, setAccounts] = useState<MetaAdAccount[]>([]);
  const [selectedAccount, setSelectedAccount] = useState<MetaAdAccount | null>(null);
  const [conversations, setConversations] = useState<ChatConversation[]>([]);
  const [currentConversation, setCurrentConversation] = useState<ChatConversation | null>(null);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [inputMessage, setInputMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [sending, setSending] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    loadAccounts();
  }, []);

  useEffect(() => {
    if (selectedAccount) {
      loadConversations();
    }
  }, [selectedAccount]);

  useEffect(() => {
    if (currentConversation) {
      loadMessages();
    }
  }, [currentConversation]);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const loadAccounts = async () => {
    try {
      const response = await api.getMetaAccounts();
      setAccounts(response.accounts);
      if (response.accounts.length > 0) {
        setSelectedAccount(response.accounts[0]);
      }
    } catch (error) {
      toast.error(getErrorMessage(error));
    }
  };

  const loadConversations = async () => {
    try {
      const response = await api.getConversations();
      setConversations(response.conversations);
    } catch (error) {
      toast.error(getErrorMessage(error));
    }
  };

  const loadMessages = async () => {
    if (!currentConversation) return;

    setLoading(true);
    try {
      const response = await api.getMessages(currentConversation.id);
      setMessages(response.conversation.messages || []);
    } catch (error) {
      toast.error(getErrorMessage(error));
    } finally {
      setLoading(false);
    }
  };

  const startNewConversation = async () => {
    if (!selectedAccount) {
      toast.error('Please select an account first');
      return;
    }

    try {
      const response = await api.createConversation(selectedAccount.id);
      setConversations([response.conversation, ...conversations]);
      setCurrentConversation(response.conversation);
      setMessages([]);
    } catch (error) {
      toast.error(getErrorMessage(error));
    }
  };

  const sendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputMessage.trim() || !currentConversation) return;

    setSending(true);
    const userMessage = inputMessage;
    setInputMessage('');

    try {
      const response = await api.sendMessage(currentConversation.id, userMessage);
      setMessages([...messages, response.user_message, response.assistant_message]);
    } catch (error) {
      toast.error(getErrorMessage(error));
      setInputMessage(userMessage); // Restore message on error
    } finally {
      setSending(false);
    }
  };

  if (!selectedAccount) {
    return (
      <div className="flex items-center justify-center h-full">
        <Card className="max-w-md text-center">
          <p className="text-gray-600">Please connect a Meta Ads account to use the chat feature.</p>
        </Card>
      </div>
    );
  }

  return (
    <div className="h-full flex gap-6">
      {/* Conversations Sidebar */}
      <div className="w-64 flex-shrink-0">
        <Card padding={false} className="h-full">
          <div className="p-4 border-b border-gray-200">
            <Button onClick={startNewConversation} className="w-full" size="sm">
              New Chat
            </Button>
          </div>
          <div className="overflow-y-auto" style={{ maxHeight: 'calc(100vh - 250px)' }}>
            {conversations.map((conv) => (
              <button
                key={conv.id}
                onClick={() => setCurrentConversation(conv)}
                className={`w-full p-4 text-left border-b border-gray-100 hover:bg-gray-50 ${
                  currentConversation?.id === conv.id ? 'bg-blue-50' : ''
                }`}
              >
                <div className="font-medium text-sm truncate">{conv.title}</div>
                <div className="text-xs text-gray-500">
                  {new Date(conv.updated_at).toLocaleDateString()}
                </div>
              </button>
            ))}
          </div>
        </Card>
      </div>

      {/* Chat Area */}
      <Card padding={false} className="flex-1 flex flex-col h-full">
        {currentConversation ? (
          <>
            {/* Messages */}
            <div className="flex-1 overflow-y-auto p-6 space-y-4">
              {loading ? (
                <div className="flex justify-center">
                  <Loading />
                </div>
              ) : messages.length === 0 ? (
                <div className="text-center text-gray-500 mt-12">
                  <p className="text-lg mb-2">Start a conversation</p>
                  <p className="text-sm">Ask questions about your ad performance!</p>
                </div>
              ) : (
                messages.map((message) => (
                  <div
                    key={message.id}
                    className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
                  >
                    <div
                      className={`max-w-2xl rounded-lg px-4 py-3 ${
                        message.role === 'user'
                          ? 'bg-blue-600 text-white'
                          : 'bg-gray-100 text-gray-900'
                      }`}
                    >
                      <p className="whitespace-pre-wrap">{message.content}</p>
                    </div>
                  </div>
                ))
              )}
              <div ref={messagesEndRef} />
            </div>

            {/* Input */}
            <form onSubmit={sendMessage} className="p-4 border-t border-gray-200">
              <div className="flex gap-2">
                <input
                  type="text"
                  value={inputMessage}
                  onChange={(e) => setInputMessage(e.target.value)}
                  placeholder="Ask about your ad performance..."
                  className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  disabled={sending}
                />
                <Button type="submit" isLoading={sending} disabled={!inputMessage.trim()}>
                  Send
                </Button>
              </div>
            </form>
          </>
        ) : (
          <div className="flex items-center justify-center h-full">
            <p className="text-gray-500">Select a conversation or start a new chat</p>
          </div>
        )}
      </Card>
    </div>
  );
}
