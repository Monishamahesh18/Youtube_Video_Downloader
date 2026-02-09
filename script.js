// Sample video data
const videos = [
    {
        id: 1,
        title: "How to Build a Modern Website with HTML, CSS & JavaScript",
        channel: "Web Dev Tutorials",
        views: "1.2M views",
        time: "2 days ago",
        duration: "15:30",
        thumbnail: "https://picsum.photos/320/180?random=1"
    },
    {
        id: 2,
        title: "React Tutorial for Beginners - Complete Course",
        channel: "Code Academy",
        views: "850K views",
        time: "5 days ago",
        duration: "42:15",
        thumbnail: "https://picsum.photos/320/180?random=2"
    },
    {
        id: 3,
        title: "CSS Grid vs Flexbox - Which Should You Use?",
        channel: "CSS Mastery",
        views: "650K views",
        time: "1 week ago",
        duration: "18:45",
        thumbnail: "https://picsum.photos/320/180?random=3"
    },
    {
        id: 4,
        title: "JavaScript ES6+ Features You Need to Know",
        channel: "JS Ninja",
        views: "1.5M views",
        time: "3 days ago",
        duration: "25:20",
        thumbnail: "https://picsum.photos/320/180?random=4"
    },
    {
        id: 5,
        title: "Building a Full-Stack App with Node.js",
        channel: "Full Stack Dev",
        views: "920K views",
        time: "6 days ago",
        duration: "38:10",
        thumbnail: "https://picsum.photos/320/180?random=5"
    },
    {
        id: 6,
        title: "Python for Data Science - Complete Guide",
        channel: "Data Science Pro",
        views: "2.1M views",
        time: "1 week ago",
        duration: "55:30",
        thumbnail: "https://picsum.photos/320/180?random=6"
    },
    {
        id: 7,
        title: "UI/UX Design Principles for Developers",
        channel: "Design Code",
        views: "780K views",
        time: "4 days ago",
        duration: "22:15",
        thumbnail: "https://picsum.photos/320/180?random=7"
    },
    {
        id: 8,
        title: "Git & GitHub Tutorial for Beginners",
        channel: "Version Control",
        views: "1.8M views",
        time: "2 weeks ago",
        duration: "30:45",
        thumbnail: "https://picsum.photos/320/180?random=8"
    },
    {
        id: 9,
        title: "Docker Containerization Explained",
        channel: "DevOps Guide",
        views: "640K views",
        time: "1 week ago",
        duration: "20:30",
        thumbnail: "https://picsum.photos/320/180?random=9"
    },
    {
        id: 10,
        title: "TypeScript vs JavaScript - When to Use What?",
        channel: "TypeScript Master",
        views: "950K views",
        time: "5 days ago",
        duration: "16:20",
        thumbnail: "https://picsum.photos/320/180?random=10"
    },
    {
        id: 11,
        title: "RESTful API Design Best Practices",
        channel: "API Expert",
        views: "720K views",
        time: "3 days ago",
        duration: "28:50",
        thumbnail: "https://picsum.photos/320/180?random=11"
    },
    {
        id: 12,
        title: "Vue.js 3 Composition API Tutorial",
        channel: "Vue Mastery",
        views: "580K views",
        time: "1 week ago",
        duration: "35:15",
        thumbnail: "https://picsum.photos/320/180?random=12"
    }
];

// DOM Elements
const menuBtn = document.getElementById('menuBtn');
const sidebar = document.getElementById('sidebar');
const mainContent = document.querySelector('.main-content');
const videoContainer = document.getElementById('videoContainer');
const searchForm = document.getElementById('searchForm');
const searchInput = document.getElementById('searchInput');

// Toggle sidebar
let sidebarOpen = true;
menuBtn.addEventListener('click', () => {
    sidebarOpen = !sidebarOpen;
    if (sidebarOpen) {
        sidebar.classList.remove('hidden');
        mainContent.classList.remove('expanded');
    } else {
        sidebar.classList.add('hidden');
        mainContent.classList.add('expanded');
    }
});

// Render videos
function renderVideos(videoList) {
    videoContainer.innerHTML = '';
    videoList.forEach(video => {
        const videoCard = createVideoCard(video);
        videoContainer.appendChild(videoCard);
    });
}

// Create video card element
function createVideoCard(video) {
    const card = document.createElement('div');
    card.className = 'video-card';
    card.innerHTML = `
        <div class="video-thumbnail">
            <img src="${video.thumbnail}" alt="${video.title}" loading="lazy">
            <span class="video-duration">${video.duration}</span>
        </div>
        <div class="video-info">
            <div class="channel-avatar">${video.channel.charAt(0)}</div>
            <div class="video-details">
                <h3 class="video-title">${video.title}</h3>
                <div class="video-meta">
                    <span class="channel-name">${video.channel}</span>
                    <span>${video.views} • ${video.time}</span>
                </div>
            </div>
        </div>
    `;
    
    card.addEventListener('click', () => {
        console.log('Playing video:', video.title);
        // Add video player functionality here
    });
    
    return card;
}

// Search functionality
searchForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const searchTerm = searchInput.value.toLowerCase().trim();
    
    if (searchTerm === '') {
        renderVideos(videos);
        return;
    }
    
    const filteredVideos = videos.filter(video => 
        video.title.toLowerCase().includes(searchTerm) ||
        video.channel.toLowerCase().includes(searchTerm)
    );
    
    renderVideos(filteredVideos);
});

// Handle sidebar navigation
document.querySelectorAll('.nav-item').forEach(item => {
    item.addEventListener('click', (e) => {
        e.preventDefault();
        document.querySelectorAll('.nav-item').forEach(nav => nav.classList.remove('active'));
        item.classList.add('active');
        
        // Handle different navigation items
        const navText = item.querySelector('span').textContent;
        console.log('Navigating to:', navText);
        
        // Reset to all videos when clicking Home
        if (navText === 'Home') {
            renderVideos(videos);
        }
    });
});

// Initialize - render all videos
renderVideos(videos);

// Handle responsive sidebar on mobile
function handleResize() {
    if (window.innerWidth <= 768) {
        sidebar.classList.add('hidden');
        mainContent.classList.add('expanded');
        sidebarOpen = false;
    } else {
        if (!sidebarOpen) {
            sidebar.classList.remove('hidden');
            mainContent.classList.remove('expanded');
            sidebarOpen = true;
        }
    }
}

window.addEventListener('resize', handleResize);
handleResize();
