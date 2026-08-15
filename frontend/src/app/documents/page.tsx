"use client";
import { useState, useEffect } from "react";
import DashboardLayout from "../dashboard/layout";
import { apiFetch } from "../../lib/api";

type Document = {
  id: string;
  filename: string;
  file_type: string;
  status: string;
  created_at: string;
};

export default function DocumentsPage() {
  const [isDragging, setIsDragging] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [documents, setDocuments] = useState<Document[]>([]);

  const fetchDocuments = async () => {
    try {
      const res = await apiFetch("/documents/");
      if (res.ok) {
        const data = await res.json();
        setDocuments(data);
      }
    } catch (err) {
      console.error("Failed to fetch documents", err);
    }
  };

  useEffect(() => {
    fetchDocuments();
  }, []);

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const handleDrop = async (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      await uploadFile(e.dataTransfer.files[0]);
    }
  };

  const handleFileInput = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      await uploadFile(e.target.files[0]);
    }
  };

  const uploadFile = async (file: File) => {
    setUploading(true);
    try {
      const formData = new FormData();
      formData.append("file", file);

      const res = await apiFetch("/documents/upload", {
        method: "POST",
        body: formData,
      });

      if (res.ok) {
        await fetchDocuments(); // Refresh the list
      } else {
        alert("Upload failed.");
      }
    } catch (err) {
      console.error("Upload error", err);
    } finally {
      setUploading(false);
    }
  };

  return (
    <DashboardLayout>
      <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-700">
        <div className="flex justify-between items-center border-b border-gray-800 pb-4">
          <div>
            <h1 className="text-3xl font-semibold tracking-tight">Documents</h1>
            <p className="text-gray-400 mt-1">Upload and manage your enterprise knowledge base.</p>
          </div>
        </div>

        {/* Upload Zone */}
        <div 
          className={`border-2 border-dashed rounded-xl p-12 text-center transition-colors ${
            isDragging ? "border-blue-500 bg-blue-500/10" : "border-gray-700 hover:border-gray-500 hover:bg-[#111]"
          }`}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
        >
          <div className="w-16 h-16 bg-gray-800 rounded-full mx-auto flex items-center justify-center mb-4">
            <svg className="w-8 h-8 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
            </svg>
          </div>
          <h3 className="text-xl font-medium text-white mb-2">Drag & Drop files here</h3>
          <p className="text-gray-400 mb-6">Supports PDF, PNG, JPG up to 50MB</p>
          
          <label className="cursor-pointer px-6 py-3 bg-white text-black rounded-md font-medium hover:bg-gray-200 transition-colors inline-block">
            {uploading ? "Uploading..." : "Browse Files"}
            <input type="file" className="hidden" accept=".pdf,.png,.jpg,.jpeg" onChange={handleFileInput} disabled={uploading} />
          </label>
        </div>

        {/* Document List */}
        <div>
          <h2 className="text-xl font-medium mb-4">Recent Documents</h2>
          <div className="bg-[#111] border border-gray-800 rounded-xl overflow-hidden">
            <table className="w-full text-left text-sm text-gray-400">
              <thead className="bg-[#1a1a1a] text-gray-300">
                <tr>
                  <th className="px-6 py-4 font-medium">Filename</th>
                  <th className="px-6 py-4 font-medium">Type</th>
                  <th className="px-6 py-4 font-medium">Status</th>
                  <th className="px-6 py-4 font-medium">Date Uploaded</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-800">
                {documents.map((doc) => (
                  <tr key={doc.id} className="hover:bg-[#1a1a1a] transition-colors">
                    <td className="px-6 py-4 font-medium text-white">{doc.filename}</td>
                    <td className="px-6 py-4">{doc.file_type}</td>
                    <td className="px-6 py-4">
                      <span className={`px-2 py-1 rounded-full text-xs border ${
                        doc.status === "COMPLETED" 
                          ? "bg-green-500/10 text-green-400 border-green-500/20" 
                          : doc.status === "FAILED"
                          ? "bg-red-500/10 text-red-400 border-red-500/20"
                          : "bg-blue-500/10 text-blue-400 border-blue-500/20"
                      }`}>
                        {doc.status}
                      </span>
                    </td>
                    <td className="px-6 py-4">
                      {new Date(doc.created_at).toLocaleDateString()}
                    </td>
                  </tr>
                ))}
                {documents.length === 0 && (
                  <tr>
                    <td colSpan={4} className="px-6 py-8 text-center text-gray-500">
                      No documents found. Upload one to get started.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
}
