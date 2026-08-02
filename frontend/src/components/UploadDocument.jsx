import { useState } from "react";

function UploadDocument() {
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");

  const upload = async (e) => {
    const file = e.target.files[0];

    if (!file) return;

    // Check if the selected file is a PDF
    if (file.type !== "application/pdf") {
      setMessage("❌ Only PDF files are allowed.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      setLoading(true);
      setMessage("");

      const response = await fetch(
        "http://localhost:8000/admin/upload",
        {
          method: "POST",
          body: formData,
        }
      );

      const data = await response.json();

      setMessage(
        data.message || "✅ Document uploaded successfully."
      );
    } catch (error) {
      console.error(error);
      setMessage("❌ Upload failed.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-5">

      <label className="block text-lg font-semibold text-slate-700">
        Upload Legal PDF Document
      </label>

      <input
        id="uploadInput"
        type="file"
        accept=".pdf"
        onChange={upload}
        className="
          w-full
          rounded-xl
          border
          border-gray-300
          bg-white
          p-3
          cursor-pointer
          focus:outline-none
          focus:ring-2
          focus:ring-green-600
        "
      />

      {loading && (
        <div className="text-blue-600 font-medium">
          ⏳ Uploading document...
        </div>
      )}

      {message && (
        <div
          className={`font-medium ${
            message.includes("❌")
              ? "text-red-600"
              : "text-green-600"
          }`}
        >
          {message}
        </div>
      )}
    </div>
  );
}

export default UploadDocument;