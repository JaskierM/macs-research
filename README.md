# Multi Agent Cybersecurity System

## 1 Запуск моделей из Ollama на локалке

### Установка Ollama
```
curl -fsSL https://ollama.com/install.sh | sh
```

### Запуск пустого сервера
```
ollama serve
```

### Загрузка моделей для инференса
```
ollama pull mistral
```

Сейчас в качестве оркестратора (управляющей LLM) выбрана mistral (~4 гб видеопамяти) - она разворачивается вручную на ollama
Также для RAG в website search tool нужна эмбеддинговая модель (маленькая модель, которая просто переводит текст в вектора): для этого выбрана all-MiniLM-L6-v2 - она не из ollama, а из зависимости langchain-huggingface (разворачивается во время запуска кода)

Модели можно поменять, покопавшись в https://ollama.com/search

### Посмотреть какие модели работают на локале
```
ollama list
```
