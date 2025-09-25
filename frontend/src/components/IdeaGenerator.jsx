import React, { useState } from "react";

// Simple markdown renderer component
function MarkdownRenderer({ content }) {
  const renderMarkdown = (text) => {
    if (!text) return "";
    
    // Convert markdown to HTML-like structure
    let html = text
      // Headers
      .replace(/^### (.*$)/gim, '<h3>$1</h3>')
      .replace(/^## (.*$)/gim, '<h2>$1</h2>')
      .replace(/^# (.*$)/gim, '<h1>$1</h1>')
      // Bold
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      // Italic
      .replace(/\*(.*?)\*/g, '<em>$1</em>')
      // Code blocks
      .replace(/```([\s\S]*?)```/g, '<pre><code>$1</code></pre>')
      // Inline code
      .replace(/`(.*?)`/g, '<code>$1</code>')
      // Lists
      .replace(/^\- (.*$)/gim, '<li>$1</li>')
      .replace(/^(\d+)\. (.*$)/gim, '<li>$2</li>')
      // Line breaks
      .replace(/\n\n/g, '</p><p>')
      .replace(/\n/g, '<br/>');

    // Wrap in paragraph tags
    html = '<p>' + html + '</p>';
    
    // Clean up empty paragraphs
    html = html.replace(/<p><\/p>/g, '');
    
    // Wrap lists in ul tags
    html = html.replace(/(<li>.*<\/li>)/gs, '<ul>$1</ul>');
    
    return html;
  };

  return (
    <div 
      className="prose prose-lg max-w-none"
      dangerouslySetInnerHTML={{ __html: renderMarkdown(content) }}
      style={{
        lineHeight: '1.8',
        fontSize: '16px'
      }}
    />
  );
}

export default function IdeaGenerator() {
  const [ideaInput, setIdeaInput] = useState("");
  const [boostedIdea, setBoostedIdea] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleBoost() {
    if (!ideaInput.trim()) return;
    
    setLoading(true);
    setError("");
    setBoostedIdea("");

    try {
      const response = await fetch("http://localhost:8000/boost", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ idea: ideaInput }),
      });
      const data = await response.json();
      if (response.ok) {
        setBoostedIdea(data.boosted_idea);
      } else {
        setError(data.detail || "Failed to enhance idea");
      }
    } catch (err) {
      setError("Network error: " + err.message);
    } finally {
      setLoading(false);
    }
  }

  const clearAll = () => {
    setIdeaInput("");
    setBoostedIdea("");
    setError("");
  };

  return (
    <>
      <div className="h-full flex">
        {/* Left Panel - Input */}
        <div className="w-1/2 p-8 flex flex-col h-full">
          <div className="bg-white/5 backdrop-blur-lg rounded-2xl border border-white/10 flex-1 flex flex-col min-h-0 p-6">
            <div className="mb-6 flex justify-between items-start flex-shrink-0">
              <div>
                <h2 className="text-2xl font-semibold text-white mb-2">Share Your Idea</h2>
                <p className="text-white/60 text-sm">Describe your concept and watch it transform into something extraordinary</p>
              </div>
              <button
                onClick={clearAll}
                className="px-3 py-1.5 bg-white/10 hover:bg-white/20 rounded-lg text-white/70 hover:text-white transition-all duration-200 text-xs"
              >
                Clear
              </button>
            </div>

            <div className="flex-1 flex flex-col min-h-0">
              <div className="flex-1 mb-6 min-h-0">
                <textarea
                  value={ideaInput}
                  onChange={(e) => setIdeaInput(e.target.value)}
                  placeholder="✨ Describe your idea in detail... What's your vision? What problem does it solve? What makes it unique?"
                  className="w-full h-full bg-white/5 border border-white/20 rounded-xl px-4 py-4 text-white placeholder-white/40 focus:outline-none focus:ring-2 focus:ring-purple-400 focus:border-transparent resize-none backdrop-blur-sm scrollbar-thin scrollbar-thumb-white/20 scrollbar-track-transparent hover:scrollbar-thumb-white/30"
                />
              </div>

              <button
                onClick={handleBoost}
                disabled={loading || !ideaInput.trim()}
                className="w-full bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 disabled:from-gray-600 disabled:to-gray-600 text-white font-semibold py-4 rounded-xl transition-all duration-300 transform hover:scale-[1.02] disabled:scale-100 disabled:cursor-not-allowed shadow-lg flex-shrink-0"
              >
                {loading ? (
                  <div className="flex items-center justify-center space-x-2">
                    <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
                    <span>Enhancing Your Vision...</span>
                  </div>
                ) : (
                  "🚀 Boost My Idea"
                )}
              </button>
            </div>

            {error && (
              <div className="mt-4 p-4 bg-red-500/20 border border-red-500/30 rounded-xl text-red-200 flex-shrink-0">
                <span className="font-medium">Error:</span> {error}
              </div>
            )}
          </div>
        </div>

        {/* Right Panel - Enhanced Idea */}
        <div className="w-1/2 p-8 flex flex-col h-full">
          <div className="bg-white/5 backdrop-blur-lg rounded-2xl border border-white/10 flex-1 flex flex-col min-h-0">
            <div className="p-6 border-b border-white/10 flex-shrink-0">
              <h2 className="text-2xl font-semibold text-white mb-2">Enhanced Vision</h2>
              <p className="text-white/60 text-sm">Your idea, supercharged with actionable insights</p>
            </div>

            <div className="flex-1 min-h-0 relative">
              {boostedIdea ? (
                <div className="h-full overflow-y-auto p-6 scrollbar-thin scrollbar-thumb-white/20 scrollbar-track-transparent hover:scrollbar-thumb-white/30">
                  <div className="text-white/90 leading-relaxed">
                    <MarkdownRenderer content={boostedIdea} />
                  </div>
                </div>
              ) : (
                <div className="h-full flex items-center justify-center text-center p-6">
                  <div className="max-w-sm">
                    <div className="w-24 h-24 bg-gradient-to-r from-purple-400/20 to-pink-400/20 rounded-full flex items-center justify-center mx-auto mb-6">
                      <span className="text-4xl">💡</span>
                    </div>
                    <h3 className="text-xl font-semibold text-white mb-3">Ready to Transform</h3>
                    <p className="text-white/50 text-sm leading-relaxed">
                      Enter your idea on the left and watch as AI transforms it into a comprehensive, actionable plan with strategic insights and next steps.
                    </p>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>

      <style jsx>{`
        /* Custom scrollbar styles */
        .scrollbar-thin {
          scrollbar-width: thin;
        }
        
        .scrollbar-thin::-webkit-scrollbar {
          width: 6px;
        }
        
        .scrollbar-thin::-webkit-scrollbar-track {
          background: transparent;
        }
        
        .scrollbar-thumb-white\/20::-webkit-scrollbar-thumb {
          background-color: rgba(255, 255, 255, 0.2);
          border-radius: 3px;
        }
        
        .scrollbar-thin:hover::-webkit-scrollbar-thumb {
          background-color: rgba(255, 255, 255, 0.3);
        }

        /* Prose styles for markdown rendering */
        .prose h1 {
          font-size: 1.5rem;
          font-weight: bold;
          color: #f8fafc;
          margin: 1.5rem 0 1rem 0;
          padding-bottom: 0.5rem;
          border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }
        .prose h2 {
          font-size: 1.3rem;
          font-weight: 600;
          color: #f1f5f9;
          margin: 1.25rem 0 0.75rem 0;
        }
        .prose h3 {
          font-size: 1.1rem;
          font-weight: 600;
          color: #e2e8f0;
          margin: 1rem 0 0.5rem 0;
        }
        .prose p {
          margin: 1rem 0;
          line-height: 1.8;
        }
        .prose strong {
          font-weight: 600;
          color: #f8fafc;
        }
        .prose em {
          font-style: italic;
          color: #cbd5e1;
        }
        .prose ul {
          margin: 1rem 0;
          padding-left: 1.5rem;
        }
        .prose li {
          margin: 0.5rem 0;
          position: relative;
        }
        .prose li::before {
          content: "•";
          color: #a855f7;
          font-weight: bold;
          position: absolute;
          left: -1rem;
        }
        .prose code {
          background: rgba(255, 255, 255, 0.1);
          padding: 0.2rem 0.4rem;
          border-radius: 0.25rem;
          font-size: 0.9rem;
          color: #fbbf24;
        }
        .prose pre {
          background: rgba(0, 0, 0, 0.3);
          padding: 1rem;
          border-radius: 0.5rem;
          margin: 1rem 0;
          overflow-x: auto;
        }
        .prose pre code {
          background: none;
          padding: 0;
          color: #e2e8f0;
        }
      `}</style>
    </>
  );
}