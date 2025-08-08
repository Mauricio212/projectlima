#!/bin/bash

# Project Lima - Day 1, Hour 1-2: Tailwind CSS Integration
# ✅ Golden Rule #6 Compliant

cd ~/project_lima

# Install Node.js & npm (if not installed)
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Initialize npm and install Tailwind CSS
npm init -y
npm install tailwindcss @tailwindcss/cli --save-dev

# Create Tailwind config
npx tailwindcss init

# Create folder structure
mkdir -p static/src static/dist/css templates

# Create Tailwind base input file
cat > static/src/input.css << 'EOF'
@tailwind base;
@tailwind components;
@tailwind utilities;
EOF

# Configure tailwind.config.js for your project
cat > tailwind.config.js << 'EOF'
module.exports = {
  content: [
    "./templates/**/*.html",
    "./static/js/**/*.js",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
EOF
