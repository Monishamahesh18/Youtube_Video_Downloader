# YouTube Clone Website

A modern, responsive YouTube clone built with HTML, CSS, and JavaScript.

## Features

- 🎨 Modern dark theme UI
- 📱 Fully responsive design
- 🔍 Search functionality
- 📺 Video grid layout
- 🎯 Interactive sidebar navigation
- ⚡ Smooth animations and transitions

## Getting Started

### Option 1: Open directly in browser
Simply open `index.html` in your web browser.

### Option 2: Use a local server (recommended)

#### Using Python:
```bash
# Python 3
python -m http.server 8000

# Python 2
python -m SimpleHTTPServer 8000
```

#### Using Node.js (http-server):
```bash
npx http-server
```

#### Using VS Code Live Server:
1. Install the "Live Server" extension
2. Right-click on `index.html`
3. Select "Open with Live Server"

Then navigate to `http://localhost:8000` (or the port shown) in your browser.

## Project Structure

```
youtube-website/
├── index.html      # Main HTML structure
├── styles.css      # All styling and responsive design
├── script.js       # JavaScript functionality
└── README.md       # This file
```

## Customization

### Changing Colors
Edit the CSS variables in `styles.css`:
```css
:root {
    --primary-color: #ff0000;      /* YouTube red */
    --bg-color: #0f0f0f;           /* Background */
    --surface-color: #181818;      /* Cards/surfaces */
    --text-primary: #ffffff;       /* Main text */
    --text-secondary: #aaaaaa;     /* Secondary text */
}
```

### Adding Videos
Edit the `videos` array in `script.js` to add your own video data.

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## License

This project is open source and available for educational purposes.
