const imageInput = document.getElementById("imageInput");
const removeBtn = document.getElementById("removeBtn");
const resultImage = document.getElementById("resultImage");
const downloadLink = document.getElementById("downloadLink");

removeBtn.addEventListener("click", async () => {
  const file = imageInput.files[0];

  if (!file) {
    alert("Please upload an image first!");
    return;
  }

  const formData = new FormData();
  formData.append("file", file);

  try {
    const response = await fetch("https://background-remover-hcj4.onrender.com/remove-bg", {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
        throw new Error("Server error: " + response.statusText);
    }

    const blob = await response.blob();
    const imageUrl = URL.createObjectURL(blob);

    resultImage.src = imageUrl;
    downloadLink.href = imageUrl;
    downloadLink.style.display = "inline";
  } catch (error) {
    console.error("Fetch error:", error);
    alert("The server might be waking up. Try again in 30 seconds!");
  }
});

# http://localhost:8000/remove-bg