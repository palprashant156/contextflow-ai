import Link from "next/link";
import { ReactNode } from "react";

export default function DashboardLayout({ children }: { children: ReactNode }) {
  return (
    <div className="flex h-screen bg-[#0a0a0a] text-white overflow-hidden">
      {/* Sidebar */}
      <aside className="w-64 border-r border-gray-800 bg-[#0f0f0f] flex flex-col">
        <div className="h-16 flex items-center px-6 border-b border-gray-800">
          <Link href="/" className="text-xl font-bold bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent">
            CortexFlow AI
          </Link>
        </div>
        <nav className="flex-1 py-6 px-4 space-y-2">
          <NavItem href="/dashboard" label="Dashboard" active />
          <NavItem href="/documents" label="Documents" />
          <NavItem href="/chat" label="AI Chat" />
          <NavItem href="/ml-models" label="ML Models" />
          <NavItem href="/workflows" label="Workflows" />
          <NavItem href="/analytics" label="Analytics" />
        </nav>
        <div className="p-4 border-t border-gray-800">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-full bg-gray-700"></div>
            <div className="text-sm">
              <p className="font-medium">User</p>
              <p className="text-gray-400 text-xs">user@cortexflow.ai</p>
            </div>
          </div>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 flex flex-col h-full overflow-y-auto">
        <header className="h-16 flex items-center px-8 border-b border-gray-800 bg-[#0f0f0f]/80 backdrop-blur-md sticky top-0 z-10">
          <h2 className="text-lg font-medium text-gray-200">Overview</h2>
        </header>
        <div className="p-8">
          {children}
        </div>
      </main>
    </div>
  );
}

function NavItem({ href, label, active = false }: { href: string; label: string; active?: boolean }) {
  return (
    <Link 
      href={href} 
      className={`block px-4 py-2 rounded-md transition-colors ${
        active ? "bg-blue-600/10 text-blue-400 border border-blue-500/20" : "text-gray-400 hover:text-white hover:bg-gray-800"
      }`}
    >
      {label}
    </Link>
  );
}
