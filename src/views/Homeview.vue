<template>
  <div class="home-container">
    <h1 class="app-title">DDART A.I.</h1>

    <div class="upload-card">
      <!-- Upload -->
      <input type="file" accept="image/*" @change="uploadFile" />

      <!-- Preview -->
      <img
        v-if="uploadedImage"
        :src="uploadedImage"
        class="uploaded-image"
      />

      <!-- Single Analyze Button -->
      <button v-if="uploadedImage" class="analyze-btn" @click="analyzeImage">
        Analyze Eye
      </button>
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
        <p>
          1. Upload a clear eye image of the fundus.<br />
          2. Make sure the eye is well-lit.<br />
          3. Click “Analyze Eye”.<br />
          4. AI will analyze and compare eye images to detect glaucoma, D.R., and AMD.
        </p>
        <button @click="showInstructions = false">Close</button>
      </div>
    </div>

    <p class="footer">made by andreas</p>
  </div>
</template>

<script>
export default {
  data() {
    return {
      uploadedImage: null,
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
      }
      reader.readAsDataURL(file)
    },

    analyzeImage() {
      this.$router.push({
        name: "Process",
        query: { img: this.uploadedImage }
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
  max-width: 360px;
  width: 100%;
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
  background: linear-gradient(90deg, #007bff, #00c6ff);
  color: white;
  width: 100%;
}

.analyze-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(0, 198, 255, 0.4);
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
  max-width: 400px;
  text-align: left;
  box-shadow: 0 10px 25px rgba(0,0,0,0.15);
}

.footer {
  margin-top: 30px;
  font-size: 13px;
  color: #555;
}
</style>
