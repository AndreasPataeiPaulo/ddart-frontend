<template>
    <div class="upload-container">
      <!-- App Name -->
      <h2 class="app-name">DDART A.I.</h2>
  
      <!-- File Upload -->
      <input type="file" accept="image/*" @change="uploadFile" />
  
      <!-- Confirm Button for Glaucoma -->
      <button v-if="uploadedImage" @click="confirmImageGlaucoma">
        Confirm for Glaucoma
      </button>
  
      <!-- Diabetic Retinopathy Button -->
      <button v-if="uploadedImage" class="dr-btn" @click="goToDR">
        Diabetic Retinopathy AI
      </button>
  
      <!-- Show uploaded image -->
      <img :src="uploadedImage" v-if="uploadedImage" class="uploaded-image"/>
  
      <!-- Instructions Button -->
      <button class="instructions-btn" @click="showInstructions = true">
        Instructions
      </button>
  
      <!-- Instructions Modal -->
      <div v-if="showInstructions" class="modal-overlay" @click.self="showInstructions = false">
        <div class="modal-content">
          <h3>Instructions</h3>
          <p>
            1. Upload a clear image of the eye.<br>
            2. Make sure the eye is well-lit.<br>
            3. Click "Confirm" to send it for Glaucoma analysis.<br>
            4. Or click "Diabetic Retinopathy AI" to analyze for DR.
          </p>
          <button @click="showInstructions = false">Close</button>
        </div>
      </div>
  
      <!-- Footer -->
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
  
      // Navigate to Glaucoma AI
      confirmImageGlaucoma() {
        this.$router.push({ name: 'Process', query: { img: this.uploadedImage } })
      },
  
      // Navigate to Diabetic Retinopathy AI
      goToDR() {
        this.$router.push({ name: 'DRProcess', query: { img: this.uploadedImage } })

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
    position: relative;
  }
  
  .app-name {
    font-size: 28px;
    font-weight: bold;
    color: #007bff;
    margin-bottom: 20px;
  }
  
  .uploaded-image {
    border: 2px solid #008cff;
    border-radius: 8px;
    max-width: 320px;
    max-height: 240px;
  }
  
  button, input[type="file"] {
    padding: 8px 14px;
    border: none;
    border-radius: 6px;
    background-color: #008cff;
    color: white;
    cursor: pointer;
    font-size: 14px;
    transition: background-color 0.2s;
  }
  
  button:hover, input[type="file"]:hover {
    background-color: #005bb5;
  }
  
  .instructions-btn {
    margin-top: 10px;
    background-color: #6c757d;
  }
  
  .dr-btn {
    background-color: #28a745;
    margin-top: 5px;
  }
  
  .modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0,0,0,0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
  }
  
  .modal-content {
    background: white;
    padding: 20px;
    border-radius: 8px;
    text-align: left;
    max-width: 400px;
  }
  
  .modal-content h3 {
    margin-top: 0;
  }
  
  .modal-content button {
    margin-top: 15px;
    background-color: #007bff;
  }
  
  .footer {
    position: absolute;
    bottom: 10px;
    right: 10px;
    font-size: 12px;
    color: #555;
  }
  </style>
  