<script setup>
import { ref } from 'vue';

const markdownInput = ref('');
const convertedOutput = ref('');
const dragging = ref(false); // 用于拖拽样式
const errorMessage = ref(''); // 错误信息
const backendUrl = import.meta.env.VITE_BACKEND_API_URL || 'http://localhost:5000'; // 后端API地址

// 处理文件拖拽进入
const handleDragEnter = (e) => {
  e.preventDefault();
  e.stopPropagation();
  dragging.value = true;
};

// 处理文件拖拽离开
const handleDragLeave = (e) => {
  e.preventDefault();
  e.stopPropagation();
  dragging.value = false;
};

// 处理文件在区域内移动
const handleDragOver = (e) => {
  e.preventDefault();
  e.stopPropagation();
};

// 处理文件拖拽放下
const handleDrop = (e) => {
  e.preventDefault();
  e.stopPropagation();
  dragging.value = false;
  errorMessage.value = '';

  const files = e.dataTransfer.files;
  if (files.length > 0) {
    const file = files[0];
    if (file.type === 'text/markdown' || file.name.endsWith('.md')) {
      readFile(file);
    } else {
      errorMessage.value = '请拖拽一个 Markdown (.md) 文件。';
    }
  }
};

// 处理手动选择文件
const handleFileSelect = (e) => {
  errorMessage.value = '';
  const files = e.target.files;
  if (files.length > 0) {
    const file = files[0];
    if (file.type === 'text/markdown' || file.name.endsWith('.md')) {
      readFile(file);
    } else {
      errorMessage.value = '请选择一个 Markdown (.md) 文件。';
    }
  }
};

// 读取文件内容
const readFile = (file) => {
  const reader = new FileReader();
  reader.onload = async (e) => {
    markdownInput.value = e.target.result;
    await convertMarkdown();
  };
  reader.onerror = () => {
    errorMessage.value = '文件读取失败。';
  };
  reader.readAsText(file);
};


// 调用后端 API 进行转换
const convertMarkdown = async () => {
  if (!markdownInput.value) {
    convertedOutput.value = '';
    errorMessage.value = '请先输入或上传 Markdown 内容。';
    return;
  }
  errorMessage.value = '';
  try {
    const response = await fetch(`${backendUrl}/convert`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ markdown_text: markdownInput.value }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    convertedOutput.value = data.converted_text;
  } catch (error) {
    console.error('转换失败:', error);
    errorMessage.value = '转换失败，请检查后端服务是否运行正常。';
    convertedOutput.value = '';
  }
};

// 复制到剪贴板
const copyToClipboard = () => {
  if (convertedOutput.value) {
    navigator.clipboard.writeText(convertedOutput.value)
      .then(() => {
        alert('转换后的文本已复制到剪贴板！');
      })
      .catch(err => {
        console.error('复制失败:', err);
        alert('复制失败，请手动复制。');
      });
  } else {
    errorMessage.value = '没有内容可以复制。';
  }
};
</script>

<template>
  <div id="app">
    <h1>Markdown 转换器</h1>

    <div
      class="drop-zone"
      :class="{ 'dragging': dragging }"
      @dragenter="handleDragEnter"
      @dragleave="handleDragLeave"
      @dragover="handleDragOver"
      @drop="handleDrop"
    >
      <p>将 Markdown 文件拖拽到此处，或</p>
      <input type="file" @change="handleFileSelect" accept=".md, text/markdown" class="file-input" />
      <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
    </div>

    <div class="editor-section">
      <div class="input-area">
        <h2>Markdown 输入</h2>
        <textarea
          v-model="markdownInput"
          placeholder="在这里粘贴或输入 Markdown 文本"
          rows="15"
          @input="convertMarkdown"
        ></textarea>
      </div>

      <div class="output-area">
        <h2>转换结果</h2>
        <textarea
          v-model="convertedOutput"
          readonly
          rows="15"
        ></textarea>
        <button @click="copyToClipboard" :disabled="!convertedOutput">复制到剪贴板</button>
      </div>
    </div>
  </div>
</template>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
  max-width: 1200px;
  margin-left: auto;
  margin-right: auto;
  padding: 20px;
  box-shadow: 0 0 10px rgba(0,0,0,0.1);
  border-radius: 8px;
}

h1 {
  color: #34495e;
  margin-bottom: 30px;
}

.drop-zone {
  border: 2px dashed #ccc;
  padding: 30px;
  margin-bottom: 20px;
  cursor: pointer;
  background-color: #f9f9f9;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.drop-zone.dragging {
  background-color: #e0e0e0;
  border-color: #3498db;
}

.drop-zone p {
  margin: 0;
  font-size: 1.1em;
  color: #555;
}

.file-input {
  margin-top: 15px;
}

.editor-section {
  display: flex;
  gap: 20px;
  margin-top: 30px;
}

.input-area, .output-area {
  flex: 1;
  text-align: left;
}

h2 {
  color: #34495e;
  margin-bottom: 15px;
  font-size: 1.3em;
}

textarea {
  width: 100%;
  padding: 15px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 1em;
  line-height: 1.6;
  resize: vertical; /* 允许垂直方向调整大小 */
  box-sizing: border-box; /* 确保 padding 不会增加宽度 */
  background-color: #fff;
  margin-bottom: 15px;
}

textarea:focus {
  border-color: #3498db;
  outline: none;
  box-shadow: 0 0 5px rgba(52, 152, 219, 0.5);
}

button {
  background-color: #28a745;
  color: white;
  padding: 12px 25px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 1.1em;
  transition: background-color 0.3s ease;
}

button:hover:not(:disabled) {
  background-color: #218838;
}

button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

.error-message {
  color: #e74c3c;
  margin-top: 10px;
  font-weight: bold;
}

@media (max-width: 768px) {
  .editor-section {
    flex-direction: column;
  }
}
</style>