<template>
  <div class="home-container">
    <h1 class="app-title">DDART A.I. – Eye Analysis</h1>

    <div class="main-layout">
      <!-- LEFT: Upload Card -->
      <div class="upload-card" @drop.prevent="dropFile" @dragover.prevent>
        <input type="file" accept="image/*" @change="uploadFile" />
        <p class="drag-drop-text">Or drag & drop image here</p>
        <img v-if="uploadedImage" :src="uploadedImage" class="uploaded-image" />
      </div>

      <!-- RIGHT: Buttons -->
      <div class="side-buttons" v-if="uploadedImage">
        <button class="analyze-btn glaucoma" @click="analyzeImage('Glaucoma')">Analyze Glaucoma</button>
        <button class="analyze-btn dr" @click="analyzeImage('DR')">Analyze Diabetic Retinopathy</button>
        <button class="analyze-btn amd" @click="analyzeImage('AMD')">Analyze AMD</button>
        <button class="analyze-btn all" @click="analyzeImage('ALL')">🔍 Analyze All Conditions</button>
      </div>

      <!-- RIGHT placeholder when no image -->
      <div class="side-buttons placeholder-side" v-else>
        <p>Upload an image to begin analysis</p>
      </div>
    </div>

    <!-- Instructions Button -->
    <button class="instructions-btn" @click="showInstructions = true">Instructions</button>

    <!-- Instructions Modal -->
    <div v-if="showInstructions" class="modal-overlay" @click.self="showInstructions = false">
      <div class="modal-content">
        <h3>Instructions</h3>
        <ol>
          <li>Upload a clear eye image of the fundus.</li>
          <li>Ensure proper lighting and focus on the retina.</li>
          <li>Select the disease type you want to analyze: Glaucoma, AMD, Diabetic Retinopathy, or all at once.</li>
          <li>The AI will process the image and show the prediction with confidence score.</li>
          <li>Results below 85% confidence are marked as Inconclusive.</li>
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
          @click="uploadedImage = img"
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
      const reader = new FileReader()
      reader.onload = e => {
        this.uploadedImage = e.target.result
        this.addToRecent(this.uploadedImage)
      }
      reader.readAsDataURL(file)
    },
    dropFile(event) {
      const file = event.dataTransfer.files[0]
      if (!file) return
      const reader = new FileReader()
      reader.onload = e => {
        this.uploadedImage = e.target.result
        this.addToRecent(this.uploadedImage)
      }
      reader.readAsDataURL(file)
    },
    addToRecent(img) {
      if (!this.recentUploads.includes(img)) {
        this.recentUploads.unshift(img)
        if (this.recentUploads.length > 5) this.recentUploads.pop()
      }
    },
    analyzeImage(type) {
      this.$router.push({
        name: "Process",
        query: { img: this.uploadedImage, type }
      })
    }
  }
}
</script>

<style>
html, body {
  height: 100%;
  margin: 0;
  overflow: auto;
}

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

.main-layout {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 30px;
  width: 100%;
  max-width: 800px;
  align-items: start;
}

.upload-card {
  background: white;
  padding: 25px 30px;
  border-radius: 15px;
  box-shadow: 0 10px 25px rgba(0,0,0,0.08);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 15px;
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
  max-height: 260px;
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

.side-buttons {
  display: flex;
  flex-direction: column;
  gap: 12px;
  justify-content: center;
}

.placeholder-side {
  background: white;
  border-radius: 15px;
  padding: 30px;
  text-align: center;
  color: #aaa;
  box-shadow: 0 10px 25px rgba(0,0,0,0.08);
  font-size: 14px;
}

.analyze-btn {
  padding: 14px 18px;
  border: none;
  border-radius: 10px;
  font-weight: 600;
  color: white;
  cursor: pointer;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  width: 100%;
}

.analyze-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(0,0,0,0.2);
}

.analyze-btn.glaucoma { background: linear-gradient(90deg, #dc3545, #ff6b6b); }
.analyze-btn.dr       { background: linear-gradient(90deg, #17a2b8, #6bcff6); }
.analyze-btn.amd      { background: linear-gradient(90deg, #ffc107, #ffd95b); color: #212529; }
.analyze-btn.all      { background: linear-gradient(90deg, #6f42c1, #a78bfa); }

.instructions-btn {
  margin-top: 25px;
  background-color: #6c757d;
  color: white;
  padding: 10px 16px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
}

.instructions-btn:hover { background-color: #5a6268; }

.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.5);
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

.modal-content button {
  margin-top: 15px;
  background: #007bff;
  color: white;
  padding: 8px 16px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
}

.recent-uploads {
  margin-top: 30px;
  width: 100%;
  max-width: 800px;
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
  cursor: pointer;
}

.thumb:hover { border-color: #0056b3; transform: scale(1.05); }

.footer {
  margin-top: 30px;
  font-size: 13px;
  color: #555;
}
</style>