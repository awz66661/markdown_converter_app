<template>
  <div id="app">
    <header>
      <h1>📝 Markdown 转换器</h1>
      <p class="subtitle">将 Markdown 转换为博客系统格式的利器</p>
    </header>

    <main>
      <div class="actions-bar">
        <button @click="loadSample" class="btn btn-secondary">
          <i class="icon">📋</i> 加载示例
        </button>
        <button @click="clearContent" class="btn btn-secondary">
          <i class="icon">🗑️</i> 清空内容
        </button>
      </div>

      <div
        class="drop-zone"
        :class="{ 'dragging': dragging }"
        @dragenter="handleDragEnter"
        @dragleave="handleDragLeave"
        @dragover="handleDragOver"
        @drop="handleDrop"
      >
        <div class="drop-content">
          <i class="drop-icon">📂</i>
          <p class="drop-text">将 Markdown 文件拖拽到此处</p>
          <p class="drop-subtext">或</p>
          <label class="btn btn-primary">
            <i class="icon">📁</i> 选择文件
            <input type="file" @change="handleFileSelect" accept=".md, text/markdown" class="file-input" />
          </label>
        </div>
      </div>

      <div class="editor-section">
        <div class="input-area card">
          <div class="card-header">
            <h2>📝 Markdown 输入</h2>
            <button @click="convertMarkdown" :disabled="isConverting" class="btn btn-small btn-primary">
              <i class="icon" v-if="isConverting">🔄</i>
              <i class="icon" v-else>⚡</i>
              {{ isConverting ? '转换中...' : '立即转换' }}
            </button>
          </div>
          <textarea
            v-model="markdownInput"
            placeholder="在这里粘贴或输入 Markdown 文本&#10;&#10;支持的语法：&#10;# 标题 → [h1]标题[/h1]&#10;## 标题 → [h2]标题[/h2]&#10;### 标题 → [h3]标题[/h3]&#10;**加粗** → <strong>加粗</strong>&#10;*斜体* → <em>斜体</em>"
            rows="15"
            @input="convertMarkdown"
            class="editor-textarea"
          ></textarea>
        </div>

        <div class="output-area card">
          <div class="card-header">
            <h2>✅ 转换结果</h2>
            <button @click="copyToClipboard" :disabled="!convertedOutput" class="btn btn-small btn-success">
              <i class="icon">📋</i> 复制结果
            </button>
          </div>
          <textarea
            v-model="convertedOutput"
            readonly
            rows="15"
            class="editor-textarea result-textarea"
          ></textarea>
        </div>
      </div>

      <div v-if="errorMessage" class="error-message">
        <i class="icon">⚠️</i> {{ errorMessage }}
      </div>
    </main>

    <footer>
      <p>© 2025 Markdown 转换器 - 专为博客内容创作而设计</p>
    </footer>
  </div>
</template>

<script>
export default {
  name: 'App',
  data() {
    return {
      markdownInput: '',
      convertedOutput: '',
      errorMessage: '',
      dragging: false,
      isConverting: false
    }
  },
  methods: {
    async convertMarkdown() {
      if (!this.markdownInput.trim()) {
        this.convertedOutput = '';
        return;
      }

      try {
        this.isConverting = true;
        this.errorMessage = '';

        const response = await fetch('/api/convert', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ markdown_text: this.markdownInput }),
        });

        if (!response.ok) {
          throw new Error('转换失败');
        }

        const data = await response.json();
        this.convertedOutput = data.converted_text;
      } catch (error) {
        this.errorMessage = '转换失败，请检查后端服务是否运行正常';
        console.error('转换错误:', error);
      } finally {
        this.isConverting = false;
      }
    },

    loadSample() {
      this.markdownInput = `# 一级标题
## 二级标题
### 三级标题
#### 四级标题

这是一段普通文本，包含**加粗**和*斜体*文字。

**特性列表：**
- 第一个特性
- 第二个特性
- 第三个特性

**步骤说明：**
1. 第一步操作
2. 第二步操作
3. 第三步操作

| 列1 | 列2 | 列3 |
|-----|-----|-----|
| 数据1 | 数据2 | 数据3 |
| 数据4 | 数据5 | 数据6 |`;
      this.convertMarkdown();
    },

    clearContent() {
      this.markdownInput = '';
      this.convertedOutput = '';
      this.errorMessage = '';
    },

    async copyToClipboard() {
      try {
        await navigator.clipboard.writeText(this.convertedOutput);
        alert('已复制到剪贴板！');
      } catch (err) {
        this.errorMessage = '复制失败，请手动选择复制';
      }
    },

    handleDragEnter(e) {
      e.preventDefault();
      this.dragging = true;
    },

    handleDragLeave(e) {
      e.preventDefault();
      this.dragging = false;
    },

    handleDragOver(e) {
      e.preventDefault();
    },

    handleDrop(e) {
      e.preventDefault();
      this.dragging = false;

      const files = e.dataTransfer.files;
      if (files.length > 0) {
        this.handleFile(files[0]);
      }
    },

    handleFileSelect(e) {
      const files = e.target.files;
      if (files.length > 0) {
        this.handleFile(files[0]);
      }
    },

    handleFile(file) {
      if (!file.name.endsWith('.md') && !file.type.includes('markdown')) {
        this.errorMessage = '请选择 Markdown 文件（.md）';
        return;
      }

      const reader = new FileReader();
      reader.onload = (e) => {
        this.markdownInput = e.target.result;
        this.convertMarkdown();
        this.errorMessage = '';
      };
      reader.onerror = () => {
        this.errorMessage = '文件读取失败';
      };
      reader.readAsText(file);
    }
  }
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  min-height: 100vh;
  color: #333;
}

