<template>
  <div class="home-container">
    <h1 class="app-title">DDART A.I. – Eye Analysis</h1>

    <!-- Upload Card -->
    <div class="upload-card" @drop.prevent="dropFile" @dragover.prevent>
      <input type="file" accept="image/*" @change="uploadFile" />
      <p class="drag-drop-text">Or drag & drop image here</p>

      <!-- Preview -->
      <img
        v-if="uploadedImage"
        :src="uploadedImage"
        class="uploaded-image"
      />

      <!-- Disease Selection Buttons -->
      <div v-if="uploadedImage" class="disease-buttons">
        <button class="analyze-btn glaucoma" @click="analyzeImage('Glaucoma')">Analyze Glaucoma</button>
        <button class="analyze-btn dr" @click="analyzeImage('DR')">Analyze DR</button>
        <button class="analyze-btn amd" @click="analyzeImage('AMD')">Analyze AMD</button>
      </div>
    </div>

    <!-- Instructions Panel -->
    <button class="instructions-btn" @click="showInstructions = true">
      Instructions
    </button>

    <div
      v-if="showInstructions"
      class="modal-overlay"
      @click.self="showInstructions = false"
    >
      <div class="modal-content">
        <h3>Instructions</h3>
        <ol>
          <li>Upload a clear eye image of the fundus.</li>
          <li>Ensure proper lighting and focus on the retina.</li>
          <li>Select the disease type you want to analyze: Glaucoma, AMD, or Diabetic Retinopathy.</li>
          <li>The AI will process the image and show the prediction with confidence.</li>
          <li>You can repeat for multiple images by pressing the upload again or go back.</li>
        </ol>
        <button @click="showInstructions = false">Close</button>
      </div>
    </div>

    <!-- Recent Uploads -->
    <div v-if="recentUploads.length" class="recent-uploads">
      <h3>Recent Uploads</h3>
      <div class="thumbs">
        <img v-for="(img, idx) in recentUploads" :key="idx" :src="img" class="thumb" />
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
      const reader = new FileReader()
      reader.onload = e => {
        this.uploadedImage = e.target.result
        this.recentUploads.unshift(this.uploadedImage)
        if (this.recentUploads.length > 5) this.recentUploads.pop()
      }
      reader.readAsDataURL(file)
    },
    dropFile(event) {
      const file = event.dataTransfer.files[0]
      if (!file) return
      const reader = new FileReader()
      reader.onload = e => {
        this.uploadedImage = e.target.result
        this.recentUploads.unshift(this.uploadedImage)
        if (this.recentUploads.length > 5) this.recentUploads.pop()
      }
      reader.readAsDataURL(file)
    },
    analyzeImage(diseaseType) {
      this.$router.push({
        name: "Process",
        query: {
          img: this.uploadedImage,
          type: diseaseType
        }
      })
    }
  }
}
</script>

<style>
.home-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  padding: 40px 20px;
  background: #f4f6fa;
  min-height: 100vh;
}

.app-title {
  font-size: 36px;
  color: #007bff;
  margin-bottom: 30px;
  text-shadow: 1px 1px 3px rgba(0,0,0,0.1);
}

.upload-card {
  background: white;
  padding: 25px 30px;
  border-radius: 15px;
  box-shadow: 0 10px 25px rgba(0,0,0,0.08);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
  max-width: 380px;
  width: 100%;
  transition: all 0.2s ease;
}

.upload-card:hover {
  box-shadow: 0 12px 30px rgba(0,0,0,0.12);
}

.drag-drop-text {
  font-size: 14px;
  color: #555;
}

.uploaded-image {
  border-radius: 12px;
  max-width: 100%;
  max-height: 280px;
  border: 2px solid #007bff;
  object-fit: contain;
}

input[type="file"] {
  padding: 10px;
  border-radius: 8px;
  border: 1px solid #ccc;
  cursor: pointer;
  width: 100%;
}

button {
  padding: 12px 18px;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease-in-out;
}

.analyze-btn {
  color: white;
  width: 100%;
  margin-top: 8px;
}

.analyze-btn.glaucoma {
  background: linear-gradient(90deg, #dc3545, #ff6b6b);
}
.analyze-btn.dr {
  background: linear-gradient(90deg, #17a2b8, #6bcff6);
}
.analyze-btn.amd {
  background: linear-gradient(90deg, #ffc107, #ffd95b);
}

.analyze-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(0,0,0,0.2);
}

.instructions-btn {
  margin-top: 25px;
  background-color: #6c757d;
  color: white;
  padding: 10px 16px;
}

.instructions-btn:hover {
  background-color: #5a6268;
}

.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  padding: 25px 30px;
  border-radius: 12px;
  max-width: 420px;
  text-align: left;
  box-shadow: 0 10px 25px rgba(0,0,0,0.15);
}

.recent-uploads {
  margin-top: 30px;
  width: 100%;
  max-width: 380px;
}

.thumbs {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.thumb {
  width: 60px;
  height: 60px;
  object-fit: cover;
  border-radius: 8px;
  border: 1px solid #007bff;
}


.footer {
  margin-top: 30px;
  font-size: 13px;
  color: #555;
}
button {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

button:hover:not(:disabled) {
  transform: scale(1.05);
  box-shadow: 0 8px 22px rgba(0, 0, 0, 0.18);
}
html, body {
  height: 100%;
  margin: 0;
  overflow: hidden;
}
</style>
