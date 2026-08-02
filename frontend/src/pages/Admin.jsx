import { useEffect, useState } from "react";

import AdminSidebar from "../components/AdminSidebar";
import TopNavbar from "../components/TopNavbar";
import DashboardHeader from "../components/DashboardHeader";
import StatCard from "../components/StatCard";
import UploadDocument from "../components/UploadDocument";
import SystemHealth from "../components/SystemHealth";
import RecentDocuments from "../components/RecentDocuments";
import Activity from "../components/Activity";

function Admin() {
  const [stats, setStats] = useState({
    documents: 0,
    chunks: 0,
    embeddings: 0,
    qdrant: "Checking...",
  });

  // ==========================
  // Load Dashboard Statistics
  // ==========================
  const loadStats = () => {
    fetch("http://localhost:8000/admin/stats")
      .then((res) => res.json())
      .then((data) => {
        setStats({
          documents: data.documents || 0,
          chunks: data.chunks || 0,
          embeddings: data.embeddings || 0,
          qdrant: data.qdrant || "Unknown",
        });
      })
      .catch(() => {
        setStats({
          documents: 0,
          chunks: 0,
          embeddings: 0,
          qdrant: "Offline",
        });
      });
  };

  useEffect(() => {
    loadStats();
  }, []);

  // ==========================
  // Refresh Dashboard
  // ==========================
  const refreshDashboard = () => {
    loadStats();
  };

  // ==========================
  // Upload Button
  // ==========================
  const openUpload = () => {
    document.getElementById("uploadInput")?.click();
  };

  // ==========================
  // Process Documents
  // ==========================
  const runProcess = async () => {
    try {
      await fetch("http://localhost:8000/admin/process", {
        method: "POST",
      });

      alert("Document processing started");
    } catch {
      alert("Processing failed");
    }
  };

  // ==========================
  // Generate Embeddings
  // ==========================
  const generateEmbedding = async () => {
    try {
      await fetch("http://localhost:8000/admin/embeddings", {
        method: "POST",
      });

      alert("Embedding generation started");
    } catch {
      alert("Embedding generation failed");
    }
  };

  // ==========================
  // Check Qdrant
  // ==========================
  const checkQdrant = async () => {
    try {
      const response = await fetch(
        "http://localhost:8000/admin/qdrant"
      );

      const data = await response.json();

      setStats((prev) => ({
        ...prev,
        qdrant: data.status,
      }));
    } catch {
      setStats((prev) => ({
        ...prev,
        qdrant: "Offline",
      }));
    }
  };

  return (
    <div className="flex h-screen bg-slate-100">

      {/* Sidebar */}
      <AdminSidebar />

      {/* Main Content */}
      <div className="flex-1 flex flex-col">

        <TopNavbar />

        <main className="flex-1 overflow-y-auto p-8">

          <DashboardHeader
            onRefresh={refreshDashboard}
            onUpload={openUpload}
          />

          {/* Statistics */}
          <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-6 mt-8">

            <StatCard
              title="Documents"
              value={stats.documents}
              icon="📄"
              color="bg-blue-100"
            />

            <StatCard
              title="Chunks"
              value={stats.chunks}
              icon="📦"
              color="bg-yellow-100"
            />

            <StatCard
              title="Embeddings"
              value={stats.embeddings}
              icon="🧠"
              color="bg-purple-100"
            />

            <StatCard
              title="Qdrant"
              value={stats.qdrant}
              icon="🗄️"
              color="bg-green-100"
            />

          </div>

          {/* Document Management */}
          <div className="bg-white rounded-2xl shadow mt-8 p-8">

            <h2 className="text-2xl font-bold mb-6">
              Document Management
            </h2>

            <UploadDocument />

            <div className="flex flex-wrap gap-4 mt-8">

              <button
                onClick={runProcess}
                className="bg-green-700 hover:bg-green-800 text-white px-6 py-3 rounded-xl"
              >
                Process Documents
              </button>

              <button
                onClick={generateEmbedding}
                className="bg-purple-600 hover:bg-purple-700 text-white px-6 py-3 rounded-xl"
              >
                Generate Embeddings
              </button>

              <button
                onClick={checkQdrant}
                className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-xl"
              >
                Check Qdrant
              </button>

            </div>

          </div>

          {/* System Health & Activity */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-8">

            <SystemHealth />

            <Activity />

          </div>

          {/* Recent Documents */}
          <div className="mt-8">

            <RecentDocuments />

          </div>

        </main>

      </div>

    </div>
  );
}

export default Admin;