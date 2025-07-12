document.getElementById("fileInput").addEventListener("change", function () {
  const file = this.files[0];
  const fileNameDisplay = document.getElementById("fileName");
  const preview = document.getElementById("filePreview");
  const removeBtn = document.getElementById("removeFileBtn");

  if (file) {
    fileNameDisplay.textContent = `📎 File selected: ${file.name}`;
    removeBtn.style.display = "block";
    preview.innerHTML = "";

    // Optional preview (image or PDF)
    if (file.type.startsWith("image/")) {
      const img = document.createElement("img");
      img.src = URL.createObjectURL(file);
      preview.appendChild(img);
    } else if (file.type === "application/pdf") {
      const embed = document.createElement("embed");
      embed.src = URL.createObjectURL(file);
      embed.type = "application/pdf";
      embed.width = "100%";
      embed.height = "300px";
      preview.appendChild(embed);
    }
  } else {
    fileNameDisplay.textContent = "";
    preview.innerHTML = "";
    removeBtn.style.display = "none";
  }
});

document.getElementById("removeFileBtn").addEventListener("click", function () {
  const fileInput = document.getElementById("fileInput");
  const fileNameDisplay = document.getElementById("fileName");
  const preview = document.getElementById("filePreview");

  fileInput.value = "";
  fileNameDisplay.textContent = "";
  preview.innerHTML = "";
  this.style.display = "none";
});


function analyzeInput() {
  const fileInput = document.getElementById("fileInput");
  const textInput = document.getElementById("textInput").value.trim();
  const formData = new FormData();

  if (fileInput.files.length > 0) {
    formData.append("file", fileInput.files[0]);
  } else if (textInput.length > 0) {
    formData.append("text", textInput);
  } else {
    return alert("Please upload a file or paste some contract text.");
  }

  fetch("/analyze", {
    method: "POST",
    body: formData,
  })
    .then((res) => res.json())
    .then((data) => {
      const resultsContainer = document.querySelector(".results-container");
      const resultsSection = document.getElementById("results");
      const rawTextBox = document.getElementById("rawText");

      resultsContainer.innerHTML = "";
      rawTextBox.textContent = data.extracted_text || "";
      resultsSection.style.display = "block";

      data.analysis.forEach((item) => {
        const div = document.createElement("div");
        div.className = `result-card ${item.risk_level}`;
        div.innerHTML = `
          <strong>${item.title}</strong><br/>
          <p>${item.summary}</p>
          <p><strong>Risk:</strong> ${item.risk_level.toUpperCase()} | <strong>Keywords:</strong> ${item.keywords_found.join(", ")}</p>
        `;
        resultsContainer.appendChild(div);
      });
    })
    .catch((err) => {
      console.error(err);
      alert("An error occurred during analysis.");
    });
}
