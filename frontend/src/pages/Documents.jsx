import React, { useEffect, useRef, useState } from "react";
import Layout from "../components/Layout";
import { documentsApi } from "../services/api";

const STATUS_STYLES = {
  ready: "bg-emerald-50 text-emerald-700",
  processing: "bg-amber-50 text-amber-700",
  failed: "bg-red-50 text-red-700",
};

export default function Documents() {
  const [documents, setDocuments] = useState([]);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState("");
  const [dragActive, setDragActive] = useState(false);
  const fileInputRef = useRef(null);

  const loadDocuments = async () => {
    const res = await documentsApi.list();
    setDocuments(res.data);
  };

  useEffect(() => {
    loadDocuments();
  }, []);

  const handleFiles = async (files) => {
    if (!files || files.length === 0) return;
    setError("");
    setUploading(true);
    try {
      for (const file of files) {
        await documentsApi.upload(file);
      }
      await loadDocuments();
    } catch (err) {
      setError(err.response?.data?.detail || "Upload failed. Please try again.");
    } finally {
      setUploading(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setDragActive(false);
    handleFiles(Array.from(e.dataTransfer.files));
  };

  const handleDelete = async (id) => {
    await documentsApi.remove(id);
    setDocuments((docs) => docs.filter((d) => d.id !== id));
  };

  return (
    <Layout>
      <div className="mx-auto max-w-3xl px-8 py-10">
        <h1 className="text-2xl font-semibold tracking-tight">Documents</h1>
        <p className="mt-1 text-sm text-ink/50">
          Upload PDF, DOCX, or Markdown files. They'll be processed into searchable
          knowledge for the chat assistant.
        </p>

        <div
          onDragOver={(e) => {
            e.preventDefault();
            setDragActive(true);
          }}
          onDragLeave={() => setDragActive(false)}
          onDrop={handleDrop}
          className={`mt-6 flex flex-col items-center justify-center rounded-2xl border-2 border-dashed px-6 py-12 text-center transition ${
            dragActive ? "border-accent bg-accent/5" : "border-ink/15 bg-white"
          }`}
        >
          <p className="text-sm font-medium text-ink/70">
            Drag & drop files here, or
          </p>
          <button
            onClick={() => fileInputRef.current?.click()}
            className="btn-secondary mt-3"
            disabled={uploading}
          >
            {uploading ? "Uploading..." : "Browse files"}
          </button>
          <input
            ref={fileInputRef}
            type="file"
            multiple
            accept=".pdf,.docx,.md,.markdown,.txt"
            className="hidden"
            onChange={(e) => handleFiles(Array.from(e.target.files))}
          />
          <p className="mt-2 text-xs text-ink/40">PDF, DOCX, Markdown, or TXT</p>
        </div>

        {error && (
          <div className="mt-4 rounded-lg bg-red-50 px-3 py-2 text-sm text-red-700">
            {error}
          </div>
        )}

        <div className="mt-8 space-y-2">
          {documents.length === 0 && (
            <p className="py-8 text-center text-sm text-ink/40">
              No documents yet. Upload one to get started.
            </p>
          )}
          {documents.map((doc) => (
            <div
              key={doc.id}
              className="card flex items-center justify-between px-4 py-3"
            >
              <div className="flex items-center gap-3">
                <span className="text-lg">📄</span>
                <div>
                  <p className="text-sm font-medium">{doc.filename}</p>
                  <p className="text-xs text-ink/40">
                    {doc.num_chunks} chunks · {doc.file_type.toUpperCase()}
                  </p>
                </div>
              </div>
              <div className="flex items-center gap-3">
                <span
                  className={`rounded-full px-2.5 py-1 text-xs font-medium ${STATUS_STYLES[doc.status] || ""}`}
                >
                  {doc.status}
                </span>
                <button
                  onClick={() => handleDelete(doc.id)}
                  className="text-xs font-medium text-ink/40 hover:text-red-600"
                >
                  Delete
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </Layout>
  );
}
