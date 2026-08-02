function AdminSidebar() {

  const handleLogout = async () => {

    try {

      await fetch("http://localhost:8000/admin/logout", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        }
      });

    } catch (error) {

      console.log("Logout error:", error);

    }


    // Remove authentication data
    localStorage.removeItem("token");

    // Redirect to login page
    window.location.href = "/login";

  };


  return (

    <aside className="w-72 bg-green-950 text-white flex flex-col justify-between min-h-screen">


      <div>


        {/* Header */}

        <div className="p-6 border-b border-green-900">


          <h1 className="text-2xl font-bold">

            ⚖ Ethiopian Legal AI

          </h1>


          <p className="text-green-300 text-sm mt-1">

            RAG Control Center

          </p>


        </div>



        {/* Navigation */}

        <nav className="p-5 space-y-2">


          <button
            className="
            w-full
            text-left
            p-3
            rounded-lg
            bg-green-900
            hover:bg-green-800
            "
          >

            🏠 Dashboard

          </button>



          <button
            className="
            w-full
            text-left
            p-3
            rounded-lg
            hover:bg-green-900
            "
          >

            📄 Documents

          </button>




          <button
            className="
            w-full
            text-left
            p-3
            rounded-lg
            hover:bg-green-900
            "
          >

            🧠 Embeddings

          </button>




          <button
            className="
            w-full
            text-left
            p-3
            rounded-lg
            hover:bg-green-900
            "
          >

            🗄 Vector Database

          </button>




          <button
            className="
            w-full
            text-left
            p-3
            rounded-lg
            hover:bg-green-900
            "
          >

            💬 Chat Management

          </button>




          <button
            className="
            w-full
            text-left
            p-3
            rounded-lg
            hover:bg-green-900
            "
          >

            📊 Reports

          </button>




          <button
            className="
            w-full
            text-left
            p-3
            rounded-lg
            hover:bg-green-900
            "
          >

            ⚙ Settings

          </button>


        </nav>


      </div>




      {/* Admin Footer */}

      <div className="p-5 border-t border-green-900">


        <p className="mb-4">

          👤 Admin

        </p>



        <button

          onClick={handleLogout}

          className="
          w-full
          bg-red-600
          hover:bg-red-700
          rounded-lg
          py-3
          transition
          "

        >

          🚪 Logout

        </button>



      </div>



    </aside>

  );

}



export default AdminSidebar;