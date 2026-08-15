"use client";
import { useState } from "react";
import DashboardLayout from "../dashboard/layout";
import { apiFetch } from "../../lib/api";

export default function MLModelsPage() {
  const [inputText, setInputText] = useState("");
  const [prediction, setPrediction] = useState("--");
  const [isLoading, setIsLoading] = useState(false);

  const handleInference = async () => {
    if (!inputText.trim()) return;
    setIsLoading(true);
    setPrediction("...");
    
    try {
      const res = await apiFetch("/ml/predict", {
        method: "POST",
        body: JSON.stringify({ text: inputText }),
      });
      
      if (res.ok) {
        const data = await res.json();
        setPrediction(data.category);
      } else {
        setPrediction("Error");
      }
    } catch (err) {
      console.error(err);
      setPrediction("Error");
    } finally {
      setIsLoading(false);
    }
  };
  return (
    <DashboardLayout>
      <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-700">
        <div>
          <h1 className="text-3xl font-semibold tracking-tight">Machine Learning Models</h1>
          <p className="text-gray-400 mt-1">Manage, monitor, and deploy custom ML models tracked via MLflow.</p>
        </div>

        {/* Model List */}
        <div className="bg-[#111] border border-gray-800 rounded-xl overflow-hidden">
          <div className="p-6 border-b border-gray-800 flex justify-between items-center">
            <h2 className="text-xl font-medium">Registered Models</h2>
            <button className="px-4 py-2 bg-blue-600 text-white rounded-md text-sm font-medium hover:bg-blue-700 transition-colors">
              Train New Model
            </button>
          </div>
          <table className="w-full text-left text-sm text-gray-400">
            <thead className="bg-[#1a1a1a] text-gray-300">
              <tr>
                <th className="px-6 py-4 font-medium">Model Name</th>
                <th className="px-6 py-4 font-medium">Architecture</th>
                <th className="px-6 py-4 font-medium">Accuracy</th>
                <th className="px-6 py-4 font-medium">Status</th>
                <th className="px-6 py-4 font-medium">Last Trained</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-800">
              <tr className="hover:bg-[#1a1a1a] transition-colors">
                <td className="px-6 py-4 font-medium text-white">Document Classifier</td>
                <td className="px-6 py-4">Logistic Regression + TF-IDF</td>
                <td className="px-6 py-4 text-green-400">87.5%</td>
                <td className="px-6 py-4">
                  <span className="px-2 py-1 rounded-full bg-green-500/10 text-green-400 border border-green-500/20 text-xs flex items-center w-fit gap-1.5">
                    <div className="w-1.5 h-1.5 rounded-full bg-green-400 animate-pulse" />
                    Active
                  </span>
                </td>
                <td className="px-6 py-4">2026-08-15</td>
              </tr>
            </tbody>
          </table>
        </div>

        {/* Quick Test Prediction */}
        <div className="bg-[#111] border border-gray-800 rounded-xl p-6 space-y-4">
          <h2 className="text-xl font-medium">Test Document Classifier</h2>
          <div className="flex gap-4">
            <textarea 
              className="flex-1 bg-gray-900 border border-gray-700 rounded-xl p-4 text-white focus:outline-none focus:border-blue-500 transition-colors resize-none"
              placeholder="Paste document text here to test classification..."
              rows={4}
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
            />
            <div className="w-64 bg-gray-900 border border-gray-700 rounded-xl p-4 flex flex-col justify-between">
              <div>
                <p className="text-xs text-gray-500 font-medium uppercase tracking-wider mb-1">Prediction</p>
                <p className="text-2xl font-bold text-gray-300">{prediction}</p>
              </div>
              <button 
                onClick={handleInference}
                disabled={isLoading || !inputText.trim()}
                className="w-full py-2 bg-white text-black font-medium rounded-lg hover:bg-gray-200 transition-colors disabled:opacity-50"
              >
                {isLoading ? "Running..." : "Run Inference"}
              </button>
            </div>
          </div>
        </div>

      </div>
    </DashboardLayout>
  );
}
