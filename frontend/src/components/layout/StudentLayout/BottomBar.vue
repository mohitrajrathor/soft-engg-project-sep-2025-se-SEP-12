<template>
  <footer
    class="fixed bottom-0 left-[250px] w-[calc(100%-250px)] bg-white border-t shadow-md z-50 px-6 py-3 flex items-center justify-between"
  >
    <div class="flex items-end gap-3 w-full max-w-3xl mx-auto">
      <!-- Auto-expanding Textarea -->
      <textarea
        v-model="message"
        placeholder="Type a follow-up..."
        rows="1"
        ref="textareaRef"
        @input="autoResize"
        class="flex-1 resize-none border rounded-2xl px-4 py-3 shadow-sm focus:ring focus:border-blue-300 transition leading-relaxed overflow-hidden"
      ></textarea>

      <!-- Hidden File Input -->
      <input
        ref="fileInput"
        type="file"
        accept="image/*,.pdf,.doc,.docx,.txt"
        class="hidden"
        @change="handleFileUpload"
      />

      <!-- Paper Clip (Attach) -->
      <button
        type="button"
        class="p-2 rounded-xl bg-blue-50 hover:bg-blue-100 transition"
        @click="triggerFilePicker"
      >
        <PaperClipIcon class="w-5 h-5 text-gray-500" />
      </button>

      <!-- Send Button -->
      <button
        type="button"
        class="bg-blue-600 text-white px-5 py-2 rounded-xl font-semibold hover:bg-blue-700 transition flex items-center gap-2"
        @click="sendMessage"
      >
        Send
      </button>
    </div>

    <!-- Attached File Preview -->
    <div
      v-if="attachedFile"
      class="absolute bottom-16 left-1/2 transform -translate-x-1/2 bg-blue-50 px-4 py-2 rounded-xl flex items-center gap-3 text-sm text-gray-700 shadow-lg"
    >
      <PaperClipIcon class="w-4 h-4 text-blue-500" />
      <span class="truncate max-w-xs">{{ attachedFile.name }}</span>
      <button @click="removeAttachment" class="text-red-500 hover:text-red-700 font-semibold">
        Remove
      </button>
    </div>
  </footer>
</template>

<script setup>
import { ref, nextTick } from "vue";
import { PaperClipIcon } from "@heroicons/vue/24/outline";

const message = ref("");
const attachedFile = ref(null);
const fileInput = ref(null);
const textareaRef = ref(null);

const triggerFilePicker = () => fileInput.value.click();

const handleFileUpload = (event) => {
  attachedFile.value = event.target.files[0];
};

const removeAttachment = () => {
  attachedFile.value = null;
  fileInput.value.value = "";
};

const sendMessage = () => {
  if (!message.value.trim()) return;
  console.log("Message sent:", message.value, attachedFile.value);
  message.value = "";
  attachedFile.value = null;
  nextTick(() => autoResize());
};

// Auto-resize logic
const autoResize = () => {
  const el = textareaRef.value;
  if (!el) return;
  el.style.height = "auto"; // Reset height
  el.style.height = el.scrollHeight + "px"; // Expand to fit content
};
</script>

<style scoped>
footer {
  height: auto;
  min-height: 72px;
}
textarea {
  max-height: 200px; /* prevents it from growing too large */
}
</style>
