import React from "react";
import IdeaGenerator from "./components/IdeaGenerator";

function App() {
  return (
    <div className="h-screen w-screen overflow-hidden bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      {/* Header */}
      <header className="h-16 bg-black/20 backdrop-blur-lg border-b border-white/10 flex items-center justify-between px-6">
        <div className="flex items-center space-x-3">
          <div className="w-8 h-8 bg-gradient-to-r from-purple-400 to-pink-400 rounded-lg flex items-center justify-center">
            <span className="text-white font-bold text-sm">CF</span>
          </div>
          <h1 className="text-2xl font-bold bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent">
            CreativeFuse
          </h1>
        </div>
      </header>

      {/* Main Content */}
      <main className="h-[calc(100vh-4rem)]">
        <IdeaGenerator />
      </main>
    </div>
  );
}

export default App;