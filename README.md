# AI-Video-Search-Engine
Developed real-time transcript indexing and semantic search across multiple vide sources

AI-Driven Video Search Engine (Timestamp Retrieval)
A powerful web application that allows users to upload videos, index them with AI for multimodal content (audio + visuals), and perform semantic natural-language searches to retrieve precise video segments with timestamps.
Features

Upload videos (local files or URLs)
AI-powered indexing: speech transcription + visual description
Semantic search across all uploaded videos
Precise timestamp retrieval – jump directly to relevant moments
Responsive video player with auto-seek to matching segments
Clean, modern UI built with Angular

Tech Stack
Frontend

Angular (v18+ recommended)
Angular Material or Tailwind CSS for styling
RxJS for reactive state management
Videogular or native HTML5 video player for playback

Backend (Suggested)

FastAPI (Python) or Node.js
Whisper (transcription) + BLIP/CLIP (visual captions)
Sentence Transformers or multimodal embeddings
Vector DB: Pinecone / Weaviate / Milvus
Storage: S3 / local filesystem
Queue: Celery / Redis




UI Flow & User Journey
1. Dashboard / Home Page

Displays grid/list of all uploaded videos
Each video card shows:
Thumbnail
Title & duration
Upload date
Status badge: Processing | Ready | Failed

Floating Upload button
Global Search Bar at the top (always visible)

2. Video Upload Flow

Click Upload Video → Opens upload dialog/modal
Drag & drop file or paste URL (YouTube/private link supported if backend handles it)
Enter optional title/description
Submit → Progress bar + upload status
Backend processes asynchronously
Notification/toast: "Video uploaded – indexing in progress"
Status updates to "Ready" when indexing completes

3. Search Flow

User types natural language query in global search bar (e.g., "where does the chef add garlic")
Debounced search (300ms) → Calls /api/search?q=...
Results appear below in real-time:
Grid or list of Search Result Cards
Each card includes:
Video thumbnail (keyframe from timestamp)
Video title
Timestamp range badge (e.g., 2:15 – 2:45)
Highlighted text snippet with bolded matching terms
Relevance score (progress bar or percentage)
Play button



4. Playback Experience

Click on a search result → Opens Video Player Modal
Video auto-seeks to start_time and starts playing
Highlighted segment overlay on timeline (optional)
Timeline markers for all matches in this video
Sidebar shows:
Clickable transcript with timestamps
List of other matching moments in the same video

Full controls: play/pause, volume, fullscreen, seek
