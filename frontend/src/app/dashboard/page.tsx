"use client";
import { useEffect, useState } from "react";
import DashboardLayout from "./layout";

type Analytics = {
  total_documents: number;
  documents_processed: number;
  total_chunks: number;
  rag_queries: number;
  sql_queries: number;
  ml_predictions: number;
};

export default function DashboardPage() {
  const [metrics, setMetrics] = useState<Analytics>({
    total_documents: 0,
    documents_processed: 0,
    total_chunks: 0,
    rag_queries: 0,
    sql_queries: 0,
    ml_predictions: 0,
  });

  useEffect(() => {
    // Fetch analytics using the new authenticated apiFetch
    apiFetch("/analytics/dashboard")
      .then(res => res.json())
      .then(data => {
        if(data && typeof data.total_documents !== 'undefined') {
          setMetrics(data);
        }
      })
      .catch(err => console.error("Failed to load analytics", err));
  }, []);

  return (
    <DashboardLayout>
      <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-700">
        
        {/* Header */}
        <div>
          <h1 className="text-3xl font-semibold tracking-tight text-white">Platform Overview</h1>
          <p className="text-gray-400 mt-1">Monitor your autonomous agents and document processing pipelines.</p>
        </div>

        {/* System Status Banner */}
        <div className="bg-green-500/10 border border-green-500/20 rounded-xl p-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-2.5 h-2.5 rounded-full bg-green-500 animate-pulse"></div>
            <span className="text-green-400 font-medium">All Systems Operational</span>
          </div>
          <div className="text-sm text-green-500/70">
            pgvector, MLflow, Redis, Celery
          </div>
        </div>

        {/* Metrics Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <MetricCard title="Total Documents" value={metrics.total_documents.toString()} subtitle={`${metrics.documents_processed} processed`} />
          <MetricCard title="Vector Chunks" value={metrics.total_chunks.toString()} subtitle="Stored in pgvector" />
          <MetricCard title="RAG / SQL Queries" value={(metrics.rag_queries + metrics.sql_queries).toString()} subtitle="Last 30 days" />
          <MetricCard title="ML Inferences" value={metrics.ml_predictions.toString()} subtitle="Document classification" />
        </div>

        {/* Recent Activity (Placeholder for visual polish) */}
        <div>
          <h2 className="text-xl font-medium mb-4 text-white">Recent Agent Activity</h2>
          <div className="bg-[#111] border border-gray-800 rounded-xl p-6 flex flex-col gap-4">
            <ActivityItem time="2 mins ago" text="SQL Agent executed query for Q3 Revenue." />
            <ActivityItem time="15 mins ago" text="Document 'Employee_Handbook.pdf' chunked and embedded." />
            <ActivityItem time="1 hour ago" text="ML Engine classified 'Invoice_102.png' as INVOICE." />
          </div>
        </div>

      </div>
    </DashboardLayout>
  );
}

function MetricCard({ title, value, subtitle }: { title: string; value: string; subtitle: string }) {
  return (
    <div className="bg-[#111] border border-gray-800 rounded-xl p-6 transition-all hover:border-gray-700 hover:shadow-lg hover:shadow-black/50">
      <h3 className="text-gray-400 text-sm font-medium">{title}</h3>
      <div className="mt-2 flex items-baseline gap-2">
        <span className="text-3xl font-bold text-white">{value}</span>
      </div>
      <p className="mt-1 text-sm text-gray-500">{subtitle}</p>
    </div>
  );
}

function ActivityItem({ time, text }: { time: string, text: string }) {
  return (
    <div className="flex items-start gap-4 pb-4 border-b border-gray-800 last:border-0 last:pb-0">
      <div className="w-24 text-xs text-gray-500 pt-1 flex-shrink-0">{time}</div>
      <div className="text-sm text-gray-300">{text}</div>
    </div>
  );
}
