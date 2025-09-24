import React, { useState } from "react";

export default function IdeaGenerator() {
  const [domain, setDomain] = useState("");
  const [keywords, setKeywords] = useState("");
  const [style, setStyle] = useState("creative");
  const [idea, setIdea] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleGenerate(e) {
    e.preventDefault();
    setLoading(true);
    setError("");
    setIdea("");

    try {
      const response = await fetch("http://localhost:8000/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ domain, keywords, style }),
      });
      const data = await response.json();
      if (response.ok) {
        setIdea(data.idea);
      } else {
        setError(data.detail || "Failed to generate idea");
      }
    } catch (err) {
      setError("Network error: " + err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="max-w-xl mx-auto p-6 bg-white rounded shadow-lg">
      <h2 className="text-2xl font-semibold mb-6 text-center">CreativeFuse Idea Generator</h2>
      <form onSubmit={handleGenerate} className="space-y-5">
        <div>
          <label htmlFor="domain" className="block mb-1 font-medium">Domain</label>
          <input
            id="domain"
            type="text"
            value={domain}
            onChange={(e) => setDomain(e.target.value)}
            required
            className="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-600"
            placeholder="e.g., healthcare, education"
          />
        </div>

        <div>
          <label htmlFor="keywords" className="block mb-1 font-medium">Keywords (optional)</label>
          <input
            id="keywords"
            type="text"
            value={keywords}
            onChange={(e) => setKeywords(e.target.value)}
            className="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-600"
            placeholder="e.g., AI, blockchain"
          />
        </div>

        <div>
          <label htmlFor="style" className="block mb-1 font-medium">Style</label>
          <select
            id="style"
            value={style}
            onChange={(e) => setStyle(e.target.value)}
            className="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-600"
          >
            <option value="creative">Creative</option>
            <option value="professional">Professional</option>
            <option value="playful">Playful</option>
          </select>
        </div>

        <button
          type="submit"
          disabled={loading}
          className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 rounded transition"
        >
          {loading ? "Generating..." : "Generate Idea"}
        </button>
      </form>

      {idea && (
        <div className="mt-8 bg-gray-100 p-4 rounded">
          <h3 className="text-xl font-semibold mb-2">Generated Idea</h3>
          <p className="whitespace-pre-line">{idea}</p>
        </div>
      )}

      {error && <p className="mt-4 text-red-600 font-bold">{error}</p>}
    </div>
  );
}
