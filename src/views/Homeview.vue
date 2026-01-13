<template>
  <div class="upload-container">
    <h2 class="app-name">DDART A.I.</h2>

    <!-- Upload -->
    <input type="file" accept="image/*" @change="uploadFile" />

    <!-- Single Analyze Button -->
    <button v-if="uploadedImage" @click="analyzeImage">
      Analyze Eye 
    </button>

    <!-- Preview -->
    <img
      v-if="uploadedImage"
      :src="uploadedImage"
      class="uploaded-image"
    />

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
          4. AI will analyze and compare eye images to detect glaucoma D.R. and other problems.
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
.upload-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 15px;
  margin-top: 20px;
  font-family: Arial, sans-serif;
}

.app-name {
  font-size: 28px;
  font-weight: bold;
  color: #007bff;
}

.uploaded-image {
  border: 2px solid #008cff;
  border-radius: 8px;
  max-width: 320px;
}

button,
input[type="file"] {
  padding: 8px 14px;
  border: none;
  border-radius: 6px;
  background-color: #008cff;
  color: white;
  cursor: pointer;
}

.instructions-btn {
  background-color: #6c757d;
}

.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-content {
  background: white;
  padding: 20px;
  border-radius: 8px;
}

.footer {
  position: fixed;
  bottom: 10px;
  right: 10px;
  font-size: 12px;
  color: #555;
}
</style>
