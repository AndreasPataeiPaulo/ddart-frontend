<template>
  <div class="home-container">
    <h1 class="app-title">DDART A.I. – Eye Analysis</h1>

    <!-- Upload Card -->
    <div class="upload-card" @drop.prevent="dropFile" @dragover.prevent>
      <input type="file" accept="image/*" @change="uploadFile" />
      <p class="drag-drop-text">Or drag & drop image here</p>

      <!-- Image + Actions Layout -->
      <div v-if="uploadedImage" class="analysis-layout">
        <!-- LEFT: Image Preview -->
        <img :src="uploadedImage" class="uploaded-image" />

        <!-- RIGHT: Analyze Buttons -->
        <div class="disease-buttons">
          <button class="analyze-btn glaucoma" @click="analyzeImage('Glaucoma')">
            Analyze Glaucoma
          </button>
          <button class="analyze-btn dr" @click="analyzeImage('DR')">
            Analyze DR
          </button>
          <button class="analyze-btn amd" @click="analyzeImage('AMD')">
            Analyze AMD
          </button>
        </div>
      </div>
    </div>

    <!-- Instructions -->
    <button class="instructions-btn" @click="showInstructions = true">
      Instructions
    </button>

    <!-- Instructions Modal -->
    <div
      v-if="showInstructions"
      class="modal-overlay"
      @click.self="showInstructions = false"
    >
      <div class="modal-content">
        <h3>Instructions</h3>
        <ol>
          <li>Upload a clear fundus image.</li>
          <li>Ensure good lighting and focus.</li>
          <li>Select the disease you want to analyze.</li>
          <li>AI will return prediction & confidence.</li>
        </ol>
        <button @click="showInstructions = false">Close</button>
      </div>
    </div>

    <!-- Recent Uploads -->
    <div v-if="recentUploads.length" class="recent-uploads">
      <h3>Recent Uploads</h3>
      <div class="thumbs">
        <img
          v-for="(img, idx) in recentUploads"
          :key="idx"
          :src="img"
          class="thumb"
        />
      </div>
    </div>

    <p class="footer">Made by Andreas Lampiris</p>
  </div>
</template>

<script>
export default {
  data() {
    return {
      uploadedImage: null,
      recentUploads: [],
      showInstructions: false
    }
  },
  methods: {
    uploadFile(event) {
      const file = event.target.files[0]
      if (!file) return
      this.readFile(file)
    },
    dropFile(event) {
      const file = event.dataTransfer.files[0]
      if (!file) return
      this.readFile(file)
    },
    readFile(file) {
      const reader = new FileReader()
      reader.onload = e => {
        this.uploadedImage = e.target.result
        this.recentUploads.unshift(this.uploadedImage)
        if (this.recentUploads.length > 5) this.recentUploads.pop()
      }
      reader.readAsDataURL(file)
    },
    analyzeImage(type) {
      this.$router.push({
        name: "Process",
        query: {
          img: this.uploadedImage,
          type
        }
      })
    }
  }
}
</script>

<style>
/* ---- LOCK SCROLL ---- */
html, body {
  height: 100%;
  margin: 0;
  overflow: hidden;
}

/* ---- PAGE ---- */
.home-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  padding: 30px 20px;
  background: #f4f6fa;
  height: 100vh;
}

/* ---- TITLE ---- */
.app-title {
  font-size: 34px;
  color: #007bff;
  margin-bottom: 20px;
}

/* ---- CARD ---- */
.upload-card {
  background: white;
  padding: 22px 26px;
  border-radius: 15px;
  box-shadow: 0 10px 25px rgba(0,0,0,0.08);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 14px;
  width: 100%;
  max-width: 520px;
}

/* ---- DRAG TEXT ---- */
.drag-drop-text {
  font-size: 13px;
  color: #555;
}

/* ---- MAIN LAYOUT ---- */
.analysis-layout {
  display: flex;
  gap: 20px;
  width: 100%;
  align-items: center;
  justify-content: space-between;
}

/* ---- IMAGE ---- */
.uploaded-image {
  max-width: 210px;
  max-height: 220px;
  border-radius: 12px;
  border: 2px solid #007bff;
  object-fit: contain;
}

/* ---- BUTTONS ---- */
.disease-buttons {
  display: flex;
  flex-direction: column;
  gap: 10px;
  min-width: 170px;
}

.analyze-btn {
  padding: 12px;
  border-radius: 8px;
  border: none;
  font-weight: 600;
  color: white;
  cursor: pointer;
  transition: all 0.2s ease;
}

.analyze-btn.glaucoma {
  background: linear-gradient(90deg, #dc3545, #ff6b6b);
}

.analyze-btn.dr {
  background: linear-gradient(90deg, #17a2b8, #6bcff6);
}

.analyze-btn.amd {
  background: linear-gradient(90deg, #ffc107, #ffd95b);
  color: #212529;
}

.analyze-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(0,0,0,0.25);
}

/* ---- INSTRUCTIONS ---- */
.instructions-btn {
  margin-top: 18px;
  background-color: #6c757d;
  color: white;
  padding: 10px 16px;
  border-radius: 8px;
  border: none;
  cursor: pointer;
}

/* ---- MODAL ---- */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-content {
  background: white;
  padding: 25px 30px;
  border-radius: 12px;
  max-width: 420px;
}

/* ---- RECENT ---- */
.recent-uploads {
  margin-top: 18px;
  max-width: 520px;
  width: 100%;
}

.thumbs {
  display: flex;
  gap: 8px;
}

.thumb {
  width: 55px;
  height: 55px;
  object-fit: cover;
  border-radius: 8px;
  border: 1px solid #007bff;
}

/* ---- FOOTER ---- */
.footer {
  margin-top: auto;
  font-size: 12px;
  color: #555;
}

/* ---- MOBILE ---- */
@media (max-width: 600px) {
  .analysis-layout {
    flex-direction: column;
  }
  .disease-buttons {
    width: 100%;
  }
}
</style>
