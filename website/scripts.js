"use strict";

const serverUrl = "https://v9c90wf7fj.execute-api.us-east-1.amazonaws.com/api";
let currentImageData = null;

function showError(message) {
    const errorElem = document.getElementById("errorMessage");
    errorElem.textContent = message;
    errorElem.style.display = "block";
}

function hideError() {
    const errorElem = document.getElementById("errorMessage");
    errorElem.style.display = "none";
}

function startScanner() {
    const scannerContainer = document.getElementById("scannerContainer");
    scannerContainer.classList.add("active");
}

function stopScanner() {
    const scannerContainer = document.getElementById("scannerContainer");
    scannerContainer.classList.remove("active");
}

async function uploadImage(file) {
    const reader = new FileReader();

    return new Promise((resolve, reject) => {
        reader.onload = async () => {
            const encodedString = reader.result.toString().replace(/^data:(.*,)?/, '');

            try {
                const response = await fetch(serverUrl + "/images", {
                    method: "POST",
                    headers: {
                        'Accept': 'application/json',
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({filename: file.name, filebytes: encodedString})
                });

                if (response.ok) {
                    const imageData = await response.json();
                    currentImageData = imageData;
                    resolve(imageData);
                } else {
                    throw new HttpError(response);
                }
            } catch (error) {
                reject(error);
            }
        };

        reader.onerror = () => reject(new Error("Failed to read file"));
        reader.readAsDataURL(file);
    });
}

function updateImage(imageData) {
    const resultsSection = document.getElementById("resultsSection");
    const imageElem = document.getElementById("image");

    imageElem.src = imageData["fileUrl"];
    imageElem.alt = imageData["fileId"];
    resultsSection.style.display = "block";

    return imageData;
}

async function translateImage(imageData) {
    startScanner();

    try {
        const response = await fetch(serverUrl + "/images/" + imageData["fileId"] + "/translate-text", {
            method: "POST",
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({fromLang: "auto", toLang: "en"})
        });

        if (response.ok) {
            const translations = await response.json();
            stopScanner();
            return translations;
        } else {
            stopScanner();
            throw new HttpError(response);
        }
    } catch (error) {
        stopScanner();
        throw error;
    }
}

function annotateImage(translations) {
    const translationsElem = document.getElementById("translations");
    translationsElem.innerHTML = "";

    if (!Array.isArray(translations) || translations.length === 0) {
        translationsElem.innerHTML = '<p style="color: var(--text-muted);">No text detected in image</p>';
        return;
    }

    for (let i = 0; i < translations.length; i++) {
        const translation = translations[i];
        const itemDiv = document.createElement("div");
        itemDiv.className = "translation-item";

        const originalDiv = document.createElement("div");
        originalDiv.className = "translation-original";
        originalDiv.textContent = translation["text"];

        const arrowDiv = document.createElement("div");
        arrowDiv.className = "translation-arrow";
        arrowDiv.textContent = "↓";

        const translatedDiv = document.createElement("div");
        translatedDiv.className = "translation-translated";
        translatedDiv.textContent = translation["translation"]["translatedText"];

        itemDiv.appendChild(originalDiv);
        itemDiv.appendChild(arrowDiv);
        itemDiv.appendChild(translatedDiv);
        translationsElem.appendChild(itemDiv);
    }
}

function handleFileSelect(file) {
    hideError();

    uploadImage(file)
        .then(imageData => updateImage(imageData))
        .catch(error => {
            showError("Error uploading image: " + error.message);
            console.error(error);
        });
}

function handleTranslate() {
    if (!currentImageData) {
        showError("Please upload an image first");
        return;
    }

    hideError();
    translateImage(currentImageData)
        .then(translations => annotateImage(translations))
        .catch(error => {
            showError("Error translating image: " + error.message);
            console.error(error);
        });
}

function handleReset() {
    currentImageData = null;
    document.getElementById("file").value = "";
    document.getElementById("resultsSection").style.display = "none";
    hideError();
    stopScanner();
}

function setupEventListeners() {
    const uploadZone = document.getElementById("uploadZone");
    const fileInput = document.getElementById("file");
    const translateBtn = document.getElementById("translateBtn");
    const resetBtn = document.getElementById("resetBtn");

    uploadZone.addEventListener("click", () => fileInput.click());

    fileInput.addEventListener("change", (e) => {
        if (e.target.files.length > 0) {
            handleFileSelect(e.target.files[0]);
        }
    });

    uploadZone.addEventListener("dragover", (e) => {
        e.preventDefault();
        uploadZone.classList.add("dragover");
    });

    uploadZone.addEventListener("dragleave", () => {
        uploadZone.classList.remove("dragover");
    });

    uploadZone.addEventListener("drop", (e) => {
        e.preventDefault();
        uploadZone.classList.remove("dragover");
        if (e.dataTransfer.files.length > 0) {
            handleFileSelect(e.dataTransfer.files[0]);
        }
    });

    translateBtn.addEventListener("click", handleTranslate);
    resetBtn.addEventListener("click", handleReset);
}

document.addEventListener("DOMContentLoaded", setupEventListeners);

class HttpError extends Error {
    constructor(response) {
        super(`${response.status} for ${response.url}`);
        this.name = "HttpError";
        this.response = response;
    }
}
