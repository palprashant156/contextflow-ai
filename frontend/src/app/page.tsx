import Link from "next/link";

export default function Home() {
  return (
    <div className="min-h-screen bg-black text-white flex flex-col items-center justify-center relative overflow-hidden">
      {/* Decorative background element */}
      <div className="absolute top-[-20%] left-[-10%] w-[500px] h-[500px] rounded-full bg-blue-600/20 blur-[120px] pointer-events-none" />
      <div className="absolute bottom-[-20%] right-[-10%] w-[500px] h-[500px] rounded-full bg-purple-600/20 blur-[120px] pointer-events-none" />

      <main className="z-10 flex flex-col items-center text-center px-4">
        <h1 className="text-5xl md:text-7xl font-bold tracking-tighter mb-6 bg-gradient-to-br from-white to-gray-400 bg-clip-text text-transparent">
          CortexFlow AI
        </h1>
        <p className="text-lg md:text-xl text-gray-400 max-w-2xl mb-10">
          Autonomous Knowledge & Decision Engine. Orchestrating RAG, Machine Learning, and SQL Agents for enterprise intelligence.
        </p>
        
        <div className="flex gap-4">
          <Link href="/dashboard" className="px-8 py-3 rounded-full bg-white text-black font-medium hover:bg-gray-200 transition-colors shadow-[0_0_20px_rgba(255,255,255,0.3)]">
            Enter Dashboard
          </Link>
          <Link href="/login" className="px-8 py-3 rounded-full bg-gray-900 border border-gray-700 text-white font-medium hover:bg-gray-800 transition-colors">
            Login
          </Link>
        </div>
      </main>
    </div>
  );
}
