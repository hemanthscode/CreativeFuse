import React from "react";
import IdeaGenerator from "./components/IdeaGenerator";

function App() {
  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-blue-600 text-white py-6 text-center text-3xl font-bold">
        CreativeFuse
      </header>
      <main className="my-10 px-4">
        <IdeaGenerator />
      </main>
    </div>
  );
}

export default App;