#app {
  max-width: 1400px;
  margin: 0 auto;
  padding: 20px;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

header {
  text-align: center;
  margin-bottom: 30px;
  color: white;
  padding: 20px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 15px;
  backdrop-filter: blur(10px);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

header h1 {
  font-size: 2.5rem;
  margin-bottom: 10px;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
}

.subtitle {
  font-size: 1.2rem;
  opacity: 0.9;
}

.actions-bar {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
  justify-content: center;
}

.btn {
  padding: 12px 20px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 500;
  transition: all 0.3s ease;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  text-decoration: none;
}

.btn-primary {
  background: #4CAF50;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background: #45a049;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(76, 175, 80, 0.3);
}

.btn-secondary {
  background: #2196F3;
  color: white;
}

.btn-secondary:hover:not(:disabled) {
  background: #1976D2;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(33, 150, 243, 0.3);
}

.btn-success {
  background: #FF9800;
  color: white;
}

.btn-success:hover:not(:disabled) {
  background: #F57C00;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(255, 152, 0, 0.3);
}

.btn-small {
  padding: 8px 16px;
  font-size: 0.9rem;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.btn:disabled:hover {
  transform: none;
  box-shadow: none;
}

.icon {
  font-style: normal;
}

.drop-zone {
  border: 3px dashed rgba(255, 255, 255, 0.5);
  padding: 40px;
  margin-bottom: 30px;
  cursor: pointer;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 15px;
  transition: all 0.3s ease;
  text-align: center;
  backdrop-filter: blur(5px);
}

.drop-zone.dragging {
  background: rgba(255, 255, 255, 0.2);
  border-color: #4CAF50;
  transform: scale(1.02);
}

.drop-content {
  color: white;
}

.drop-icon {
  font-size: 3rem;
  display: block;
  margin-bottom: 15px;
}

.drop-text {
  font-size: 1.3rem;
  margin-bottom: 10px;
  font-weight: 500;
}

.drop-subtext {
  font-size: 1rem;
  opacity: 0.8;
  margin: 15px 0;
}

.file-input {
  display: none;
}

.editor-section {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 25px;
  margin-bottom: 20px;
}

@media (max-width: 768px) {
  .editor-section {
    grid-template-columns: 1fr;
  }
  
  header h1 {
    font-size: 2rem;
  }
  
  .actions-bar {
    flex-direction: column;
    align-items: center;
  }
}

.card {
  background: white;
  border-radius: 15px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  backdrop-filter: blur(10px);
}

.card-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header h2 {
  font-size: 1.4rem;
  font-weight: 500;
}

.editor-textarea {
  width: 100%;
  padding: 20px;
  border: none;
  resize: vertical;
  font-size: 1rem;
  line-height: 1.6;
  min-height: 300px;
  font-family: 'Consolas', 'Monaco', monospace;
  background: #fafafa;
  transition: background-color 0.3s ease;
}

.editor-textarea:focus {
  outline: none;
  background: #fff;
  box-shadow: inset 0 0 10px rgba(0, 0, 0, 0.1);
}

.result-textarea {
  background: #f8f9fa;
}

.result-textarea:focus {
  background: #fff;
}

.error-message {
  background: #ffebee;
  color: #c62828;
  padding: 15px 20px;
  border-radius: 8px;
  margin-top: 20px;
  display: flex;
  align-items: center;
  gap: 10px;
  border-left: 4px solid #c62828;
}

footer {
  text-align: center;
  margin-top: auto;
  padding: 30px 20px 20px;
  color: rgba(255, 255, 255, 0.8);
  font-size: 0.9rem;
}

/* 滚动条样式 */
.editor-textarea::-webkit-scrollbar {
  width: 8px;
}

.editor-textarea::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 4px;
}

.editor-textarea::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 4px;
}

.editor-textarea::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}

/* 动画效果 */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.card {
  animation: fadeIn 0.5s ease-out;
}

/* 响应式设计 */
@media (max-width: 1024px) {
  #app {
    padding: 15px;
  }
  
  .editor-section {
    gap: 20px;
  }
}

@media (max-width: 480px) {
  #app {
    padding: 10px;
  }
  
  header {
    padding: 15px;
  }
  
  header h1 {
    font-size: 1.8rem;
  }
  
  .subtitle {
    font-size: 1rem;
  }
  
  .drop-zone {
    padding: 30px 20px;
  }
  
  .card-header {
    padding: 15px;
  }
  
  .card-header h2 {
    font-size: 1.2rem;
  }
  
  .editor-textarea {
    padding: 15px;
    min-height: 250px;
  }
}
</style>